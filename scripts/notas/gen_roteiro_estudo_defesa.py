"""Roteiro de estudo da defesa: slide a slide e capítulo a capítulo do palco, na ordem
da apresentação (PPTX 1-21 → painel HTML → PPTX 22-23), com fundamentos de cada tema
e conteúdo adicional (apêndice) no fim.

    python gen_roteiro_estudo_defesa.py [--preview <pasta>]

Imagens:
  - slides: PNG de cada slide em SLIDES_PNG (s01.png...), gerados pelo render.ps1 da
    skill tcc-pptx-editor sobre uma cópia do deck (nunca o do OneDrive);
  - palco: output/verifica_palco/1920x1080/, gerados por scripts/verifica_palco.py.
As duas pastas são convertidas para JPEG reduzido em SLIDES_PNG/../jpg antes de entrar
no PDF (os PNGs originais deixariam o arquivo com dezenas de MB).
"""
import sys
from pathlib import Path

from PIL import Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.units import cm
from reportlab.platypus import (CondPageBreak, Image as RLImage, KeepTogether, Paragraph, Spacer, Table,
                                TableStyle)

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pdfnote import ACCENT, MUTED, Note, _style, render_preview  # noqa: E402

SLIDES_PNG = Path(r"C:\Temp\defesa_roteiro\png")
PALCO_PNG = ROOT / "output" / "verifica_palco" / "1920x1080"
CACHE = SLIDES_PNG.parent / "jpg"
CACHE.mkdir(parents=True, exist_ok=True)
W = 14.7  # largura útil em cm


def jpg(src: Path, largura=1300) -> Path:
    """Cópia JPEG reduzida da imagem (cache por nome e data)."""
    dst = CACHE / (src.parent.name + "_" + src.stem + ".jpg")
    if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
        with Image.open(src) as im:
            im = im.convert("RGB")
            if im.width > largura:
                im = im.resize((largura, round(im.height * largura / im.width)), Image.LANCZOS)
            im.save(dst, "JPEG", quality=86, optimize=True)
    return dst


RAP_PDF = Path(r"C:\Users\victo\OneDrive\Meus Bagulhos\Arquivos\UERJ\TCC - Victor e Bruno"
               r"\Bibliografia\RAP 2023.08.15 08h030min versão final.pdf")


if not RAP_PDF.exists():
    RAP_PDF = Path.home() / "OneDrive" / "UERJ" / "TCC - Victor e Bruno" / "Bibliografia" / "RAP 2023.08.15 08h030min versão final.pdf"


def rap_fig(nome, pagina, clip) -> Path:
    """Recorte de uma figura do RAP-ONS 00012/2023 (página 1-based, clip em pt)."""
    dst = CACHE / f"rap_{nome}.jpg"
    if not dst.exists():
        import pymupdf
        with pymupdf.open(RAP_PDF) as d:
            pix = d[pagina - 1].get_pixmap(dpi=220, clip=pymupdf.Rect(*clip))
            png = CACHE / f"rap_{nome}.png"
            pix.save(png)
        with Image.open(png) as im:
            im.convert("RGB").save(dst, "JPEG", quality=88, optimize=True)
        png.unlink()
    return dst


n = Note(
    title="Roteiro de estudo da defesa",
    subtitle="Slide a slide e capítulo a capítulo, na ordem em que a apresentação acontece "
             "(PPTX, painel HTML e de volta ao PPTX), com os fundamentos de cada tema",
    out=ROOT / "output" / "roteiro_estudo_defesa.pdf",
    meta_left="Victor e Bruno<br/>Comportamento do SRF-PLL de inversores frente a contingências",
    meta_right="Material de estudo<br/>25 de outubro de 2026",
    running_head="Roteiro de estudo da defesa",
)

# ------------------------------------------------------------------ estilos locais
S_BOXT = _style("boxt", fontName="TNR-Bold", fontSize=8.6, leading=11, spaceAfter=0)
S_BOX = _style("box", fontSize=10.3, leading=14.4, spaceAfter=0, alignment=TA_JUSTIFY)
S_MSG = _style("msg", fontName="TNR-Bold", fontSize=12.2, leading=16.2, spaceAfter=0,
               textColor=ACCENT)
S_SUB = _style("sub", fontName="TNR-Bold", fontSize=11.3, leading=14.5, textColor=ACCENT,
               spaceBefore=8, spaceAfter=4, keepWithNext=1)
S_BUL = _style("bul", leftIndent=15, bulletIndent=4, spaceAfter=3.5, alignment=TA_JUSTIFY)
S_ONDE = _style("onde", fontSize=9.4, leading=12.8, textColor=MUTED, leftIndent=12,
                spaceAfter=7, alignment=TA_JUSTIFY)
S_PONTE = _style("ponte", fontName="TNR-Italic", fontSize=10.3, leading=14,
                 textColor=MUTED, spaceBefore=4)
S_BAND_L = _style("bandl", fontName="TNR-Bold", fontSize=8.5, leading=10,
                  textColor=colors.white, spaceAfter=0, alignment=1)
S_BAND_N = _style("bandn", fontName="TNR-Bold", fontSize=22, leading=24,
                  textColor=colors.white, spaceAfter=0, alignment=1)
S_BAND_T = _style("bandt", fontName="TNR-Bold", fontSize=15, leading=18, textColor=ACCENT,
                  spaceAfter=1)
S_BAND_M = _style("bandm", fontSize=9.2, leading=12, textColor=MUTED, spaceAfter=0)

KIND = {  # fundo, barra, rótulo
    "msg": ("#E7EFF6", "#1A4A6E", "MENSAGEM"),
    "banca": ("#EDF4FB", "#2F6FA8", "PERGUNTA DO RODAPÉ DO SLIDE"),
    "prova": ("#F3EEF8", "#6B4C9A", "PERGUNTA PROVÁVEL DA BANCA"),
    "cuidado": ("#FDF3E1", "#C27C0E", "CUIDADO"),
    "alem": ("#EAF4EC", "#3D8A57", "ALÉM DO TCC · para entender e responder, não para a fala"),
    "passo": ("#F4F7F9", "#5A6B78", "PASSOS DO CAPÍTULO"),
    "fala": ("#FBF6EC", "#8A6D3B", "O QUE FALAR · tópicos para dizer com as suas palavras"),
    "base": ("#EEF2F7", "#34495E", "RELEMBRANDO CONTROLE · em uma frase"),
}


def box(kind, *paras, titulo=None):
    """Caixa colorida de uma célula só: o reportlab não parte tabela de uma linha,
    então a caixa nunca fica com o título numa página e o texto na outra."""
    bg, bar, rot = KIND[kind]
    estilo = S_MSG if kind == "msg" else S_BOX
    conteudo = [Paragraph(f"<font color='{bar}'>{titulo or rot}</font>", S_BOXT)]
    for p_ in paras:
        conteudo += [Spacer(1, 3), Paragraph(p_, estilo)]
    t = Table([[conteudo]], colWidths=[W * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(bg)),
        ("LINEBEFORE", (0, 0), (0, -1), 3, colors.HexColor(bar)),
        ("LEFTPADDING", (0, 0), (-1, -1), 11), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    n.story.append(t)
    n.gap(8)


def sub(text):
    n.story.append(Paragraph(text, S_SUB))


def bul(*items):
    for it in items:
        n.story.append(Paragraph(it, S_BUL, bulletText="•"))
    n.gap(3)


def eq(tex, tag=None, onde=None):
    n.eq_tex(tex, tag, fontsize=12.5)
    if onde:
        n.story.append(Paragraph(onde, S_ONDE))
    else:
        n.gap(7)


def tab(header, rows, widths):
    n.table(header, rows, widths)
    if len(rows) <= 6:  # tabela curta não se parte entre páginas
        bloco = [n.story.pop()]
        anterior = n.story[-1] if n.story else None
        if isinstance(anterior, Paragraph) and getattr(anterior.style, "keepWithNext", 0):
            bloco.insert(0, n.story.pop())  # título vai junto com a tabela
        n.story.append(KeepTogether(bloco))
    n.gap(8)


def nums(rows):
    tab(["Número", "O que é"], rows, [3.9, 10.8])


def figura(caminho, legenda, largura=W):
    with Image.open(caminho) as im:
        h = largura * cm * im.height / im.width
    img = RLImage(str(caminho), width=largura * cm, height=h)
    img.hAlign = "CENTER"
    n.story.append(KeepTogether([img, Spacer(1, 3), Paragraph(legenda, n.s_tag)]))
    n.gap(6)


S_INST = _style("inst", fontName="TNR-Bold", fontSize=11, leading=13.5, textColor=ACCENT,
                spaceAfter=0)


def instante(quando, titulo, primeiro):
    """Selo do instante, título do passo e o primeiro parágrafo, sempre na mesma página."""
    t = Table([[Paragraph(quando, S_BAND_L), Paragraph(titulo, S_INST)]],
              colWidths=[3.1 * cm, (W - 3.1) * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), ACCENT), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4), ("LINEBELOW", (1, 0), (1, 0), 0.6, ACCENT),
    ]))
    n.story.append(KeepTogether([Spacer(1, 8), t, Spacer(1, 5),
                                 Paragraph(primeiro, n.s_body)]))


def ponte(text):
    # prende a ponte ao bloco anterior (caixa + espaçador): sem linha solta na página seguinte
    ultimos = [n.story.pop(), n.story.pop()][::-1]
    n.story.append(KeepTogether(ultimos + [Paragraph(f"&#8594; <b>Próximo:</b> {text}",
                                                     S_PONTE)]))


PARTE = []  # título e abertura de parte, impressos na página do próximo slide


def parte(titulo, *paras):
    PARTE.extend([Paragraph(titulo, n.s_h)] + [Paragraph(x, n.s_body) for x in paras])


def faixa(rotulo, num, titulo, meta, imagem=None, alt=6.0, legenda=None):
    """Faixa de título e miniatura juntas; página nova só se não couberem com folga
    (sobra de um slide curto não vira página quase vazia)."""
    n.story.append(CondPageBreak((alt + 4.5) * cm))
    n.story.extend(PARTE)
    PARTE.clear()
    band = Table([[[Paragraph(rotulo, S_BAND_L), Paragraph(str(num), S_BAND_N)],
                   [Paragraph(titulo, S_BAND_T), Paragraph(meta, S_BAND_M)]]],
                 colWidths=[2.1 * cm, (W - 2.1) * cm])
    band.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), ACCENT),
        ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#F4F7F9")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (1, 0), (1, 0), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    bloco = [band]
    if imagem:
        with Image.open(imagem) as im:
            asp = im.height / im.width
        w = W * cm
        h = w * asp
        if h > alt * cm:
            h = alt * cm
            w = h / asp
        img = RLImage(str(imagem), width=w, height=h)
        img.hAlign = "CENTER"
        bloco += [Table([[img]], colWidths=[W * cm], style=TableStyle([
            ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))]
        if legenda:
            bloco.append(Paragraph(legenda, n.s_tag))
    n.story.append(KeepTogether(bloco))
    n.gap(10)


def slide(num, titulo, bloco, quem, tcc):
    faixa("SLIDE", num, titulo, f"{bloco} &#160;·&#160; Fala: {quem} &#160;·&#160; No TCC: {tcc}",
          jpg(SLIDES_PNG / f"s{num:02d}.png"))


def cap(num, titulo, ref, png, legenda):
    faixa("PAINEL", num, titulo, ref, jpg(PALCO_PNG / png), alt=7.8, legenda=legenda)


def imagem_palco(png, legenda, alt=8.6):
    n.image(jpg(PALCO_PNG / png), width_cm=W, max_height_cm=alt, caption=legenda)


# =============================================================================
# ABERTURA
# =============================================================================
n.h("Como usar este roteiro")
n.p("O roteiro segue a apresentação na ordem real, uma página (ou mais) por slide: os "
    "slides 1 a 18 no PowerPoint, o slide 19 como porta para o painel HTML, os oito "
    "capítulos do <b>modo apresentação</b> e a volta ao PowerPoint nos slides 20 e 21. O "
    "apêndice do deck e os slides ocultos ficam no fim, como <b>conteúdo adicional</b>. Não "
    "há texto de fala para decorar; na modelagem (slides 5 a 16), uma caixa <b>O que falar</b> "
    "dá os tópicos de cada um, na ordem e com quem fala.")
n.p("Cada página tem a miniatura e, embaixo, blocos sempre na mesma ordem:")
bul("<b>Mensagem</b>: a frase que o slide tem de deixar na cabeça da banca.",
    "<b>Fundamentos</b>: a teoria por trás, com as equações, para explicar com as próprias "
    "palavras e aguentar a pergunta seguinte. Quando a equação é do TCC, o número dela "
    "aparece à direita entre parênteses, como (3.18).",
    "<b>Números</b> para saber de cor, todos do TCC entregue (VFinal, 15/10/2026).",
    "<font color='#8A6D3B'><b>O que falar</b></font> (só na modelagem): o roteiro da fala "
    "em tópicos, logo abaixo da mensagem, para dizer com as próprias palavras.",
    "Caixas coloridas: <font color='#2F6FA8'><b>pergunta do rodapé</b></font> do slide, "
    "<font color='#6B4C9A'><b>pergunta provável</b></font> da banca, "
    "<font color='#C27C0E'><b>cuidado</b></font> e <font color='#3D8A57'><b>além do "
    "TCC</b></font> (conta ou leitura física que não está no texto: para entender e "
    "responder, não para dizer por iniciativa própria).",
    "<b>Próximo</b>: a ponte para o slide seguinte.")

n.h("O percurso")
tab(["Trecho", "Onde", "Conteúdo", "Fala"], [
    ["Abertura", "PPTX 1", "Capa, autores, orientadores", "Bruno, Victor"],
    ["Motivação", "PPTX 2-4", "Renováveis, blecautes, problema e objetivos", "Bruno, Victor"],
    ["Modelagem", "PPTX 5-16", "Inversor, Park, SRF-PLL, rede, sintonia, LCL, corrente, ONS",
     "alternada"],
    ["Método", "PPTX 17-18", "Protocolo de falta e fluxo de análise", "Bruno, Victor"],
    ["Porta", "PPTX 19", "Alt+Tab para o navegador, botão Modo apresentação", "Victor"],
    ["Resultados", "HTML 1-8", "Faltas destacadas ... Todos os casos (passador avança)",
     "a definir"],
    ["Conclusão", "PPTX 20-21", "Síntese e trabalhos futuros", "Bruno, Victor"],
    ["Adicional", "PPTX 22-29", "Apêndice e slides ocultos, para perguntas", "os dois"],
], [2.3, 2.6, 7.6, 2.2])

n.h("A história em cinco frases")
for i, f in enumerate([
        "A geração nova chega por inversores, e a rede perde a sustentação natural das "
        "máquinas síncronas; os blecautes de 2023 e 2025 passaram por esse elo.",
        "O inversor seguidor de rede só sabe onde está a tensão porque o SRF-PLL estima o "
        "ângulo dela, e a falta destrói justamente a tensão que o PLL mede.",
        "Com a sintonia nominal, o PLL atravessa as faltas trifásicas e volta ao sincronismo "
        "em todos os pontos, com severidade ditada pela distância elétrica.",
        "Nas faltas assimétricas, a sequência negativa vira 120 Hz no referencial dq, perto "
        "demais da banda do PI para ser filtrada; reduzir os ganhos filtra melhor, mas na "
        "falta mais severa faz o PLL perder o sincronismo e a usina absorver potência.",
        "Logo, ficar conectado, que é o que a verificação de hoje pergunta, não basta: é "
        "preciso olhar a qualidade do rastreamento angular durante e depois da falta."], 1):
    n.story.append(Paragraph(f, S_BUL, bulletText=f"{i}."))
n.gap(6)

n.h("Convenções que valem para tudo")
tab(["Use", "Evite", "Por quê"], [
    ["sintonia inadequada", "BAD_PLL, PLL ruim", "nome de código não vai para a banca"],
    ["escorregamento de ciclo", "cycle slipping", "é o termo do palco"],
    ["simulação computacional", "a sigla de transitórios eletromagnéticos",
     "o orientador não gostou; fora do deck e do TCC"],
    ["recuperar o sincronismo", "reaquisitar", "a palavra não existe"],
    ["azul = nominal, laranja = inadequada", "trocar as cores", "vale no deck e no painel"],
], [4.6, 4.2, 5.9])
n.note("Sem RoCoF (fora do escopo) e sem citar a contagem exata de cenários: o TCC tem 28 na "
       "Tabela 4.1 e usa 29 no Cap. 5 (defesa_qa.pdf, pergunta 1).")

# tópicos de fala da modelagem (5-17), tirados das notas do deck
FALAS = {
5: [("Victor", "&#8220;Começamos pela usina.&#8221; Aponte a Figura 3.2: à esquerda, a fonte primária, "
     "um barramento CC ideal. Diga o porquê numa frase: sem elo CC e sem MPPT, tudo o que se vê "
     "na falta vem do lado CA e do sincronismo."),
    ("Bruno", "Siga a figura da esquerda para a direita: o inversor transforma CC em CA, passa pelo "
     "filtro e entrega os 100 MW na Barra 2. Ele é <b>seguidor de rede</b>: mede a tensão e o "
     "SRF-PLL, em laranja, estima o ângulo. Feche com a pergunta do rodapé: como ele segue a rede?")],
6: [("Victor", "Comece pelo problema: um PI não zera o erro de uma senoide. A transformada de Park "
     "projeta as três fases em dois eixos, d e q, que giram junto com a rede."),
    ("Bruno", "Aponte o painel da direita: girando junto, a senoide de 60 Hz vira uma constante, e "
     "aí o PI funciona. Mas a conta inteira depende de &#952;: &#8220;quem dá esse ângulo é o "
     "PLL&#8221;. Desça para as duas linhas sob a matriz: com o ângulo do PLL, v<sub>d</sub> é a "
     "amplitude vezes o cosseno do erro, v<sub>q</sub> vezes o seno; travado, v<sub>q</sub> = 0, "
     "e é esse v<sub>q</sub> que o PLL zera.")],
7: [("Victor", "Três blocos, um por área tracejada. O detector de fase é a própria Park: com o eixo "
     "d alinhado, a amplitude toda fica em v<sub>d</sub> e v<sub>q</sub> vale zero. Então "
     "v<sub>q</sub> é o erro de ângulo."),
    ("Bruno", "O PI recebe v<sub>q</sub> e devolve a correção &#916;&#969;; somada aos 60 Hz, entra "
     "no VCO, um integrador, que devolve &#952; para a Park e para as correntes. Cartão da "
     "direita: com o PI, o laço é de segunda ordem, K<sub>p</sub> = 2&#958;&#969;<sub>n</sub> e "
     "K<sub>i</sub> = &#969;<sub>n</sub>&#178;. Se &#952; erra, a corrente sai orientada errado.")],
8: [("Victor", "O sistema de teste: IEEE 9 barras. O G2, de 192 MVA, sai; a usina de 100 MW entra "
     "na Barra 2. G1 e G3 continuam síncronos e carregam a inércia que sobra."),
    ("Bruno", "Três geradores, três transformadores, seis linhas e três cargas, em 230 kV; os 100 MW "
     "são 1 pu na base de 100 MVA. As faltas mudam de lugar para variar a distância elétrica, com "
     "o nível de curto fixo (é uma limitação, volta no fim)."),
    ("Victor", "Duas ferramentas: no PSIM, a rede vira um Thévenin na Barra 2, tirado da matriz de "
     "impedância nodal; no Simulink, roda o sistema completo.")],
9: [("Bruno", "Antes do inversor, uma bancada no PSIM: duas fontes ideais ligadas pela impedância "
     "da rede. Sem chaves e sem LCL, só o laço do PLL."),
    ("Victor", "O que se olhou ali: v<sub>q</sub> indo a zero e o ângulo travando. Os ganhos do "
     "próximo slide foram validados nessa bancada. Nenhum número neste slide.")],
10: [("Victor", "Etapa 1: a tensão entra em pu, dividida pelo pico nominal de fase, 16.329,93 V. "
      "Assim o ganho do detector vale 1 e v<sub>q</sub> é o próprio erro de ângulo."),
     ("Bruno", "Etapas 2 a 4: linearizado, o laço tem a forma canônica, K<sub>i</sub> = "
      "&#969;<sub>n</sub>&#178; e K<sub>p</sub> = 2&#958;&#969;<sub>n</sub>. Fixa-se &#958; = 0,707, "
      "o clássico de Ogata, com cerca de 5% de sobre-elevação. Sobra um só grau de liberdade: "
      "t<sub>s</sub>."),
     ("Victor", "Use a régua: t<sub>s</sub> = 4,6/(&#958;&#969;<sub>n</sub>) pelo critério de 1%. "
      "Curto demais deixa passar ruído e desequilíbrio; longo demais não acompanha a rede. 20 ms, "
      "pouco mais de um ciclo, como em Alves, Dias e Rolim (2020) e Teodorescu, Liserre e "
      "Rodriguez (2011). Leia a caixa final: K<sub>p</sub> = 460, &#969;<sub>n</sub> = 325,3 rad/s "
      "(51,8 Hz), K<sub>i</sub> = 105.820.")],
11: [("Bruno", "Aponte a coluna laranja: a sintonia inadequada multiplica os dois ganhos por 0,2, "
      "92 e 21.164. A &#969;<sub>n</sub> cai para 145,5 rad/s e o &#958; para 0,316: laço mais lento "
      "e menos amortecido. No caso-limite, o PLL não recupera o sincronismo depois da falta."),
     ("Victor", "Cartão da direita, a ponte para os resultados: na falta assimétrica, a sequência "
      "negativa vira 120 Hz em v<sub>q</sub>, 754 rad/s, só 2,32 vezes a &#969;<sub>n</sub>. O PI "
      "não atenua e a oscilação passa para o ângulo. &#8220;É esse mecanismo que investigamos.&#8221;")],
12: [("Victor", "Agora o inversor. Na primeira versão, no PSIM, pede-se 1 pu de ativo (os 100 MW) "
      "num degrau aos 35 ms e reativo zero. Cada um é dividido pelo v<sub>d</sub> que vem do PLL, e "
      "saem as referências de corrente."),
     ("Bruno", "Cartão de baixo, à esquerda: é a equação de potência em dq invertida. Só vale com "
      "v<sub>q</sub> = 0, eixo d alinhado, e quem garante isso é o PLL.")],
13: [("Bruno", "&#8220;Antes da malha de corrente, o filtro que liga o inversor à rede.&#8221; "
      "Percorra a figura da esquerda para a direita: barramento CC constante, inversor a 5 kHz, "
      "o LCL e o PCC. Passos 1 e 2: L<sub>1</sub> sai do limite de ondulação da corrente "
      "(depende de V<sub>cc</sub> e f<sub>sw</sub>); L<sub>2</sub> é proporcional a L<sub>1</sub>; "
      "somados, L<sub>est</sub> = 30,71 mH, que volta no PI de corrente."),
     ("Victor", "Passo 3: o capacitor fecha a ressonância em 9.068,99 rad/s; aponte a régua, entre "
      "a rede e o chaveamento. Passo 4: resistências em série com os indutores e o capacitor "
      "atenuam o pico. Feche com a caixa da direita: barramento CC em valor constante, para "
      "manter a margem de modulação.")],
14: [("Bruno", "Figura 3.1, eixo por eixo: erro &#8594; PI &#8594; notch na ressonância do LCL "
      "&#8594; índice de modulação &#8594; PWM a 5 kHz no inversor de dois níveis."),
     ("Victor", "O filtro é o do slide anterior; o notch corta a ressonância dele. O PI segue a mesma forma canônica do PLL: &#958; = 0,707 e "
      "&#969;<sub>n</sub> = 4&#8730;2&#183;f<sub>g</sub>, a corrente acomoda em um ciclo; "
      "K<sub>p</sub> = 8f<sub>g</sub>L<sub>est</sub> e K<sub>i</sub> = "
      "32f<sub>g</sub>&#178;L<sub>est</sub>, com L<sub>est</sub> = 30,71 mH. Feche com o rodapé: "
      "são dois PIs, um sincroniza, o outro faz a corrente seguir a referência.")],
15: [("Bruno", "No modelo final, as referências fixas da primeira versão dão lugar ao bloco do "
      "Submódulo 2.10 do ONS, que lê a tensão no PCC. Na faixa normal (0,85 a 1,1 pu), reativo "
      "zero e eixo d na corrente nominal; abaixo de 0,85 pu, pede reativo pela rampa da Fig. 2.2, "
      "atingindo 1 pu em 0,5 pu, limitado a I<sub>max</sub>."),
     ("Victor", "Círculo à direita: o reativo tem prioridade e o eixo d fica só com a folga dentro "
      "de I<sub>max</sub>, reduzindo o ativo na falta e retornando ao pré-falta após a eliminação. "
      "Rodapé da direita: o ONS decide <b>quanto</b> injetar, e o SRF-PLL decide <b>em que "
      "direção</b>.")],
16: [("Victor", "Juntando tudo, Figura 4.2. Em cima a potência: inversor, LCL e Barra 2. Embaixo "
      "o controle: o PLL dá o ângulo às transformações dq, o Submódulo 2.10 dá as referências "
      "i<sub>d,ref</sub> e i<sub>q,ref</sub> em função de V<sub>PCC</sub> e as malhas comandam "
      "as chaves."),
     ("Bruno", "Uma frase: &#8220;é esse sistema que as faltas no IEEE 9 barras vão testar.&#8221;")],
}


def fala(num):
    box("fala", *[f"<b>{quem}:</b> {texto}" for quem, texto in FALAS[num]])


# =============================================================================
# PARTE I
# =============================================================================
parte("PARTE I · PowerPoint, slides 1 a 18",
      "Motivação (2-4), modelagem (5-16) e método (17-18). A modelagem é a parte mais "
      "teórica da defesa e a que mais rende pergunta: cada slide dela tem um bloco de "
      "fundamentos.")

# --- 1
slide(1, "Capa", "Abertura", "Bruno abre, Victor lista os blocos, Bruno agradece", "capa")
box("msg", "Quem somos, o título e os cinco blocos: contexto, fundamentação e modelagem, "
    "metodologia, resultados e conclusões.")
n.p("O título já diz o objeto (o SRF-PLL, não o inversor inteiro) e a condição "
    "(contingências). Orientador: Prof. Oscar Cuaresma Zevallos. Coorientador: Prof. André "
    "Guilherme Peixoto Alves, autor da tese de onde vêm o controle de corrente e parte do "
    "método de sintonia (Alves, Dias e Rolim, 2020).")
ponte("&#8220;Vamos começar pelo contexto que motivou este estudo.&#8221;")

# --- 2
slide(2, "Expansão das renováveis", "Motivação", "Bruno, Victor", "Cap. 2 (IEA 2026, ONS 2025)")
box("msg", "Solar e eólica saltaram de 5% para 17% da geração mundial em uma década; no "
    "Brasil a capacidade já passa da carga média.")
sub("Fundamento: o que a máquina síncrona faz sem ninguém mandar")
n.p("Uma máquina síncrona é uma massa girando, acoplada eletromagneticamente à rede. Ela "
    "presta três serviços por pura física:")
bul("<b>Inércia</b>: quando falta potência, a energia cinética do rotor sai sozinha e "
    "freia a queda de frequência.",
    "<b>Corrente de curto</b>: numa falta, entrega várias vezes a corrente nominal, o que "
    "sustenta a tensão e faz a proteção enxergar o defeito.",
    "<b>Tensão interna</b>: é uma fonte de tensão atrás de uma reatância; impõe tensão e "
    "ângulo à rede.")
eq(r"E_c = \dfrac{1}{2} J \omega_m^2 \qquad H = \dfrac{E_c}{S_n}\ \ [\mathrm{s}]",
   onde="J: momento de inércia; &#969;<sub>m</sub>: velocidade mecânica; S<sub>n</sub>: "
        "potência nominal. A constante H é a energia armazenada em segundos de potência "
        "nominal. Somando H&#183;S de todas as máquinas, a inércia de um sistema sai em "
        "GW&#183;s: é a unidade dos 265 GW&#183;s do slide 3.")
n.p("O inversor não tem nada disso por natureza. Ele se comporta como uma <b>fonte de "
    "corrente controlada</b>, com corrente limitada perto da nominal pelos semicondutores, "
    "e entrega o que o controle manda. Trocar máquinas por inversores transfere a "
    "sustentação da rede da física para o algoritmo, e o SRF-PLL é a peça do algoritmo que "
    "diz ao inversor onde a rede está.")
nums([["600 TWh", "crescimento da geração solar mundial em 2025, ~70% do aumento global"],
      ["5% &#8594; 17%", "participação de solar + eólica no mundo em uma década"],
      ["~30% / 35%", "União Europeia / Brasil com MMGD (na fala)"],
      ["96,8 GW", "eólica, solar e MMGD no SIN em 2025 (+279% desde 2020)"],
      ["85,8 GWmed", "carga média nacional, já superada pela capacidade acima"],
      ["800 GW", "adições renováveis no mundo em 2025, 23º recorde (só na fala)"]])
box("banca", "<b>Qual é a consequência para a rede?</b> A geração nova chega por inversores, "
    "e a síncrona, que impõe tensão e frequência pela inércia, perde espaço.")
box("cuidado", "MMGD = micro e minigeração distribuída. Capacidade (GW) não é energia "
    "(GWmed): 96,8 GW contra 85,8 GWmed mostra escala, não que a carga é atendida só por "
    "renováveis.")
ponte("se a rede depende do controle, falhas de controle deveriam aparecer em eventos "
      "reais. E aparecem.")

# --- 3
slide(3, "Eventos no mundo real", "Motivação", "Victor, Bruno, Victor, Bruno",
      "Cap. 2, §2.4 (RAP do ONS, ENTSO-E, CEN)")
box("msg", "Os três grandes blecautes recentes passaram pela geração conectada por "
    "inversores.")
sub("Os três eventos")
bul("<b>Brasil, 15/08/2023.</b> Abertura de uma linha de 500 kV pela proteção, afundamento "
    "de tensão no Nordeste, desligamentos em cascata e quatro ilhas. O ONS descartou falta "
    "de inércia (cerca de 265 GW&#183;s) e de potência de curto: foi colapso de tensão, "
    "porque o suporte dinâmico de reativos das eólicas e fotovoltaicas ficou muito aquém "
    "dos modelos. É o evento que motiva o TCC.",
    "<b>Península Ibérica, 28/04/2025.</b> Oscilação de 0,63 Hz classificada pela ENTSO-E "
    "como instabilidade guiada por conversores: usinas em fator de potência fixo, sem "
    "suporte dinâmico de tensão; mais de 2,5 GW desconectaram por sobretensão e a "
    "península perdeu o sincronismo com a Europa.",
    "<b>Chile, 25/02/2025.</b> Desligamento em 500 kV dividiu o país em duas ilhas em "
    "1,5 s; a norte colapsou por instabilidade de tensão e a centro-sul por queda de "
    "frequência; 11.066 MW de carga perdida num sistema com 73% "
    "de solar e eólica. O CEN passou a rever requisitos de controle seguidor (GFL) e "
    "formador de rede (GFM).")
sub("Fundamento: por que reativo segura a tensão")
n.p("Numa linha de transmissão, a queda de tensão entre as pontas depende da potência que "
    "passa por ela. Como a reatância X é muito maior que a resistência R, o termo do reativo "
    "manda:")
eq(r"\Delta V \approx \dfrac{R\,P + X\,Q}{V} \approx \dfrac{X\,Q}{V} \qquad (X \gg R)",
   onde="Quem injeta reativo perto da carga reduz a queda e sustenta a tensão; sem esse "
        "suporte, a tensão cai, as cargas puxam mais corrente e a queda piora: é o colapso "
        "de tensão. Por isso o diagnóstico do ONS fala em suporte dinâmico de reativos, e "
        "por isso o Submódulo 2.10 (slide 16) pede corrente reativa na falta.")
sub("Fundamento: seguidor (GFL) e formador de rede (GFM)")
n.p("O <b>seguidor de rede</b> (grid-following, o deste TCC) mede a tensão, estima o "
    "ângulo com o PLL e injeta corrente nesse ângulo: depende de uma rede que já exista e "
    "tenha tensão bem definida. O <b>formador de rede</b> (grid-forming) impõe a própria "
    "tensão e o próprio ângulo, como uma máquina. GFM está fora do escopo.")

sub("Brasil em detalhe: o que o relatório do ONS conta")
n.p("O relatório de análise de perturbação do ONS (RAP-ONS 00012/2023, 572 páginas) é a "
    "fonte do §2.4.3. A perda foi de 23.368 MW: 12.689 MW no Norte e Nordeste e 10.680 MW "
    "no Sul, Sudeste e Centro-Oeste.")
box("cuidado", "Tudo o que vem a seguir sai do relatório do ONS e <b>não está no TCC</b>: "
    "serve para entender o evento e responder à banca, não para a fala. As figuras são "
    "recortes do próprio RAP. Nos mapas do ONS, linha vermelha é 500 kV e linha verde é "
    "230 kV.")
instante("08h30 · antes", "O SIN na hora do evento: o Nordeste exportando",
         "A partir das 5h30 a geração solar do Nordeste cresceu, e às 8h a eólica do Ceará "
         "somou-se a ela. No minuto anterior ao evento, o Nordeste gerava 22.454 MW (16.317 MW "
         "de eólica e 3.211 MW de solar) para uma carga de 10.151 MW. Os cerca de 12.300 MW de "
         "sobra saíam da região por dois caminhos: para o Norte (FNEN) e para o Sudeste "
         "(FNESE). O mapa abaixo é o retrato do SIN que o ONS usa no relatório.")
figura(rap_fig("mapa_sin", 16, (60, 206, 524, 549)),
       "Mapa do SIN às 08h30, com geração e carga por região e os fluxos entre regiões com "
       "seus limites. Fonte: ONS, RAP-ONS 00012/2023, Figura 2-1 (p. 16).")
n.p("Como ler o mapa: cada região tem a sua tabela de geração e carga, e as setas são os "
    "fluxos entre regiões com o valor medido e o limite operativo. Os limites vêm de estudos "
    "que simulam a perda de linhas: é o máximo que pode passar e ainda sobreviver a uma "
    "contingência.")
n.table(["Fluxo entre regiões", "Medido", "Limite", "Situação"], [
    ["Nordeste → Norte (FNEN)", "5.879 MW", "5.800 MW",
     "79 MW acima (1,4%), resto de uma violação de ~6.000 MW às 8h02 que o ONS vinha "
     "reduzindo por redespacho"],
    ["Nordeste → Sudeste (FNESE)", "6.392 MW", "7.000 MW", "91% do limite"],
    ["Norte → Sudeste (FNS)", "528 MW", "4.000 MW", "folgado"],
    ["FNS + FNESE", "6.920 MW", "9.800 MW", "folgado"],
], [4.0, 2.0, 2.0, 6.7])
n.gap(4)
n.note("O limite de 5.800 MW do FNEN era temporário, por causa de um disjuntor em manutenção "
       "na SE São João do Piauí. O próprio ONS registra que essa pequena violação não tem "
       "relação com a perturbação nem com as suas consequências.")

instante("08h30 · Ceará", "Zoom no Ceará: a linha mais carregada da sua história",
         "Fortaleza é um centro de carga alimentado por dois caminhos paralelos: a linha de "
         "500 kV Quixadá–Fortaleza II e o tronco de 230 kV que desce por Aquiraz, Banabuiú e "
         "Milagres. Com a eólica do Ceará no máximo, a linha de 500 kV levava 1.950 MW, o "
         "maior carregamento da sua história.")
figura(rap_fig("ceara_pre", 263, (93, 238, 491, 440)),
       "Fluxos no Ceará imediatamente antes da perda da linha: 1.950 MW em Quixadá–Fortaleza "
       "II. Fonte: ONS, RAP-ONS 00012/2023, Figura 5-24 (p. 263).")

instante("T0 = 36,946 s", "A linha abre sem curto: a proteção estava ajustada abaixo do limite",
         "A linha operava com 2.375 A, e o limite normal dela é 2.390 A: estava a 99,4% do "
         "limite, mas dentro dele. Ela não deveria ter aberto. Abriu porque uma função de "
         "sobrecorrente, que só deveria existir nos primeiros instantes depois de energizar a "
         "linha (lógica SOTF), ficou ativa por erro de implementação, e com ajuste de "
         "<b>2.310 A</b>, abaixo do próprio limite da linha. Bastou a carga normal passar de "
         "2.310 A. O terminal de Quixadá abriu às 8h30min36,946s (T0) e a linha saiu de "
         "serviço sem nenhum curto-circuito.")
figura(rap_fig("origem", 14, (60, 256, 524, 489)),
       "Área de origem da perturbação: em verde, o tronco de 230 kV paralelo à linha "
       "Quixadá–Fortaleza II. Fonte: ONS, RAP-ONS 00012/2023, Figura 1-1 (p. 14).")
n.p("<b>O que era esperado.</b> Perder uma linha é uma contingência simples, das que a rede "
    "é planejada para aguentar. Essa perda era até prevista: existe um esquema (SEP 5.10.65) "
    "que, se a Quixadá–Fortaleza II cair, desliga por sobrecorrente em 5, 6 e 7 s as três "
    "linhas de 230 kV Banabuiú–Aquiraz, para não passarem do limite de emergência. E os "
    "estudos do ONS, feitos com os modelos das usinas, previam tensões adequadas depois da "
    "perda (Figura 5-28, mais abaixo). O que fez da perda de uma linha um blecaute foi a "
    "tensão.")

instante("T0 até 530 ms", "O fluxo migra para o 230 kV e a tensão desaba no Ceará",
         "Sem a linha de 500 kV, o fluxo que ia por ela passa ao tronco de 230 kV, mais fraco. "
         "Corrente maior numa linha de reatância alta significa mais queda de tensão "
         "(&#916;V &#8776; XQ/V) e mais consumo de reativo pela própria linha. Quem deveria "
         "sustentar a tensão eram as eólicas e solares da região, injetando reativo. Em meio "
         "segundo, a tensão no Ceará estava pela metade.")
figura(rap_fig("tensoes530", 24, (60, 140, 524, 403)),
       "Fluxos e tensões em T0 + 530 ms, com a linha Quixadá–Fortaleza II marcada com X. "
       "Fonte: ONS, RAP-ONS 00012/2023, Figura 3-4 (p. 24).")
tab(["Barra (T0 + 530 ms)", "Tensão", "Barra (T0 + 530 ms)", "Tensão"], [
    ["Icó 230 kV", "0,47 pu", "Açu III 500 kV", "0,57 pu"],
    ["Banabuiú 230 kV", "0,52 pu", "Campo Grande III", "0,57 pu"],
    ["Milagres 230 kV", "0,54 pu", "Boa Esperança", "0,68 pu"],
    ["Milagres II", "0,56 pu", "Presidente Dutra", "0,92 pu"],
], [4.2, 3.15, 4.2, 3.15])
n.p("Para ter escala: no Submódulo 2.10, abaixo de 0,85 pu a usina já tem de injetar "
    "corrente reativa adicional (slide 16), e 0,5 pu fica no meio da rampa. Barras de 230 kV "
    "a 0,5 pu sem curto nenhum, meio segundo depois de uma única linha abrir, é a medida da "
    "gravidade.")

instante("T0 + 530 ms", "Presidente Dutra: a proteção vê uma oscilação e separa Norte e Nordeste",
         "Com a tensão baixa, a impedância vista pelo relé no terminal de Presidente Dutra da "
         "linha Presidente Dutra–Boa Esperança (500 kV) foi caindo devagar, a 55 &#937;/s. O "
         "relé distingue curto de oscilação pela velocidade: abaixo de 1.500 &#937;/s, ele "
         "entende oscilação de potência. Ao chegar à característica ajustada, a proteção de "
         "perda de sincronismo disparou e, pelo esquema ECE 4.14.11, levou junto as linhas "
         "para Teresina (C1 e C2) e Imperatriz (C2). A corrente estava em 2.153 A, 8% acima do "
         "limite de longa duração de 2.000 A. Com isso, a interligação Norte–Nordeste por "
         "Presidente Dutra se abriu.")

instante("T0 + 570 ms a 1,8 s", "O tronco de 230 kV abre pela proteção de distância",
         "Quarenta milissegundos depois, a proteção de distância abriu Milagres–Icó (230 kV) "
         "com <b>0,54 pu e 897 A, 11% acima do limite de 810 A</b>. A linha levava 177 MW e "
         "absorvia 66 Mvar. Para o relé, tensão baixa e corrente alta é cara de curto. Seguem "
         "Aquiraz–Banabuiú (608 ms), São João do Piauí–Ribeiro Gonçalves C2 no 500 kV "
         "(609 ms), Milagres–Banabuiú C3 (669 ms) e C1 (1.773 ms), e o tronco de 230 kV entre "
         "Milagres e Fortaleza fica aberto.")
figura(rap_fig("tronco230", 31, (88, 164, 494, 368)),
       "Sequência de aberturas no tronco de 230 kV entre Milagres e Fortaleza, com o instante "
       "e a proteção de cada uma. Fonte: ONS, RAP-ONS 00012/2023, Figura 3-12 (p. 31).")
n.note("O ONS observa que essas aberturas só anteciparam o que o SEP 5.10.65 faria em 5 a 7 s "
       "pela sobrecarga. O problema não foi a proteção de distância errar, e sim a tensão "
       "estar baixa a ponto de a carga parecer curto.")

instante("~T0 + 1,8 s", "Perda de sincronismo: centros elétricos no tronco de 500 kV",
         "Com tantas linhas abertas, o Nordeste ficou ligado ao resto do SIN por poucos "
         "caminhos, que passaram a carregar mais. O ângulo entre as áreas abriu e começou a "
         "oscilação de potência. Quando duas áreas ficam quase em oposição de fase, aparece "
         "num ponto da linha entre elas uma tensão quase nula, o <b>centro elétrico</b>, e os "
         "relés perto dele veem algo parecido com um curto. Os centros se formaram quase ao "
         "mesmo tempo em várias linhas de 500 kV, e as proteções de perda de sincronismo foram "
         "abrindo uma a uma (Poções III–Padre Paraíso a T0 + 1,788 s e 1,825 s).")
figura(rap_fig("centros", 43, (123, 244, 461, 483)),
       "Centros elétricos identificados por volta de 8h30min38,730s. Fonte: ONS, RAP-ONS "
       "00012/2023, Figura 3-27 (p. 43).", largura=7.0)

instante("T0 + 2,642 s", "O Norte se separa do SIN, levando parte do Ceará e do Piauí",
         "A abertura de Serra da Mesa–Gurupi (C1 e C2, pela proteção de perda de "
         "sincronismo), depois de Gurupi–Peixe II e do tronco Gurupi–Miracema, isolou o "
         "Subsistema Norte do restante do SIN. A ilha do Norte levou junto parte do Ceará, do "
         "Piauí e do Rio Grande do Norte. Faltando geração, a frequência caiu, o corte de "
         "carga atuou, geradores desligaram, e a ilha colapsou.")
figura(rap_fig("sep_norte", 87, (97, 510, 487, 710)),
       "Momento da separação do Subsistema Norte; em amarelo, os desligamentos do tronco que "
       "levaram a ela. Fonte: ONS, RAP-ONS 00012/2023, Figura 3-77 (p. 87).")

instante("T0 + 5 s", "A linha de origem volta e cai de novo",
         "Às 8h30min41,976s o religamento automático fechou a Quixadá–Fortaleza II. A função "
         "de sobrecorrente esquecida continuava ativa: a corrente chegou a 2.600 A, contra o "
         "ajuste de 2.310 A e o limite de 2.390 A, e a linha abriu de novo 153 ms depois. Uma "
         "falha no algoritmo de religamento ainda fechou o segundo disjuntor (T0 + 5,541 s) "
         "sem verificar o sincronismo.")

instante("3,5 s a 19,8 s", "As outras ilhas",
         "Acre/Rondônia se separa por volta de 3,5 s, com sobrefrequência e sobretensão, e "
         "colapsa. Parte do Nordeste vira ilha por volta de 19,8 s e, apesar de "
         "desligamentos por sobretensão, estabiliza. O Sul, o Sudeste, o Centro-Oeste e o "
         "sudoeste da Bahia ficam juntos e se equilibram com o corte de carga. A perda total "
         "foi de 23.368 MW: 12.689 MW no Norte e Nordeste e 10.680 MW no Sul, Sudeste e "
         "Centro-Oeste.")

instante("Esperado × real", "O gráfico que explica o relatório inteiro",
         "Depois do evento, o ONS simulou só a abertura da Quixadá–Fortaleza II, partindo do "
         "estado real da rede naquele minuto. Com os modelos oficiais das usinas (curva azul), "
         "a tensão em Açu III, o ponto mais próximo da linha, afunda por um instante e "
         "<b>volta a cerca de 1 pu</b>: não aconteceria nada. A medição de campo (curva "
         "vermelha) cai continuamente para ~0,7 pu em 0,4 s, ~0,6 pu em 0,6 s e ~0,43 pu em "
         "0,8 s.")
figura(rap_fig("acu", 268, (65, 172, 519, 400)),
       "Tensão em Açu III 500 kV: medição de campo (vermelho), simulação com a base oficial "
       "(azul) e com a base ajustada (verde). Fonte: ONS, RAP-ONS 00012/2023, Figura 5-28 "
       "(p. 268).")
n.p("Para a simulação reproduzir o campo (curva verde), o ONS teve de alterar os modelos das "
    "eólicas e solares em dois pontos: o controle de reativo da usina (PPC) e a "
    "<b>lógica de injeção de corrente reativa sob falta dos inversores</b>. Com isso a "
    "simulação passou a reproduzir até a atuação da proteção em Presidente Dutra. É a prova "
    "do §7.10: a rede caiu porque as usinas entregaram menos reativo do que o modelo "
    "prometia. E injeção de corrente reativa sob falta é exatamente o requisito do "
    "Submódulo 2.10 que o TCC verifica, e que depende do ângulo estimado pelo PLL.")

n.table(["Grandeza", "Real", "Limite ou esperado", "Leitura"], [
    ["Corrente na Quixadá–Fortaleza II", "2.375 A", "limite 2.390 A",
     "99,4% do limite: carregada, mas legal"],
    ["Ajuste da sobrecorrente esquecida", "2.310 A", "acima do carregamento máximo da linha",
     "ajuste 3% abaixo do limite: erro"],
    ["Fluxo Nordeste → Norte", "5.879 MW", "5.800 MW", "1,4% acima, sem relação com o evento"],
    ["Tensão em Açu III (~0,6 s)", "~0,6 pu", "~1,0 pu (simulação oficial)",
     "o modelo das usinas não representava o campo"],
    ["Tensão em Banabuiú e Icó (530 ms)", "0,52 e 0,47 pu", "~1 pu em operação",
     "metade da tensão sem curto"],
    ["Corrente em Pres. Dutra–Boa Esperança", "2.153 A", "2.000 A", "8% acima"],
    ["Velocidade da impedância (P. Dutra)", "55 &#937;/s", "1.500 &#937;/s separa curto "
     "de oscilação", "lenta: lida como oscilação, abre a interligação"],
    ["Corrente em Milagres–Icó", "897 A a 0,54 pu", "810 A", "11% acima: parece curto"],
    ["Religamento da linha de origem", "2.600 A", "2.390 A", "cai de novo pelo mesmo erro"],
], [4.4, 2.6, 3.4, 4.3])
n.gap(8)
n.p("<b>Fundamento: as três proteções da cascata.</b>")
bul("<b>Fechamento sob falta (SOTF):</b> fica armada no instante em que a linha é "
    "energizada e dispara sem retardo se houver sinal de curto, para o caso de fechar o "
    "disjuntor sobre um aterramento esquecido. Em 15/08 uma sobrecorrente ligada a "
    "ela ficou ativa por erro, ajustada abaixo do limite da linha, e abriu a linha com "
    "carga normal: foi uma atuação acidental, e é o gatilho.",
    "<b>Distância:</b> mede a impedância vista pelo relé, Z = V/I, e dispara se ela cair "
    "dentro da zona ajustada. Num curto, V cai e I sobe, e Z fica pequena. O problema é que "
    "afundamento com sobrecarga faz a mesma coisa: com 0,54 pu e 897 A, a linha Milagres–Icó "
    "pareceu estar em falta sem estar.",
    "<b>Perda de sincronismo:</b> acompanha a trajetória da impedância quando o ângulo entre "
    "duas áreas abre demais e separa as áreas antes que oscilem uma contra a outra. Ela "
    "abriu o tronco de 500 kV que ligava o Norte ao Nordeste.")
eq(r"Z_{ap} = \dfrac{V}{I} \quad\downarrow \quad \mathrm{se}\ V\downarrow\ \mathrm{e}\ "
   r"I\uparrow \quad \mathrm{(curto\ ou\ afundamento\ com\ sobrecarga)}",
   onde="É por isso que o colapso de tensão se propaga pela proteção: cada linha que abre "
        "joga o fluxo nas vizinhas, que ficam com tensão menor e corrente maior e passam a "
        "parecer em falta.")
tab(["Ilha", "Separa em", "O que houve", "Desfecho"], [
    ["Norte", "~2,6 s", "Subfrequência; corte de carga atua, geradores desligam",
     "Colapso"],
    ["Acre/Rondônia", "~3,5 s", "Sobrefrequência e sobretensão", "Colapso"],
    ["Parte do Nordeste", "~19,8 s", "Sobrefrequência e sobretensão; desligamentos",
     "Estabiliza"],
    ["Sul/SE/CO e sudoeste da BA", "—", "Corte de carga restabelece o equilíbrio",
     "Permanece estável"],
], [3.6, 2.2, 6.3, 2.6])
n.p("<b>O fator determinante.</b> O ONS conclui que \"o desempenho dos controles em campo, "
    "de usinas eólicas e fotovoltaicas, em especial no que tange à capacidade de suporte "
    "dinâmico de potência reativa, foi muito aquém dos modelos matemáticos fornecidos pelos "
    "agentes\". Cada usina entrega ao ONS um modelo do seu controle, e o ONS usa esses "
    "modelos para decidir quanto a rede pode transportar com segurança. Se no afundamento "
    "a usina injeta menos reativo do que o modelo promete, a tensão cai mais do que o "
    "estudo previa, e um cenário que parecia seguro deixa de ser. O relatório registra a "
    "divergência, mas não aponta o mecanismo dentro do controle que a causou. É nesse "
    "ponto que o TCC entra: o inversor só injeta a corrente reativa certa se o PLL souber "
    "onde está a tensão, e é o PLL sob afundamento que o trabalho simula.")
n.p("<b>O que o ONS descarta.</b>")
bul("<b>Inércia:</b> o SIN tinha cerca de 265 GW&#183;s para uns 73 GW de carga, "
    "proporção acima da de vários sistemas no mundo. O colapso foi de tensão, não de "
    "frequência, e mais inércia não o teria evitado.",
    "<b>Potência de curto-circuito:</b> adequada a todos os critérios dos Procedimentos de "
    "Rede. Mais máquinas síncronas na região não dariam margem para esse fenômeno; o risco "
    "continuaria parecido enquanto persistisse a diferença entre modelo e campo.",
    "<b>Oscilação de potência como causa:</b> não houve nos primeiros instantes; a abertura "
    "angular entre áreas foi consequência da queda de tensão.")
box("alem", "<b>Referência acadêmica sobre o evento.</b> Xiong et al. (2025), citado na "
    "Motivação por indicação do orientador, aponta como uma das causas a falha das "
    "proteções de oscilação de potência baseadas em impedância numa área com muita geração "
    "seguidora de rede: essas proteções foram pensadas para máquinas síncronas, e o "
    "inversor oscila de outro jeito. É também a fonte dos dados das linhas do modelo. O "
    "artigo não traz MW nem porcentagem de carga perdida; esses números são do RAP.",
    "<b>Recomposição:</b> partida autônoma em Tucuruí, Balbina, Coaracy Nunes, Estreito e "
    "Samuel, com várias tentativas falhas; o ONS autorizou a recomposição total das cargas "
    "às 14h49.")
box("prova", "<b>Se não faltou inércia, então o que faltou?</b> Suporte dinâmico de reativo "
    "das eólicas e fotovoltaicas no afundamento, abaixo do que os modelos prometiam.",
    "<b>O PLL causou o blecaute?</b> O ONS não diz isso, nem o TCC. O relatório mostra que "
    "o controle das usinas respondeu pior que o modelo e não aponta o mecanismo; o TCC "
    "estuda um elo necessário dessa resposta, o sincronismo sob afundamento e assimetria.",
    "<b>Não foi uma falta?</b> Não: o gatilho foi uma abertura de linha sem curto. O que o "
    "inversor viu foi um afundamento de tensão, e é isso que as faltas simuladas reproduzem "
    "no ponto de conexão.")

sub("Península Ibérica em detalhe: a tensão que subiu demais")
n.p("Era um dia de primavera com muita geração solar no sudoeste da Espanha (cerca de "
    "18,7 GW), bem acima do consumo da região, e a Espanha exportava 5 GW. A energia "
    "atravessava longas distâncias e a tensão da rede de 400 kV já oscilava desde as 9h, "
    "chegando perto do limite de 435 kV às 10h30. Diferente do Brasil, o problema não foi "
    "tensão baixa: foi <b>tensão alta</b>, e o desligamento das usinas por sobretensão.")
n.table(["Hora (local)", "O que aconteceu"], [  # pode partir: evita vão no fim da página
    ["12h03–12h08", "Oscilação de 0,63 Hz, só na península, imposta por uma usina "
                    "inversorizada (oscilação forçada, guiada por conversor)"],
    ["12h19–12h22", "Oscilação de 0,2 Hz entre áreas: a Ibéria oscila contra o centro da "
                    "Europa"],
    ["12h20–12h30", "As medidas contra as oscilações (religar linhas, reduzir a exportação "
                    "para a França) funcionam, mas sobem a tensão; reatores desligados nas "
                    "oscilações não voltam"],
    ["12h32min57s", "Primeiro desligamento por sobretensão: transformador em Granada"],
    ["12h33min16s–21s", "Badajoz e cascata de eólicas e solares: mais de 2,5 GW perdidos; "
                        "a frequência cai"],
    ["12h33min19s–24s", "Perda de sincronismo com a Europa; abrem as ligações com França e "
                        "Marrocos; colapso de Espanha e Portugal"],
], [3.3, 11.4])
n.gap(8)
n.p("<b>O mecanismo central: fator de potência fixo.</b> As renováveis espanholas operavam "
    "absorvendo reativo numa proporção fixa da potência ativa, e não por tensão medida:")
eq(r"Q = P\,\tan\varphi \quad\rightarrow\quad \Delta Q = \Delta P\,\tan\varphi",
   onde="&#966;: ângulo do fator de potência, fixo por regulamento (0,98 indutivo a 0,98 "
        "capacitivo). Quando o despacho reduz P, a absorção de reativo cai na mesma "
        "proporção, e pela relação &#916;V &#8776; XQ/V acima a tensão sobe. E nada "
        "reage à tensão, porque Q não depende dela.")
n.p("Daí nasce um laço de realimentação positiva:")
bul("o despacho reduz a potência ativa das renováveis (cerca de 0,4 a 0,5 GW às 12h30);",
    "a absorção de reativo cai junto e a tensão sobe;",
    "a proteção de sobretensão desliga usinas, algumas com ajuste fora do exigido e sem "
    "temporização;",
    "a usina desligada deixa de absorver reativo e a tensão sobe mais, até a cascata.")
n.p("Os reatores de barra, que poderiam segurar a tensão, eram manobrados à mão, e a subida "
    "levou cerca de um minuto, rápida demais para uma decisão humana. Em Portugal, ao "
    "contrário, as renováveis recebem em tempo real uma referência de tensão do operador.")
n.p("<b>O que é a oscilação forçada de 0,63 Hz.</b> Uma rede tem frequências próprias de "
    "oscilação (modos naturais), como uma corda tem suas notas. A de 0,63 Hz não era uma "
    "delas: não aparecia no modelo da rede nem nos meses anteriores. Ela era <b>imposta</b> "
    "por um equipamento que injetava potência oscilando. A ENTSO-E rastreou a fonte até uma "
    "usina inversorizada de grande porte na região de Badajoz, anterior ao código de rede "
    "europeu atual e operando com potência limitada. Quando a usina subiu a potência, a "
    "oscilação diminuiu. Ela ainda excitou o modo de 0,2 Hz entre áreas, que tinha "
    "amortecimento muito baixo. Por isso o relatório fala em <b>instabilidade guiada por "
    "conversor</b>: a malha de controle de um conversor foi a fonte.")
box("alem", "<b>Inércia teria salvado?</b> Não. A ENTSO-E testou: mesmo com inércia bem "
    "maior, a perda de sincronismo não teria sido evitada, porque a cascata derrubou o "
    "torque sincronizante rápido demais. Em simulação, mais margem de reativo teria evitado "
    "o colapso. A conclusão do painel é que o fenômeno central foi a falta de controle de "
    "tensão. Isso reforça o argumento do TCC: a sustentação da rede passou para o controle.")

sub("Chile em detalhe: uma proteção, duas ilhas, dois colapsos")
n.p("O sistema chileno é longo e estreito: cerca de 3.100 km de Arica a Chiloé, com o norte "
    "exportando para o centro-sul. No instante do evento, 1.800 MW (cerca de 90% da "
    "capacidade) passavam por uma única linha dupla de 500 kV, Nueva Maitencillo–Nueva Pan "
    "de Azúcar, e 73% da geração era solar e eólica.")
n.table(["Hora (local)", "O que aconteceu"], [
    ["13h35", "A transmissora desabilita a comunicação da proteção diferencial de um dos "
              "circuitos; a linha segue protegida pelas proteções de retaguarda"],
    ["15h13", "Reinicia o controlador de comunicações sem avisar nem pedir autorização ao "
              "operador (CEN)"],
    ["15h15–15h16", "Na ressincronização, a proteção dispara indevidamente os dois "
                    "circuitos de 500&#160;kV, risco previsto no manual do fabricante"],
    ["+1,5 s", "O 220 kV em paralelo fica sobrecarregado e abre: o país se divide em duas "
               "ilhas"],
    ["+4 s / +4 min", "A ilha centro-sul colapsa por frequência em segundos; a ilha norte "
                      "resiste cerca de 4 min e colapsa por tensão"],
], [3.3, 11.4])
n.gap(8)
n.p("<b>Por que a proteção disparou sozinha.</b> A proteção diferencial de linha compara a "
    "corrente que entra por uma ponta com a que sai pela outra. Em operação normal, a soma "
    "das correntes que entram pelas duas pontas é nula; numa falta dentro da linha, não é:")
eq(r"I_{dif} = |\,\bar I_A + \bar I_B\,| \approx 0 \quad \mathrm{(sem\ falta)}",
   onde="As duas pontas estão a centenas de quilômetros, e as amostras de corrente precisam "
        "estar alinhadas no tempo pela comunicação. Um desalinhamento de &#916;t gira uma "
        "corrente em relação à outra de &#969;&#916;t, e a diferença aparente cresce com a "
        "corrente: com 1.800 MW passando, um erro pequeno de sincronismo parece falta "
        "interna e a proteção abre.")
n.p("<b>Por que cada ilha caiu de um jeito.</b>")
bul("<b>Centro-sul</b> (70% da carga): ficou com déficit de cerca de 1.800 MW, uns 25% da "
    "demanda. Faltando potência, a energia sai da rotação das máquinas e a frequência cai. "
    "O corte automático de carga atuou, mas cerca de 230 MW não foram cortados como "
    "previsto; a frequência firmou em 48,5 Hz, voltou a cair e, ao passar de 47,5 Hz, mais "
    "geração saiu e veio o colapso.",
    "<b>Norte</b> (30% da carga): ficou com sobra de geração. O desligamento automático de "
    "geração segurou a ilha por cerca de 4 min, mas a tensão subiu: as renováveis não "
    "faziam controle dinâmico de reativo e um equipamento de compensação foi perdido. "
    "Linha longa com pouca carga ainda gera reativo pela própria capacitância (efeito "
    "Ferranti), o que empurra a tensão para cima.")
n.p("<b>Por que está no trabalho, se o gatilho foi humano.</b> O disparo foi erro de "
    "proteção, mas a ilha norte caiu pela mesma deficiência do Brasil (falta de suporte "
    "dinâmico de reativo das renováveis), e a resposta do operador foi uma das 14 medidas "
    "corretivas: publicar guia e proposta de norma para inversores <b>GFM e GFL</b>, para "
    "que as usinas renováveis prestem suporte à rede. O relatório do CEN também só registra "
    "se cada proteção atuou ou não; o comportamento interno do sincronismo dos inversores "
    "não aparece, e é esse comportamento que o TCC simula.")

sub("Os três eventos lado a lado")
tab(["", "Brasil 2023", "Ibéria 2025", "Chile 2025"], [
    ["Gatilho", "Proteção abre linha de 500 kV", "Subida de tensão",
     "Disparo indevido de proteção diferencial"],
    ["Problema de tensão", "Afundamento, colapso de tensão", "Sobretensão em cascata",
     "Sobretensão na ilha norte"],
    ["Papel dos inversores", "Suporte de reativo aquém dos modelos",
     "Fator de potência fixo; fonte da 0,63 Hz", "Sem controle dinâmico de reativo"],
    ["Resultado", "23.368 MW; quatro ilhas", "Espanha e Portugal inteiros",
     "11.066 MW; país inteiro"],
], [3.2, 3.8, 3.8, 3.9])
box("cuidado", "O TCC (§2.4.1 e §2.4.2) traz só o essencial: escala máxima, subida de "
    "tensão, cascata por sobretensão, 0,63 Hz guiada por conversor, fator de potência fixo, "
    "mais de 2,5 GW; e no Chile 11.066 MW, 73%, intervenção não autorizada na proteção "
    "diferencial, duas ilhas em 1,5 s, ilha norte por tensão, centro-sul por frequência, "
    "revisão de requisitos GFM/GFL. Horários, Badajoz, Granada, Portugal e o mecanismo "
    "detalhado vêm dos relatórios (ENTSO-E 2026, CEN 2025): use para responder, não na fala.",
    "Duas simplificações do slide que a banca pode notar: no Chile, o slide diz que o "
    "desligamento \"isolou o norte\", mas foram duas ilhas e a centro-sul caiu por "
    "frequência; e na Ibéria o problema foi sobretensão, não afundamento, embora o rodapé "
    "fale em falha \"no afundamento\". Se perguntarem: o elo comum é a resposta de tensão "
    "e de sincronismo do controle dos inversores durante o transitório.")
box("prova", "<b>O apagão ibérico foi falta de inércia?</b> Não: a ENTSO-E mostrou que mais "
    "inércia não evitaria a perda de sincronismo; faltou controle de tensão.",
    "<b>O que é instabilidade guiada por conversor?</b> Categoria da classificação "
    "estendida de estabilidade (Cap. 2): instabilidade causada pela interação das malhas "
    "de controle dos conversores, como o PLL e o controle de corrente, com a rede.",
    "<b>Se o Chile foi erro humano, por que citar?</b> Pelo modo como a perturbação se "
    "propagou (ilha norte por tensão) e pela resposta regulatória, que mirou o controle dos "
    "inversores (GFM e GFL).")
nums([["23.368 MW", "carga perdida no Brasil, 34,5% da nacional (§2.4.3)"],
      ["265 GW&#183;s", "inércia do SIN no evento: não faltou inércia"],
      ["> 2,5 GW; 0,63 Hz", "Ibéria: desconexão por sobretensão; oscilação antes do colapso"],
      ["11.066 MW; 73%", "Chile: carga perdida; participação solar e eólica"]])
box("banca", "<b>O que une os três eventos?</b> Perturbações ordinárias viraram blecautes "
    "porque o controle e o sincronismo dos inversores falharam no afundamento.")
box("cuidado", "A introdução do TCC traz 22.547 MW (31%) e a §2.4.3 traz 23.368 MW (34,5%). "
    "O deck usa 23.368 MW, do RAP do ONS (defesa_qa.pdf, pergunta 6).")
ponte("por que o sincronismo falha justamente no afundamento?")

# --- 4
slide(4, "Problema e objetivos", "Motivação", "Bruno, Victor, Bruno, Victor", "Cap. 1")
box("msg", "O SRF-PLL depende de uma tensão limpa, justamente o que a falta na rede destrói.")
sub("Fundamento: os três estragos da falta na tensão medida")
bul("<b>Afundamento</b>: a amplitude cai. Como a amplitude multiplica o ganho do laço do "
    "PLL (slide 7), o laço fica mais lento e menos amortecido.",
    "<b>Salto de fase</b>: o ângulo da tensão muda de repente, e o PLL precisa correr atrás.",
    "<b>Assimetria</b>: a falta desequilibrada cria sequência negativa, que no referencial "
    "dq vira uma oscilação de 120 Hz em v<sub>q</sub>, e v<sub>q</sub> é exatamente o sinal "
    "de erro do PLL.")
sub("Fundamento: componentes simétricas (Fortescue)")
n.p("Qualquer conjunto trifásico desequilibrado se decompõe em três conjuntos "
    "equilibrados: sequência positiva (gira no sentido da rede), negativa (gira ao "
    "contrário) e zero (as três fases iguais). Uma falta trifásica só reduz a positiva; "
    "faltas mono e bifásicas criam negativa.")
eq(r"v_{abc} = v^{+} + v^{-} + v^{0}")
n.p("Vista por eixos que giram a +&#969;, a positiva fica parada e a negativa gira a "
    "&#8722;2&#969;. Por isso, com uma componente negativa de amplitude V<sup>&#8722;</sup>, "
    "aparece em dq uma parcela oscilando a 2&#969; = 120 Hz:")
eq(r"v_d = V^{+} + V^{-}\cos(2\omega t + \phi) \qquad v_q = -V^{-}\sin(2\omega t + \phi)",
   onde="Forma de Yazdani e Iravani (2010), §8.3.5; o sinal e a fase &#966; dependem da "
        "convenção. O PLL lê esse v<sub>q</sub> como se fosse erro de ângulo.")
sub("Cadeia causal da figura e objetivos")
n.p("Tensão degradada &#8594; erro de ângulo &#8594; correntes d e q orientadas no lugar "
    "errado &#8594; o desacoplamento entre P e Q se perde &#8594; o inversor não entrega o "
    "suporte de reativo que o Submódulo 2.10 pede. <b>Objetivo geral:</b> analisar a "
    "dinâmica, a sensibilidade à sintonia e a robustez do SRF-PLL de um inversor de 100 MW "
    "sob contingências no IEEE 9 barras. <b>Específicos:</b> modelar no Simulink, comparar "
    "sintonia nominal e inadequada sob faltas simétricas e assimétricas, verificar o suporte "
    "de subtensão (ONS).")
box("banca", "<b>Qual é a pergunta central?</b> Como a sintonia do PI do SRF-PLL define a "
    "fronteira entre manter o suporte de tensão e perder o sincronismo durante a falta?")
box("cuidado", "As notas falam em sobrecorrentes; o TCC conclui que elas não se manifestam "
    "(defesa_qa.pdf, pergunta 2). Não puxe o assunto.")
ponte("para responder, primeiro o modelo: como a usina se liga à rede.")

# --- 5
slide(5, "Fonte renovável", "Modelagem", "Victor, Bruno", "Fig. 3.2, §3.2, §4.1, §4.3.1")
box("msg", "A usina fotovoltaica ou eólica se conecta à rede por um inversor seguidor de rede.")
fala(5)
sub("Fundamento: a cadeia da figura")
bul("<b>Fonte primária</b>: um barramento CC ideal (tensão constante).",
    "<b>Conversor</b>: VSI (inversor fonte de tensão) trifásico de dois níveis; as chaves "
    "ligam cada fase ao + ou ao &#8722; do barramento, e o PWM faz a média dessa tensão "
    "seguir a referência senoidal.",
    "<b>Filtro e PCC</b>: o filtro LCL tira o chaveamento da corrente; o PCC (ponto de "
    "acoplamento comum) é a Barra 2.",
    "<b>Controle</b>: mede a tensão no PCC, o SRF-PLL (em laranja) estima o ângulo e as "
    "malhas de corrente decidem o chaveamento.")
n.p("<b>Por que CC ideal, sem elo CC e sem MPPT?</b> Para isolar o fenômeno estudado. O "
    "elo CC e o rastreamento de máxima potência têm dinâmicas próprias que se misturariam "
    "ao sincronismo. Com a fonte ideal, tudo o que se vê na falta vem da rede CA, do PLL e "
    "da malha de corrente.")
box("banca", "<b>Como o inversor segue a rede?</b> O controle trabalha em dq, e o SRF-PLL "
    "rastreia o ângulo da tensão no PCC.")
ponte("&#8220;trabalha em dq&#8221; pede a transformada de Park.")

# --- 6
slide(6, "Transformada de Park", "Modelagem", "Victor, Bruno", "Eqs. (3.4)-(3.7), §3.1.2")
box("msg", "Girando com a rede, a transformada de Park torna constantes as grandezas "
    "trifásicas.")
fala(6)
sub("Fundamento: a transformação")
n.p("As três fases são projetadas em dois eixos, d e q, que giram no ângulo &#952;. No TCC "
    "a transformação é invariante em amplitude (fator 2/3): a amplitude de fase reaparece "
    "inteira em dq.")
eq(r"v_d = \frac{2}{3}\left[v_a\cos\theta + v_b\cos\left(\theta-\frac{2\pi}{3}\right)"
   r" + v_c\cos\left(\theta+\frac{2\pi}{3}\right)\right]")
eq(r"v_q = -\frac{2}{3}\left[v_a\sin\theta + v_b\sin\left(\theta-\frac{2\pi}{3}\right)"
   r" + v_c\sin\left(\theta+\frac{2\pi}{3}\right)\right]",
   onde="Forma em cosseno; o TCC (Eqs. 3.5 a 3.7) pode usar outra convenção de seno, "
        "cosseno ou sinal. O resultado abaixo é o mesmo em qualquer uma.")
sub("Fundamento: as duas linhas embaixo da matriz")
n.p("A matriz é a transformação geral, com um &#952; qualquer. No inversor, quem fornece "
    "&#952; é o PLL, então &#952; = &#952;<sub>PLL</sub>. A rede tem o seu próprio ângulo, "
    "&#952;<sub>ref</sub>, que ninguém mede direto. A linha embaixo da matriz mostra o que "
    "sai da Park nessa situação. A conta tem três passos.")
n.p("<b>1. Tensões da rede.</b> Equilibradas, de amplitude de fase V<sub>m</sub>, como no "
    "TCC (§3.4, logo antes da Equação 3.10):")
eq(r"v_a = V_m\cos\theta_{ref},\quad v_b = V_m\cos(\theta_{ref} - 2\pi/3),\quad "
   r"v_c = V_m\cos(\theta_{ref} + 2\pi/3)")
n.p("<b>2. Produto de cossenos.</b> Na linha de v<sub>d</sub>, cada fase entra como "
    "cos(&#952;<sub>ref</sub> &#8722; k&#183;2&#960;/3)&#183;cos(&#952; &#8722; k&#183;2&#960;/3). "
    "A identidade cos A cos B = &#189;[cos(A &#8722; B) + cos(A + B)] separa cada produto em "
    "duas parcelas:")
bul("<b>cos(A &#8722; B)</b>: os deslocamentos de 2&#960;/3 se cancelam e sobra "
    "cos(&#952;<sub>ref</sub> &#8722; &#952;) <b>igual nas três fases</b>. Somadas, dão "
    "3&#183;&#189; = 3/2.",
    "<b>cos(A + B)</b>: os deslocamentos se somam (0, &#8722;4&#960;/3, +4&#960;/3), são três "
    "cossenos defasados de 120&#176; e <b>a soma é zero</b>. É essa parcela que gira a 2&#969; "
    "e some quando a tensão é equilibrada.")
n.p("Na linha de v<sub>q</sub> é o mesmo, com cos A sen B no lugar, e sobra o seno da diferença.")
n.p("<b>3. O 2/3 cancela o 3/2.</b> Por isso a transformação é chamada de invariante em "
    "amplitude:")
eq(r"v_d = \frac{2}{3}\cdot\frac{3}{2}\,V_m\cos(\theta_{ref} - \theta_{PLL}) "
   r"= V_m\cos(\theta_{ref} - \theta_{PLL})")
eq(r"v_q = \frac{2}{3}\cdot\frac{3}{2}\,V_m\,\mathrm{sen}(\theta_{ref} - \theta_{PLL}) "
   r"= V_m\,\mathrm{sen}(\theta_{ref} - \theta_{PLL})",
   onde="A linha de v<sub>q</sub> é a do TCC (§3.4, antes da 3.10). A de v<sub>d</sub> sai da "
        "mesma conta, mas o TCC não a escreve: se a banca pedir a fonte, é a Equação (3.5) "
        "com essa substituição.")
tab(["Situação", "v<sub>d</sub>", "v<sub>q</sub>", "Leitura"], [
    ["&#952;<sub>PLL</sub> = &#952;<sub>ref</sub> (travado)", "V<sub>m</sub>", "0",
     "amplitude inteira em d: as senoides viraram constantes"],
    ["erro pequeno &#916;&#952;", "&#8776; V<sub>m</sub>", "&#8776; V<sub>m</sub>&#183;&#916;&#952;",
     "v<sub>q</sub> mede o erro de ângulo (slides 7 e 10)"],
    ["erro de 90&#176;", "0", "V<sub>m</sub>", "o vetor caiu inteiro no eixo q"],
], [4.2, 2.0, 2.6, 6.2])
box("base", "O v<sub>d</sub> diz <b>quanto</b> de tensão há e o v<sub>q</sub> diz <b>quanto o "
    "ângulo está errado</b>. O PLL usa só o v<sub>q</sub>: leva ele a zero e, com isso, alinha o "
    "eixo d com a tensão da rede.")
box("alem", "<b>Por que só v<sub>q</sub>, e não v<sub>d</sub>, vai para o PI?</b> Perto do "
    "travamento, o cosseno é quase 1 e varia pouco com o erro, enquanto o seno varia "
    "linearmente. Por isso o v<sub>q</sub> é o sinal que carrega o erro de fase.")
sub("Fundamento: por que o controle quer dq")
n.p("Um PI zera o erro em regime de um sinal <b>constante</b>: a parte integral acumula até "
    "o erro sumir. Para uma senoide, o integrador nunca para de oscilar e sempre sobra erro "
    "de amplitude e de fase. Em dq, o controle de corrente e o PLL viram problemas de sinal "
    "contínuo, e o PI resolve.")
box("alem", "O que <b>não</b> gira a +&#969; aparece oscilando em dq. Sequência negativa "
    "(gira a &#8722;&#969;): aparece a 2&#969; = 120 Hz. Componente contínua nas fases (o "
    "deslocamento transitório da corrente de curto): aparece a &#969; = 60 Hz. Harmônicos: "
    "o 5º (sequência negativa) e o 7º (positiva) aparecem os dois a 6&#969; = 360 Hz. "
    "Isso explica o pico em 60 Hz de algumas curvas no espectro do capítulo 4 do painel.")
box("banca", "<b>E o ângulo &#952;?</b> A transformação só vale se &#952; for o ângulo real "
    "da tensão. Quem estima &#952; é o PLL.")
ponte("como o PLL encontra &#952;.")

# --- 7
slide(7, "Estrutura do SRF-PLL", "Modelagem", "Victor, Bruno", "Fig. 4.3, §3.4, Eqs. (3.10)-(3.19)")
box("msg", "O SRF-PLL gira o referencial dq até alinhar o eixo d com a tensão da rede.")
fala(7)
n.p("Este é o slide em que a banca mais pode puxar teoria de controle. A seção abaixo "
    "remonta o raciocínio do zero, na ordem em que ele se encadeia: o que é uma malha, "
    "onde cada bloco do PLL entra nela, como sai a função de transferência, como ler polos "
    "e amortecimento, por que o erro vai a zero e por que o afundamento amolece o laço.")

sub("1. Relembrando: a malha fechada")
n.p("Toda malha de controle tem as mesmas peças: uma <b>referência</b> (o que se quer), "
    "uma <b>saída</b> (o que se tem), um <b>comparador</b> que forma o erro, um "
    "<b>controlador</b> que transforma o erro em ação e uma <b>planta</b> que responde à "
    "ação. A realimentação faz a saída perseguir a referência: enquanto houver erro, o "
    "controlador age. O SRF-PLL é exatamente isso, só que a grandeza controlada é um "
    "<b>ângulo</b>:")
tab(["Peça da malha", "No SRF-PLL", "Sinal"], [
    ["Referência", "ângulo real da tensão da rede (não é medido direto)", "&#952;<sub>g</sub>"],
    ["Saída", "ângulo estimado pelo PLL", "&#952;<sub>PLL</sub>"],
    ["Comparador / sensor", "Park da tensão medida: compara os dois ângulos sem medir "
     "&#952;<sub>g</sub>", "v<sub>q</sub> &#8776; U&#183;(&#952;<sub>g</sub> &#8722; "
     "&#952;<sub>PLL</sub>)"],
    ["Controlador", "PI (o &#8220;filtro de laço&#8221;)", "&#916;&#969;"],
    ["Planta (atuador)", "VCO: integrador que transforma frequência em ângulo",
     "&#952;<sub>PLL</sub> = &#8747;&#969;<sub>PLL</sub>dt"],
], [3.4, 7.3, 4.0])
box("base", "O PLL é um controlador de posição angular: a Park mede o erro, o PI decide a "
    "correção de velocidade e o integrador transforma velocidade em posição.")

sub("2. Os três blocos, um a um")
bul("<b>Detector de fase (PD)</b>: a própria Park sobre a tensão medida. Como mostrado no "
    "slide 6, v<sub>q</sub> = U&#183;sen(&#952;<sub>g</sub> &#8722; &#952;<sub>PLL</sub>). "
    "Para erro pequeno, sen x &#8776; x, e v<sub>q</sub> &#8776; U&#183;&#916;&#952;: o erro "
    "de ângulo multiplicado pela amplitude. O v<sub>d</sub> &#8776; U do diagrama é a "
    "amplitude estimada, usada depois nas referências de corrente (slide 12).",
    "<b>Filtro de laço (PI)</b>: recebe v<sub>q</sub> e entrega a correção de frequência "
    "&#916;&#969;. A parte proporcional reage ao erro presente; a integral acumula o erro "
    "passado e é ela que &#8220;memoriza&#8221; um desvio de frequência da rede.",
    "<b>VCO</b> (oscilador controlado por tensão, nome herdado do PLL analógico): no "
    "digital, é um integrador. Soma &#916;&#969; à nominal &#969;<sub>0</sub> = 2&#960;&#183;60 "
    "e integra para dar &#952;<sub>PLL</sub>, que volta à Park da tensão (a realimentação "
    "tracejada em laranja) e segue para as malhas de corrente.")
eq(r"\Delta\omega = K_{pPLL}\,v_q + K_{iPLL}\int v_q\,dt \qquad "
   r"\theta_{PLL} = \int(\omega_0 + \Delta\omega)\,dt")
n.p("<b>Sinal da correção.</b> Se a rede está adiantada (&#952;<sub>g</sub> &gt; "
    "&#952;<sub>PLL</sub>), v<sub>q</sub> &gt; 0, o PI aumenta &#916;&#969;, o PLL gira mais "
    "depressa e alcança a rede. Se está atrasada, o contrário. Quando v<sub>q</sub> = 0, o "
    "eixo d está sobre a tensão: o PLL travou.")
n.p("<b>Por que o feed-forward &#969;<sub>0</sub>?</b> O ângulo da rede é uma rampa, "
    "&#952;<sub>g</sub> = &#969;<sub>0</sub>t + &#966;. Somando &#969;<sub>0</sub> por fora, o "
    "PI só precisa cuidar do <b>desvio</b> em torno de 60 Hz. Sem ele, a integral teria de "
    "construir 377 rad/s a partir de zero na partida, com um transitório longo e grande.")

sub("3. Relembrando: Laplace, integrador e PI")
n.p("Em Laplace, derivar vira multiplicar por s e integrar vira dividir por s. Assim o VCO "
    "é 1/s e o PI é:")
eq(r"C(s) = K_p + \frac{K_i}{s} = \frac{K_p\,s + K_i}{s}",
   onde="Um <b>polo na origem</b> (o integrador do PI) e um <b>zero</b> em s = "
        "&#8722;K<sub>i</sub>/K<sub>p</sub>. Na sintonia nominal, 105.820/460 = 230 rad/s.")
box("base", "Polo: valor de s que faz a função ir ao infinito, define o modo natural de "
    "resposta. Zero: valor de s que zera a função, muda a forma da resposta (no PLL, aumenta "
    "a sobre-elevação, ver slide 10). Integrador = polo em s = 0.")

sub("4. Montando a malha fechada passo a passo")
n.p("Com o PD linearizado (ganho U), a malha aberta é o produto dos três blocos:")
eq(r"L(s) = U\cdot\frac{K_p s + K_i}{s}\cdot\frac{1}{s} = \frac{U(K_p s + K_i)}{s^2}",
   onde="Da esquerda para a direita: U é o detector (Park linearizada), a fração do meio é "
        "o PI e 1/s é o VCO. O s&#178; do denominador são os dois integradores.")
n.p("Fechando a realimentação unitária, G = L/(1 + L):")
eq(r"G(s) = \frac{\theta_{PLL}(s)}{\theta_g(s)} = "
   r"\frac{U K_p\,s + U K_i}{s^2 + U K_p\,s + U K_i}",
   onde="Com U = 1 pu, é a Eq. (3.18) do TCC. A forma com U é a de Karimi-Ghartemani "
        "(2014), eq. 6.4: s<super>2</super> + h<sub>0</sub>Us + h<sub>1</sub>U = 0.")
n.p("O denominador é a <b>equação característica</b> (o cartão da direita do slide). "
    "Igualando à forma canônica de 2ª ordem, termo a termo:")
eq(r"s^2 + U K_p\,s + U K_i = 0 \quad\Leftrightarrow\quad s^2 + 2\xi\omega_n s + \omega_n^2 = 0",
   onde="Com U = 1 pu: K<sub>p</sub> = 2&#958;&#969;<sub>n</sub> (coeficiente de s) e "
        "K<sub>i</sub> = &#969;<sub>n</sub><super>2</super> (termo independente), TCC 3.19.")
box("base", "Dois integradores na malha aberta (PI e VCO) dão uma malha fechada de 2ª ordem. "
    "Toda a sintonia se resume a escolher onde ficam os dois polos.")

n.p("Como ler &#969;<sub>n</sub> e &#958; nos polos, e como se escolhem os seus valores, "
    "fica para o slide 10.")

sub("5. Relembrando: tipo do sistema e erro em regime")
n.p("O <b>tipo</b> de uma malha é o número de integradores na malha aberta L(s). Ele diz "
    "que entradas a malha segue com erro nulo em regime, pelo teorema do valor final, "
    "e<sub>&#8734;</sub> = lim<sub>s&#8594;0</sub> s&#183;E(s), com:")
eq(r"E(s) = \theta_g - \theta_{PLL} = \frac{1}{1+L(s)}\,\theta_g(s) = "
   r"\frac{s^2}{s^2 + U K_p s + U K_i}\,\theta_g(s)")
tab(["O que a rede faz", "&#952;<sub>g</sub>(s)", "Só P (tipo 1)", "PI (tipo 2, o do TCC)"], [
    ["Salto de fase &#916;&#966;", "&#916;&#966;/s", "0", "0"],
    ["Degrau de frequência &#916;&#969;", "&#916;&#969;/s&#178;",
     "&#916;&#969;/(U&#183;K<sub>p</sub>), constante", "0"],
], [4.4, 2.6, 3.9, 3.8])
n.p("O s&#178; no numerador de E(s) é a assinatura do tipo 2: cancela o s&#178; do degrau "
    "de frequência e o erro vai a zero. Fisicamente, a integral do PI guarda o "
    "&#916;&#969; necessário com v<sub>q</sub> = 0. É por isso que, depois da falta, o PLL "
    "volta a zero sozinho, desde que não perca o sincronismo no caminho.")
box("prova", "<b>&#8220;Por que PI e não só um ganho proporcional?&#8221;</b> Só com P, o "
    "laço é tipo 1 (só o integrador do VCO). Se a frequência da rede se desvia, sobra um "
    "erro de ângulo permanente &#916;&#969;/(U&#183;K<sub>p</sub>): v<sub>q</sub> fica "
    "diferente de zero e o eixo d nunca alinha de fato. O integrador do PI zera esse erro.")

sub("6. O que o afundamento faz com o laço")
n.p("Como a tensão é dividida por um valor fixo (o porquê está no slide 10), U fica dentro "
    "do ganho do detector: em regime U = 1, mas na falta U cai. Casando a equação "
    "característica com a forma canônica, agora com U livre:")
eq(r"\omega_{n,\mathrm{ef}}^2 = U K_i \Rightarrow \omega_{n,\mathrm{ef}} = \omega_n\sqrt{U}"
   r"\qquad 2\xi_{\mathrm{ef}}\omega_{n,\mathrm{ef}} = U K_p \Rightarrow "
   r"\xi_{\mathrm{ef}} = \xi\sqrt{U}")
eq(r"t_{s,\mathrm{ef}} = \frac{4{,}6}{\xi_{\mathrm{ef}}\,\omega_{n,\mathrm{ef}}} = "
   r"\frac{9{,}2}{U K_p} = \frac{20\ \mathrm{ms}}{U}",
   onde="O laço amolece justamente quando mais precisa reagir: a frequência natural e o "
        "amortecimento caem com &#8730;U, e o tempo de acomodação (critério de 1% do slide "
        "10) cresce com 1/U.")
tab(["U (pu)", "&#969;<sub>n,ef</sub> (rad/s)", "&#958;<sub>ef</sub>", "t<sub>s,ef</sub>",
     "Leitura"], [
    ["1,0", "325,3", "0,707", "20 ms", "sintonia nominal"],
    ["0,5", "230,0", "0,500", "40 ms", "afundamento moderado"],
    ["0,25", "162,7", "0,354", "80 ms", "&#969;<sub>n</sub> e &#958; à metade"],
    ["0,2", "145,5", "0,316", "100 ms", "igual à sintonia inadequada"],
    ["0,09", "97,6", "0,212", "~220 ms", "ordem da tensão na falta (capítulo 6 do painel)"],
], [1.6, 2.8, 1.6, 1.9, 6.8])
n.note("Valores do modelo linear, válidos enquanto o erro de ângulo for pequeno. O "
       "t<sub>s,ef</sub> é um indicador de tendência: a tensão não fica parada num U só "
       "durante a falta.")

sub("7. Onde o modelo linear deixa de valer")
n.p("O detector real é v<sub>q</sub> = U&#183;sen(&#916;&#952;), não U&#183;&#916;&#952;. "
    "A aproximação erra cerca de 5% em 30&#176; e piora depois. Três consequências:")
bul("<b>Ganho máximo em 90&#176;</b>: acima disso, quanto maior o erro, <b>menor</b> o "
    "sinal que o PI recebe para corrigir.",
    "<b>Ponto instável em 180&#176;</b>: se &#916;&#952; passa de 180&#176;, o sinal de "
    "v<sub>q</sub> inverte e o PLL é empurrado para o próximo ponto de travamento, um ciclo "
    "à frente. É o escorregamento de ciclo, a forma concreta de perder o sincronismo.",
    "<b>U perto de zero</b>: numa falta próxima, v<sub>q</sub> fica quase nulo qualquer que "
    "seja o erro. O PLL fica &#8220;cego&#8221;: a integral segura o último &#916;&#969; e o "
    "ângulo deriva até a tensão voltar.")
box("alem", "Por isso a sintonia lenta e pouco amortecida é a mais exposta: com "
    "&#958;<sub>ef</sub> baixo, a resposta passa do ponto, o erro chega mais longe e fica "
    "mais perto dos 180&#176; no momento em que a tensão volta.")

sub("8. Por que o travamento importa: a conta do erro de ângulo")
n.p("Com o eixo d sobre a tensão, i<sub>d</sub> controla só a potência ativa e "
    "i<sub>q</sub> só a reativa: é o desacoplamento entre P e Q. Se &#952;<sub>PLL</sub> "
    "erra de &#916;&#952;, a corrente que o controle manda no eixo d sai girada de "
    "&#916;&#952; em relação à tensão real. Uma fração cos &#916;&#952; vira ativa e sen "
    "&#916;&#952; vaza para a reativa (e vice-versa para i<sub>q</sub>):")
tab(["Erro de ângulo", "cos &#916;&#952; (fica no eixo certo)", "sen &#916;&#952; (vaza)"], [
    ["5&#176;", "99,6%", "8,7%"],
    ["10&#176;", "98,5%", "17,4%"],
    ["30&#176;", "86,6%", "50,0%"],
    ["90&#176;", "0%", "100%: o reativo pedido pelo ONS sai como ativo"],
], [3.4, 5.0, 6.3])
n.p("Daí a pergunta do rodapé: o suporte de tensão do ONS depende de injetar reativo "
    "<b>na direção certa</b>, e quem dá a direção é o PLL.")
box("banca", "<b>Por que o travamento importa?</b> Um erro em &#952; passa direto às malhas "
    "de corrente e compromete o desacoplamento entre P e Q.")

sub("Glossário de bolso")
tab(["Termo", "Em uma frase"], [
    ["Malha aberta L(s)", "produto de tudo que o sinal atravessa do erro até a saída"],
    ["Malha fechada G(s)", "L/(1+L): como a saída responde à referência"],
    ["Equação característica", "denominador de G(s) igualado a zero; suas raízes são os polos"],
    ["&#969;<sub>n</sub>", "frequência natural: o quão rápido o laço se move"],
    ["&#958;", "amortecimento: o quanto ele oscila antes de assentar (0,707 = clássico)"],
    ["t<sub>s</sub>", "tempo até a resposta ficar dentro de 1% do final (4,6/&#958;&#969;<sub>n</sub>)"],
    ["Tipo", "número de integradores em L(s); tipo 2 segue degrau de frequência sem erro"],
    ["Banda passante", "até onde G(s) segue a entrada; acima, filtra (slide 11)"],
], [4.2, 10.5])
ponte("antes de sintonizar, qual rede o PLL enxerga?")

# --- 8
slide(8, "Sistema IEEE 9 barras", "Modelagem", "Victor, Bruno, Victor", "Fig. 4.1, §4.3.1")
box("msg", "A UFV assume a Barra 2 e enxerga o resto da rede como um equivalente de "
    "Thévenin.")
fala(8)
sub("Fundamento: o sistema")
n.p("O caso clássico tem três geradores, três transformadores, seis linhas e três cargas, "
    "em 230 kV. O G2 (192 MVA) sai e a UFV de 100 MW entra na Barra 2; G1 e G3 continuam "
    "síncronos e carregam a inércia que sobra.")
sub("Fundamento: sistema por unidade")
n.p("Tudo é dividido por uma base: potência de 100 MVA e a tensão nominal de cada trecho. "
    "A impedância base sai das duas:")
eq(r"Z_{base} = \frac{V_{base}^2}{S_{base}}",
   onde="20 kV: 4 &#937;; 230 kV: 529 &#937;. Em pu, os 100 MW da usina valem 1 pu e os "
        "transformadores ideais somem das contas.")
sub("Fundamento: Thévenin pela matriz de impedância nodal")
n.p("A Z<sub>barra</sub> é a inversa da matriz de admitâncias da rede. O elemento "
    "diagonal Z<sub>22</sub> é, por definição, a impedância vista da Barra 2 com as fontes "
    "anuladas: é a impedância de Thévenin que o inversor enxerga. No PSIM, a rede inteira foi "
    "reduzida a uma fonte atrás dessa impedância; no Simulink, roda o sistema completo.")
box("alem", "<b>Força da rede (SCR).</b> A relação de curto-circuito é a potência de curto "
    "no ponto de conexão dividida pela potência do inversor; com o inversor em 1 pu, é "
    "aproximadamente 1/|Z<sub>th</sub>| em pu. Rede &#8220;fraca&#8221; é a de SCR baixo, "
    "onde a corrente do inversor mexe muito na própria tensão que o PLL mede. O TCC mantém "
    "o nível de curto fixo e varia o local da falta: varrer o SCR é trabalho futuro.")
nums([["192 MVA", "máquina original da Barra 2"],
      ["100 MW = 1 pu", "UFV, na base de 100 MVA, 60 Hz"],
      ["230 kV / 20 kV", "rede de transmissão / tensão do lado do inversor"]])
box("banca", "<b>Por que um Thévenin no PSIM?</b> Representa a rede vista pelo inversor com "
    "boa fidelidade dinâmica e mantém a coerência com o sistema completo do Simulink.")
box("cuidado", "R<sub>th</sub> = 10,04 m&#937; e L<sub>th</sub> = 1,16 mH não estão no TCC; "
    "aparecem só no apêndice (slide 24).")
ponte("com a rede reduzida, deu para testar o PLL sozinho.")

# --- 9
slide(9, "Bancada do PLL", "Modelagem", "Bruno, Victor", "fora do TCC (exceção de método)")
box("msg", "Antes do inversor, o SRF-PLL foi testado isolado entre duas fontes ideais.")
fala(9)
n.p("A geração é uma fonte trifásica ideal; a rede é outra fonte (barramento infinito) "
    "atrás da impedância de Thévenin. Sem chaves e sem filtro, só o laço PD-PI-VCO. É o "
    "princípio de testar um subsistema de cada vez: se o PLL falha aqui, o problema é do "
    "laço, não do conversor. É etapa de método aprovada como exceção à regra &#8220;deck = "
    "TCC&#8221;: entra sem nenhum número.")
box("banca", "<b>Por que começar por fontes ideais?</b> Separa o sincronismo do resto: se o "
    "PLL falha aqui, o problema é do laço.")
ponte("nesta bancada os ganhos do PI foram dimensionados.")

# --- 10
slide(10, "Sintonia do PLL", "Modelagem", "Victor, Bruno, Victor", "§3.4, Eqs. (3.10)-(3.20)")
box("msg", "Fixado o amortecimento, resta um único grau de liberdade: o tempo de acomodação.")
fala(10)
n.p("O slide 7 deu a <b>forma</b> do laço: uma malha fechada de 2ª ordem com dois ganhos, "
    "K<sub>p</sub> e K<sub>i</sub>. Este slide responde <b>como se escolhe cada número</b>. "
    "A lógica em uma linha: tornar o laço independente da tensão (passos 1 e 2), trocar os "
    "dois ganhos por duas grandezas com significado físico, &#969;<sub>n</sub> e &#958; "
    "(passo 3), fixar uma delas por um critério clássico (passo 4) e escolher a outra pela "
    "velocidade desejada (passo 5).")

sub("Passo 1: tensão em pu. De onde vem 16.329,93 V")
n.p("A rede do lado do inversor é de 20 kV <b>de linha, eficaz</b>. O detector trabalha com "
    "o <b>pico de fase</b>, então:")
eq(r"V_{pico,fase} = \frac{20\,000}{\sqrt{3}}\cdot\sqrt{2} = 11\,547\cdot 1{,}414 = "
   r"16\,329{,}93\ \mathrm{V}",
   onde="&#8730;3 passa de linha para fase; &#8730;2 passa de eficaz para pico. Com a "
        "transformada invariante em amplitude (slide 6), é esse pico que aparece inteiro em "
        "v<sub>d</sub>.")
n.p("<b>Por que dividir.</b> Sem a divisão, v<sub>q</sub> &#8776; 16.329,93&#183;&#916;&#952; "
    "volts: o ganho do detector seria 16.329,93, e ele entraria multiplicando os dois ganhos "
    "do PI. Dividindo, a tensão nominal vale U = 1 pu, o ganho do detector K<sub>pd</sub> vale "
    "1 e a equação característica do slide 7 fica sem U. É isso que deixa usar as fórmulas "
    "canônicas direto.")
n.p("<b>Por que um valor fixo, e não a amplitude medida.</b> O divisor é constante: em "
    "regime ele dá U = 1, mas na falta a tensão cai e U cai junto. É daí que vem o "
    "amolecimento do laço (&#969;<sub>n</sub>&#8730;U, &#958;&#8730;U, slide 7, passo 6).")
box("alem", "<b>A alternativa que o TCC não usa.</b> Dividir v<sub>q</sub> pela amplitude "
    "medida, &#8730;(v<sub>d</sub>&#178; + v<sub>q</sub>&#178;), torna o laço independente de U "
    "(Karimi-Ghartemani, 2014). O modelo do TCC normaliza por constante, como a maioria das "
    "implementações básicas, e é justamente essa dependência que o trabalho explora.")

sub("Passo 2: linearizar")
n.p("O detector real é v<sub>q</sub> = V<sub>m</sub>&#183;sen(&#952;<sub>ref</sub> &#8722; "
    "&#952;<sub>PLL</sub>). Para projetar, considera-se o PLL já perto do travamento, com "
    "erro pequeno, onde sen x &#8776; x:")
eq(r"v_q \approx V_m(\theta_{ref} - \theta_{PLL}), \qquad V_m = 1\ \mathrm{pu} "
   r"\Rightarrow K_{pd} = 1")
n.p("Projetar no ponto de operação e conferir depois em simulação é o procedimento padrão: "
    "as fórmulas lineares dizem como o laço se comporta em torno do travamento. Longe dele "
    "(erro grande, falta próxima), quem responde é a simulação (slide 7, passo 7).")

sub("Passo 3: forma canônica. Por que &#8220;um único grau de liberdade&#8221;")
n.p("Com K<sub>pd</sub> = 1, a equação característica s&#178; + K<sub>p</sub>s + K<sub>i</sub> "
    "= 0 é comparada termo a termo com a de qualquer sistema de 2ª ordem:")
eq(r"s^2 + K_p\,s + K_i = s^2 + 2\xi\omega_n s + \omega_n^2 \ \Rightarrow\ "
   r"K_p = 2\xi\omega_n, \quad K_i = \omega_n^2")
n.p("São duas incógnitas (K<sub>p</sub>, K<sub>i</sub>) e agora duas grandezas que se sabe "
    "interpretar (&#969;<sub>n</sub>, &#958;). Escolher os ganhos é o mesmo que escolher "
    "&#969;<sub>n</sub> e &#958;. Fixado o &#958; (passo 4), sobra uma escolha só: o "
    "t<sub>s</sub> (passo 5), que define &#969;<sub>n</sub>. É o &#8220;único grau de "
    "liberdade&#8221; do título.")
sub("Relembrando: como ler &#969;<sub>n</sub> e &#958; nos polos")
n.p("As raízes da equação característica, para &#958; &lt; 1, são um par complexo:")
eq(r"s = -\xi\omega_n \pm j\,\omega_n\sqrt{1-\xi^2}",
   onde="Parte real &#8722;&#958;&#969;<sub>n</sub>: velocidade com que a envoltória "
        "e<super>&#8722;&#958;&#969;n t</super> morre; é ela que define o t<sub>s</sub>. "
        "Parte imaginária: frequência da oscilação amortecida. &#969;<sub>n</sub> é a "
        "distância do polo à origem; &#958; é o cosseno do ângulo entre o polo e o semieixo "
        "real negativo.")
n.p("Na sintonia nominal, os polos ficam em <b>&#8722;230 &#177; j230</b>: a 45&#176;, "
    "exatamente na diagonal, porque cos 45&#176; = 0,707. Polo mais à esquerda: decai mais "
    "rápido. Polo mais perto do eixo imaginário: oscila mais. Sobre o eixo imaginário, "
    "oscilação sem amortecimento; à direita dele, instabilidade.")
box("alem", "Conta rápida para conferir: parte real = K<sub>p</sub>/2 = 460/2 = 230; parte "
    "imaginária = &#8730;(K<sub>i</sub> &#8722; 230&#178;) = &#8730;(105.820 &#8722; 52.900) "
    "&#8776; 230.")

sub("Passo 4: fixar &#958; = 0,707. Por que esse valor")
n.p("O &#958; decide o formato da resposta, independente da velocidade. A sobre-elevação "
    "do protótipo de 2ª ordem só depende dele:")
eq(r"M_p = e^{-\pi\xi/\sqrt{1-\xi^2}}")
tab(["&#958;", "M<sub>p</sub>", "Polo com o eixo real", "Leitura"], [
    ["0,316", "35%", "71,6&#176;", "oscila muito (é a sintonia inadequada, slide 11)"],
    ["0,5", "16%", "60&#176;", "ainda oscila bastante"],
    ["<b>0,707</b>", "<b>4,3%</b>", "<b>45&#176;</b>", "<b>compromisso clássico</b>"],
    ["1,0", "0%", "0&#176; (polo duplo real)", "sem oscilação, porém mais lento"],
], [1.8, 1.6, 3.6, 7.7])
n.p("Abaixo de 0,707, a resposta passa do ponto e oscila; acima, fica cada vez mais lenta "
    "para chegar ao valor final, sem ganho real em oscilação. 0,707 é o ponto em que se "
    "aceita um pequeno sobressinal em troca de rapidez. É também o menor &#958; em que a "
    "resposta em frequência do protótipo não tem pico de ressonância. É o valor de Ogata e "
    "o de Alves, Dias e Rolim (2020).")
box("prova", "<b>&#8220;A sobre-elevação do PLL é mesmo 5%?&#8221;</b> Os 4,3% valem para o "
    "protótipo de 2ª ordem sem zero. A G(s) do PLL (TCC 3.18) tem um zero, que vem do PI, "
    "e com ele a resposta ao degrau de fase passa mais: cerca de 21% com a sintonia "
    "nominal (conta de simulação do modelo linear, além do TCC). Resposta segura: o "
    "&#958; = 0,707 foi escolhido pela forma canônica, como em Ogata e em Alves, Dias e "
    "Rolim; o zero do PI aumenta a sobre-elevação ao degrau de fase, e o tempo de "
    "acomodação continua perto dos 20 ms (cerca de 16 ms no modelo linear).")

sub("Passo 5: escolher t<sub>s</sub>. De onde vem o 4,6")
n.p("A resposta de 2ª ordem subamortecida é uma senoide que morre dentro da envoltória "
    "e<super>&#8722;&#958;&#969;n t</super>. O tempo de acomodação é quando essa envoltória "
    "cai a 1% do valor inicial:")
eq(r"e^{-\xi\omega_n t_s} = 0{,}01 \ \Rightarrow\ \xi\omega_n t_s = \ln 100 = 4{,}6 "
   r"\ \Rightarrow\ t_s = \frac{4{,}6}{\xi\omega_n}", tag="3.20",
   onde="Com o critério de 2%, seria ln 50 &#8776; 3,9, arredondado para 4: é o "
        "4/(&#958;&#969;<sub>n</sub>) usado no PI de corrente (slide 14). O 1% é mais "
        "exigente: para o mesmo t<sub>s</sub>, pede um laço um pouco mais rápido.")
n.p("<b>O compromisso.</b> t<sub>s</sub> curto significa &#969;<sub>n</sub> alto e banda "
    "larga: o PLL acompanha rápido, mas deixa passar ruído de medição, harmônicos e o "
    "desequilíbrio (os 120 Hz da sequência negativa, slide 11) para o ângulo. t<sub>s</sub> "
    "longo filtra bem, mas não acompanha variações reais da rede e demora a retomar o "
    "sincronismo depois da falta.")
n.p("<b>Por que 20 ms.</b> Um período de 60 Hz dura 16,7 ms; 20 ms é pouco mais de um "
    "ciclo, ou seja, o PLL acomoda em pouco mais de um ciclo da rede. É o valor de Alves, "
    "Dias e Rolim (2020) e de Teodorescu, Liserre e Rodriguez (2011).")
box("prova", "<b>&#8220;O que acontece se aumentar muito os ganhos?&#8221;</b> &#969;<sub>n</sub> "
    "e a banda sobem: o PLL acompanha mais rápido, mas deixa passar mais ruído, harmônicos e "
    "os 120 Hz da sequência negativa para o ângulo. Com os 20 ms, a banda já fica em 107 Hz, "
    "colada nos 120 Hz (slide 11): ir mais rápido pioraria isso.")

sub("A conta de mão, do t<sub>s</sub> aos ganhos")
n.p("Com &#958; = 0,707 e t<sub>s</sub> = 20 ms, quatro linhas, cada uma usando só a "
    "anterior:")
tab(["", "Conta", "Resultado", "De onde vem"], [
    ["1", "&#958;&#969;<sub>n</sub> = 4,6 / 0,020", "230 rad/s", "critério de 1% (passo 5)"],
    ["2", "K<sub>p</sub> = 2&#183;&#958;&#969;<sub>n</sub> = 2&#183;230", "460",
     "forma canônica (passo 3); o mesmo que 9,2/t<sub>s</sub>"],
    ["3", "&#969;<sub>n</sub> = 230 / 0,707", "325,3 rad/s (51,8 Hz)",
     "divide pelo &#958; fixado (passo 4)"],
    ["4", "K<sub>i</sub> = &#969;<sub>n</sub>&#178; = 325,3&#178;", "105.820",
     "forma canônica (passo 3)"],
], [0.7, 5.0, 3.6, 5.4])
n.p("Repare que K<sub>p</sub> nem precisa do &#958;: 2&#183;&#958;&#969;<sub>n</sub> = "
    "2&#183;4,6/t<sub>s</sub> = 9,2/t<sub>s</sub>, a forma de Teodorescu. O &#958; só entra "
    "para tirar &#969;<sub>n</sub> e, com ele, K<sub>i</sub>. Por isso K<sub>p</sub> fixa a "
    "<b>velocidade</b> e K<sub>i</sub>, junto com K<sub>p</sub>, o <b>amortecimento</b>.")
box("cuidado", "K<sub>i</sub> depende do arredondamento: com &#969;<sub>n</sub> = 325,3 sai "
    "105.820, o valor do TCC e do modelo. Sem arredondar o 0,707 e o 4,6 o número muda na "
    "terceira casa. Na fala, use sempre 105.820.")
nums([["460 / 105.820", "K<sub>pPLL</sub> / K<sub>iPLL</sub> nominais"],
      ["325,3 rad/s", "&#969;<sub>n</sub> nominal, 51,8 Hz"],
      ["0,707", "&#958;; 4,3% no protótipo de 2ª ordem (o TCC diz cerca de 5%); ~21% com o "
                "zero do PI"],
      ["20 ms", "t<sub>s</sub> pelo critério de 1%"]])
box("cuidado", "A régua do slide mostra só &#8220;1 período&#8221; e 20 ms. O porquê do "
    "critério de 1% está em criterio_acomodacao_srf_pll.pdf.")
ponte("esta é a sintonia nominal; para testar a sensibilidade, uma segunda.")

# --- 11
slide(11, "Duas sintonias do PLL", "Modelagem", "Bruno, Victor", "§3.4 (eq. 3.20), §4.3")
box("msg", "A sintonia inadequada reduz os dois ganhos em 80%: laço mais lento e menos "
    "amortecido.")
fala(11)
sub("Fundamento: a conta da inadequada")
eq(r"K_p = 0{,}2\cdot460 = 92 \qquad K_i = 0{,}2\cdot105\,820 = 21\,164")
eq(r"\omega_n = \sqrt{21\,164} = 145{,}5\ \mathrm{rad/s} \qquad "
   r"\xi = \frac{92}{2\cdot145{,}5} = 0{,}316",
   onde="Como K<sub>i</sub> cai 5 vezes, &#969;<sub>n</sub> cai &#8730;5 &#8776; 2,24 vezes; "
        "&#958; cai na mesma proporção. Pelo mesmo critério, t<sub>s</sub> sobe para cerca "
        "de 100 ms.")
sub("Fundamento: o cartão 2&#969;<sub>0</sub> = 2,32&#183;&#969;<sub>n</sub>")
n.p("A oscilação da sequência negativa é de 120 Hz, ou 754 rad/s: só 2,32 vezes a "
    "&#969;<sub>n</sub> nominal. Um laço de segunda ordem só atenua bem o que está muito "
    "acima da sua &#969;<sub>n</sub>. Quanto passa sai do módulo de G(j&#969;):")
eq(r"|G(j\omega)| = \frac{\sqrt{K_i^2 + (K_p\,\omega)^2}}"
   r"{\sqrt{(K_i - \omega^2)^2 + (K_p\,\omega)^2}}")
box("alem", "Contas com o modelo linear e U = 1 (tabela abaixo).")
tab(["", "Nominal", "Inadequada"], [
    ["&#969;<sub>n</sub> ; &#958;", "325,3 rad/s ; 0,707", "145,5 rad/s ; 0,316"],
    ["Polos ; ângulo com o eixo real", "&#8722;230 &#177; j230 ; 45&#176;",
     "&#8722;46 &#177; j138 ; 71,6&#176;"],
    ["Banda de &#8722;3 dB de G(s)", "669 rad/s (107 Hz)", "242 rad/s (38 Hz)"],
    ["|G(j754)|: quanto do 120 Hz passa", "0,63", "0,13"],
    ["t<sub>s</sub> (critério de 1%)", "20 ms", "~100 ms"],
], [6.0, 4.35, 4.35])
n.p("A leitura: a banda da sintonia nominal (107 Hz) fica colada nos 120 Hz, então quase "
    "dois terços da oscilação chegam ao ângulo. A inadequada deixa passar um oitavo, por "
    "isso filtra melhor (capítulo 5 do painel), mas responde cinco vezes mais devagar "
    "(capítulo 6).")
box("alem", "<b>A inadequada não é artificial.</b> Pela fórmula do slide 7, a sintonia "
    "nominal com U = 0,2 pu tem &#969;<sub>n</sub> = 325,3&#183;&#8730;0,2 = 145,5 rad/s e "
    "&#958; = 0,707&#183;&#8730;0,2 = 0,316: exatamente a inadequada. Um afundamento para "
    "0,2 pu deixa o laço nominal com a dinâmica da sintonia inadequada. Bom argumento se a "
    "banca questionar o fator 0,2.")
nums([["92 / 21.164", "K<sub>p</sub> / K<sub>i</sub> inadequados (nominais &#215; 0,2)"],
      ["145,5 rad/s; 0,316", "&#969;<sub>n</sub> (23,2 Hz); &#958;"],
      ["754 rad/s = 2,32&#183;&#969;<sub>n</sub>", "120 Hz contra a &#969;<sub>n</sub> nominal"]])
box("banca", "<b>Por que reduzir os ganhos?</b> Simula uma malha de sincronismo mais lenta "
    "e menos amortecida; no caso-limite, o SRF-PLL deixa de recuperar o sincronismo após a "
    "eliminação da falta.")
ponte("com o sincronismo resolvido, o inversor.")

# --- 12
slide(12, "Referência de corrente", "Modelagem", "Victor, Bruno",
      "§3.1.3-3.1.4, Eqs. (3.8)-(3.9); diagrama: exceção de método (PSIM)")
box("msg", "Na primeira versão do inversor, a referência de corrente saía direto da "
    "potência desejada.")
fala(12)
sub("Fundamento: potência em dq")
eq(r"P = \frac{3}{2}\left(v_d i_d + v_q i_q\right) \qquad "
   r"Q = \frac{3}{2}\left(v_q i_d - v_d i_q\right)", tag="3.8",
   onde="O 3/2 compensa o 2/3 da Park invariante em amplitude.")
n.p("Com o PLL travado, v<sub>q</sub> = 0 e cada potência depende de uma só corrente "
    "(TCC 3.9). Invertendo:")
eq(r"i_{d,ref} = \frac{2P}{3v_d} \qquad i_{q,ref} = -\frac{2Q}{3v_d}",
   onde="Em pu, o 3/2 some. Na versão do PSIM: P<sub>ref</sub> = 1 pu (100 MW) em degrau "
        "aplicado em 35 ms e Q<sub>ref</sub> = 0, divididos por v<sub>d</sub> vindo do "
        "próprio SRF-PLL.")
box("alem", "<b>E se o ângulo estiver errado?</b> Escrevendo a tensão no referencial do PLL "
    "(v<sub>d</sub> = V cos&#916;&#952;, v<sub>q</sub> = V sen&#916;&#952;) e substituindo "
    "acima, sai a equação a seguir.")
eq(r"P = \frac{3}{2}V\left(i_d\cos\Delta\theta + i_q\sin\Delta\theta\right) \qquad "
   r"Q = \frac{3}{2}V\left(i_d\sin\Delta\theta - i_q\cos\Delta\theta\right)",
   onde="Com &#916;&#952; = 0 volta ao caso desacoplado. Com &#916;&#952; grande, a corrente "
        "que o controle chama de ativa vira reativa, e com |&#916;&#952;| &gt; 90° a ativa "
        "muda de sinal. É o mecanismo da potência absorvida no capítulo 6 do painel.")
box("banca", "<b>Por que o PLL importa aqui?</b> A divisão só vale com v<sub>q</sub> = 0; "
    "quem alinha o eixo d e entrega v<sub>d</sub> é o SRF-PLL.")
box("cuidado", "&#8220;35 ms&#8221; é o único número fora do TCC neste slide (aprovado). O "
    "TCC se contradiz sobre o desacoplamento (§3.1.4 diz que não há, §3.5 diz que há); o "
    "slide não afirma nenhum dos dois.")
ponte("antes da malha de corrente, o filtro que liga o inversor à rede.")

# --- 13
slide(13, "Filtro LCL", "Modelagem", "Bruno, Victor",
      "§4.3.2 e §4.3.2.1 (só os resultados; equações fora do TCC)")
box("msg", "Quatro passos fixam o filtro, com a ressonância entre a rede e o chaveamento.")
fala(13)
box("cuidado", "Slide de exceção de método (aprovada em 27/10/2026): o TCC entregue só traz "
    "os resultados (L<sub>est</sub> = 30,71 mH, &#969;<sub>res</sub> = 9.068,99 rad/s, "
    "R<sub>d1</sub>, R<sub>d2</sub>, R<sub>d3</sub>), não as equações. Na tela e na fala, só os "
    "números do TCC. Os intermediários abaixo (L<sub>1</sub>, L<sub>2</sub>, C, V<sub>cc</sub>) "
    "são do modelo e servem para responder, não para dizer.")
sub("Fundamento: por que LCL")
n.p("O inversor chaveia a 5 kHz: a tensão de saída é uma sequência de pulsos, e a corrente "
    "carrega ondulação nessa frequência. O filtro deixa passar os 60 Hz e barra o "
    "chaveamento. Um L simples precisaria de indutância enorme; o LCL atenua muito mais "
    "com menos material (60 dB por década acima da ressonância, contra 20 dB do L). O preço "
    "é a ressonância, que o passo 3 posiciona e o passo 4 amortece.")
sub("Os quatro passos, com os números do modelo")
n.p("Base: 100 MW em 20 kV dão 2.887 A eficazes por fase, ou 4.082 A de pico. "
    "V<sub>cc</sub> do cálculo = 90,91 kV (o modelo usa 1,5 vez esse valor, ver abaixo).")
eq(r"L_1 = \frac{V_{cc}}{24\,f_{sw}\,\Delta i_{L1}} = "
   r"\frac{90\,909}{24\cdot5000\cdot24{,}9} = 30{,}42\ \mathrm{mH}",
   onde="<b>Passo 1.</b> A ondulação da corrente cresce com V<sub>cc</sub> e cai com "
        "L<sub>1</sub> e f<sub>sw</sub>; o 24 é o fator de pior caso do VSI de dois níveis "
        "usado na tese de Alves. A ondulação admitida foi 0,61% do pico (24,9 A).")
eq(r"L_2 = k\,L_1 = 0{,}0095\cdot30{,}42 = 0{,}289\ \mathrm{mH} \qquad "
   r"L_{est} = L_1 + L_2 = 30{,}71\ \mathrm{mH}",
   onde="<b>Passo 2.</b> L<sub>est</sub> é o número do TCC: é a indutância que a malha de "
        "corrente enxerga em baixa frequência (planta 1/(sL<sub>est</sub>), slide 14).")
eq(r"C_x = \frac{L_1 + L_2}{L_1 L_2\,(\pi f_{sw})^2} = 14{,}16\ \mu\mathrm{F} \qquad "
   r"C = 3\,C_x = 42{,}47\ \mu\mathrm{F}",
   onde="<b>Passo 3.</b> C<sub>x</sub> poria a ressonância exatamente na metade do "
        "chaveamento (&#960;f<sub>sw</sub> = 15.708 rad/s, 2,5 kHz). O fator 3 a puxa para "
        "baixo por &#8730;3, com margem.")
eq(r"\omega_{res} = \sqrt{\frac{L_1 + L_2}{L_1 L_2 C}} = \frac{\pi f_{sw}}{\sqrt{3}} = "
   r"9\,068{,}99\ \mathrm{rad/s}\ (1\,443\ \mathrm{Hz})",
   onde="Cerca de 24 vezes a fundamental e 0,29 vez o chaveamento: a &#8220;faixa "
        "intermediária segura&#8221; do TCC.")
eq(r"R_{d1} = 0{,}05\,\omega_g L_1 = 0{,}5734\ \Omega \quad "
   r"R_{d2} = 0{,}05\,\omega_g L_2 = 0{,}0054\ \Omega \quad "
   r"R_{d3} = \frac{0{,}05}{\omega_g C} = 3{,}1228\ \Omega",
   onde="<b>Passo 4.</b> Cada resistência vale 5% da reatância do seu elemento em 60 Hz "
        "(&#969;<sub>g</sub> = 377 rad/s): amortece o pico de ressonância e quase não mexe "
        "na fundamental.")
sub("Por que o V<sub>cc</sub> é alto")
n.p("No TCC: o barramento CC foi &#8220;fixado em valor constante para manter a margem de "
    "modulação necessária&#8221;. No modelo, V<sub>cc</sub> = 136,36 kV, 1,5 vez os 90,91 kV "
    "do cálculo. A conta que mostra o porquê (além do TCC):")
bul("A reatância de L<sub>1</sub> em 60 Hz é 377&#183;30,42 mH = 11,47 &#937;. Com "
    "2.887 A, a queda nela é cerca de 33,1 kV eficazes por fase.",
    "A tensão de fase da rede é 11,55 kV eficazes. Somando em quadratura, o inversor precisa "
    "sintetizar cerca de 35 kV eficazes, ou 49,6 kV de pico por fase.",
    "No PWM senoidal, o pico de fase máximo sem sobremodular é V<sub>cc</sub>/2. Com 90,91 kV, "
    "dá 45,5 kV: falta tensão e o PWM sobremodula. Com 136,36 kV, dá 68,2 kV: índice de "
    "modulação perto de 0,73, com folga.")
box("prova", "<b>&#8220;L<sub>1</sub> de 30 mH num sistema de 20 kV não é grande demais?&#8221;</b> "
    "É. Na base de 20 kV e 100 MVA (Z<sub>base</sub> = 4 &#937;), 11,47 &#937; são cerca de "
    "2,9 pu, quando o usual fica abaixo de 0,1 pu. Vem do critério de ondulação com uma "
    "ondulação admitida pequena (0,61%). Resposta segura: o filtro foi dimensionado pelo "
    "critério de ondulação de corrente e mantido igual em todos os cenários, então não "
    "interfere na comparação entre sintonias, que é o objeto do trabalho; a consequência foi "
    "exigir um barramento CC maior, para manter a margem de modulação. Otimizar o filtro "
    "fica fora do escopo.")
box("prova", "<b>&#8220;Por que o fator 3 no capacitor?&#8221;</b> Sem ele, a ressonância "
    "cairia na metade do chaveamento, onde ainda há conteúdo do PWM. Triplicando C, ela "
    "desce por &#8730;3 para 1.443 Hz, longe dos dois lados.")
box("alem", "O capacitor absorve reativo na fundamental: com X<sub>C</sub> = 1/(377&#183;42,47 "
    "&#956;F) = 62,5 &#937;, são cerca de 6,4 Mvar, 6,4% dos 100 MVA. Se a banca perguntar, "
    "é da ordem do limite usual de 5%.")
box("cuidado", "O TCC associa &#958; = 0,707 ao filtro; não está na tela deste slide (está no "
    "14). Se perguntarem, é o amortecimento adotado no projeto, o mesmo das malhas; não "
    "elabore.")
nums([["30,71 mH", "L<sub>est</sub> = L<sub>1</sub> + L<sub>2</sub> (TCC)"],
      ["9.068,99 rad/s", "&#969;<sub>res</sub> = &#960;f<sub>sw</sub>/&#8730;3 (TCC), 1.443 Hz"],
      ["0,5734 / 0,0054 / 3,1228 &#937;", "R<sub>d1</sub> / R<sub>d2</sub> / R<sub>d3</sub> (TCC)"],
      ["30,42 mH; 0,289 mH; 42,47 &#956;F", "L<sub>1</sub>; L<sub>2</sub>; C (modelo, apêndice)"],
      ["136,36 kV", "V<sub>cc</sub> do modelo, 1,5 &#215; 90,91 kV (apêndice)"]])
box("banca", "<b>Por que a ressonância fica no meio?</b> Longe da rede e do chaveamento; o "
    "amortecimento passivo atenua o pico de ressonância.")
box("banca", "<b>E o barramento CC?</b> Fixado em valor constante, para manter a margem de "
    "modulação necessária.")
ponte("com o filtro definido, a malha que faz a corrente seguir a referência.")

# --- 14
slide(14, "Controle de corrente", "Modelagem", "Bruno, Victor",
      "Fig. 3.1, §3.5 (Eqs. 3.21-3.23), §4.3.2 (Eq. 4.2)")
box("msg", "Um PI com notch em cada eixo faz a corrente do inversor seguir a referência.")
fala(14)
sub("Fundamento: a malha, eixo por eixo")
n.p("Erro (referência menos medida) &#8594; PI &#8594; filtro notch na ressonância do LCL "
    "&#8594; índice de modulação &#8594; PWM a 5 kHz no VSI de dois níveis. Em baixa "
    "frequência, o filtro se comporta como uma indutância só, L<sub>est</sub>:")
eq(r"G_i(s) = \frac{1}{s\,L_{est}}", tag="3.21")
eq(r"s^2 + \frac{K_p}{L_{est}}s + \frac{K_i}{L_{est}} = 0 \ \Rightarrow\ "
   r"K_p = 2\xi\omega_n L_{est},\ \ K_i = \omega_n^2 L_{est}",
   onde="Eqs. (3.22) e (3.23) do TCC: o polinômio característico e os ganhos que saem dele.")
n.p("É a mesma forma canônica do PLL. Com &#958; = 0,707 e &#969;<sub>n</sub> = "
    "4&#8730;2&#183;f<sub>g</sub> = 339,4 rad/s (TeseAGP):")
eq(r"K_p = 2\cdot\frac{1}{\sqrt{2}}\cdot4\sqrt{2}\,f_g\,L_{est} = 8 f_g L_{est}"
   r"\qquad K_i = (4\sqrt{2}\,f_g)^2 L_{est} = 32 f_g^2 L_{est}",
   onde="Pelo critério de 2%, a corrente acomoda em 4/(&#958;&#969;<sub>n</sub>) = 16,7 ms: "
        "um ciclo.")
sub("Fundamento: por que notch")
n.p("A ressonância do LCL (slide 13) é uma frequência em que o filtro amplifica em vez de "
    "atenuar. Se a malha de corrente excitar essa frequência, a corrente oscila. Além do "
    "amortecimento passivo, o notch é um filtro que corta uma faixa estreita em torno de "
    "&#969;<sub>res</sub> e deixa o resto passar.")
nums([["5 kHz", "chaveamento do PWM"],
      ["339,4 rad/s", "&#969;<sub>n</sub> = 4&#8730;2&#183;60 do PI de corrente"],
      ["30,71 mH", "L<sub>est</sub> = L<sub>1</sub> + L<sub>2</sub>"],
      ["9.068,99 rad/s", "ressonância do LCL, &#958; = 0,707"],
      ["14,74 / 3.537,8", "K<sub>p</sub> / K<sub>i</sub> de corrente (apêndice, fora do TCC)"]])
box("banca", "<b>Por que dois PIs?</b> O PI do PLL zera v<sub>q</sub> e entrega o ângulo; o "
    "PI de corrente faz i<sub>d</sub> e i<sub>q</sub> seguirem a referência. Cada um tem "
    "projeto próprio.")
box("cuidado", "Nunca confundir os dois: K<sub>p</sub> = 8f<sub>g</sub>L<sub>est</sub> é da "
    "corrente, não do PLL. Os ganhos de corrente aparecem escalados no modelo (de propósito; "
    "valores no apêndice). As bandas dos dois PIs são parecidas (339 e 325 rad/s); a "
    "interação entre eles está fora do escopo (defesa_qa.pdf, pergunta 4).")
ponte("no modelo final, a referência deixa de ser fixa.")

# --- 15
slide(15, "Submódulo 2.10 do ONS", "Modelagem", "Bruno, Victor", "Fig. 2.2, Fig. 4.2, §2.5.2, §4.3.2, §5.2")
box("msg", "No modelo final, a tensão medida define o reativo e o ativo fica com o que sobra.")
fala(15)
n.p("No modelo final, as referências fixas da primeira versão (slide 12) dão lugar ao bloco "
    "do Submódulo 2.10, que lê a tensão no PCC e conhece a corrente nominal e a máxima do "
    "conversor. Separação de papéis: o bloco do ONS decide o <b>módulo</b> de cada componente "
    "(i<sub>d,ref</sub> e i<sub>q,ref</sub>); o SRF-PLL decide a <b>direção</b> do eixo "
    "(&#952;<sub>PLL</sub>).")
sub("Fundamento: a rampa (Fig. 2.2)")
eq(r"i_q = \frac{0{,}85 - V}{0{,}35}\quad (0{,}5 \leq V < 0{,}85\ \mathrm{pu}) "
   r"\qquad i_q = 1\ \mathrm{pu}\quad (V < 0{,}5\ \mathrm{pu})",
   onde="Nula em 0,85 pu, igual à nominal em 0,5 pu. Entre 0,85 e 1,1 pu, banda morta "
        "(i<sub>q</sub> = 0, i<sub>d</sub> nominal); acima de 1,1 pu, absorve reativo. "
        "A lógica física é a do slide 3: corrente reativa injetada levanta a tensão "
        "(&#916;V &#8776; X&#183;i<sub>q</sub> em pu). Aqui i<sub>q</sub> é o módulo da "
        "injeção, como no ONS; no código e na Eq. (3.9) o sinal é o oposto "
        "(i<sub>q,ref</sub> = &#8722;2Q/3v<sub>d</sub>).")
sub("Fundamento: o círculo de corrente (exceção de método)")
eq(r"i_d^2 + i_q^2 \leq I_{max}^2 \ \Rightarrow\ i_d \leq \sqrt{I_{max}^2 - i_q^2}",
   onde="A corrente total é limitada pelos semicondutores. O reativo tem prioridade; o eixo "
        "d fica com o que sobra. Abaixo de 0,5 pu quase nada sobra, e a potência ativa cai "
        "durante a falta. Quando a falta é eliminada, a tensão volta à faixa normal, o "
        "reativo adicional zera e o ativo retorna ao patamar pré-falta.")
nums([["0,85 / 0,5 pu", "início da injeção reativa / saturação em 1 pu (Fig. 2.2); entre 0,85 e 1,1 pu, banda morta"]])
box("alem", "<b>O dilema que volta no capítulo 7 do painel.</b> Em pu, Q &#8776; "
    "V&#183;i<sub>q</sub>. Quanto mais a tensão cai, mais corrente reativa a regra pede, e "
    "menos potência reativa essa corrente consegue entregar.")
box("cuidado", "A sobretensão ficou fora do desenho de propósito: sobretensão e incremento "
    "de carga estão fora do escopo do trabalho inteiro.")
box("banca", "<b>Por que priorizar o reativo?</b> Sustenta a tensão sem exceder I<sub>max</sub>; "
    "eliminada a falta, o ativo retorna ao pré-falta.<br/>"
    "<b>Quem orienta as correntes?</b> O SRF-PLL. O bloco do ONS diz quanto de i<sub>d</sub> "
    "e i<sub>q</sub> injetar; o ângulo &#952;<sub>PLL</sub> diz em que direção.")
ponte("juntando todas as partes no sistema completo.")

# --- 16
slide(16, "Sistema completo", "Modelagem", "Victor, Bruno", "Fig. 4.2, §4.3.2")
box("msg", "Juntando as partes, este é o inversor usado em todas as simulações.")
fala(16)
sub("Revise em voz alta, de cima para baixo")
bul("<b>Sincronismo</b>: o SRF-PLL entrega &#952;<sub>PLL</sub> às transformações dq.",
    "<b>Referência pelo Submódulo 2.10</b>: antes fixas (P = 1 pu, Q = 0), i<sub>d,ref</sub> "
    "e i<sub>q,ref</sub> seguem a tensão V<sub>PCC</sub>.",
    "<b>Corrente e PWM</b>: os PIs em dq geram a modulação, e o LCL entrega a corrente à "
    "Barra 2.")
n.p("Uma forma de amarrar: são laços com velocidades parecidas, um dentro do outro. O PLL "
    "acomoda em cerca de 20 ms e a corrente em um ciclo (16,7 ms); o PWM chaveia a cada "
    "200 &#956;s. Se der para contar este slide sem olhar, a modelagem está estudada.")
box("banca", "<b>E agora?</b> Com o modelo fechado, as faltas no IEEE 9 barras testam o "
    "SRF-PLL.")
ponte("como as faltas foram aplicadas.")

# --- 17
slide(17, "Protocolo de contingência", "Método", "Bruno, Victor", "§4.3.4, Tab. 4.1, §5.2")
box("msg", "Todas as simulações seguem a mesma linha do tempo; muda só o local e o tipo da "
    "falta.")
sub("A linha do tempo")
tab(["Trecho", "Intervalo", "O que acontece"], [
    ["Inicialização", "0 a 0,1 s", "o modelo parte e o PLL trava; fora das métricas"],
    ["Pré-falta", "0,1 a 0,3 s", "regime, referência para as métricas em %"],
    ["Falta", "0,3 a 0,4 s", "100 ms = 6 ciclos de 60 Hz"],
    ["Pós-falta", "0,4 a 0,6 s", "200 ms de observação da recuperação"],
], [3.2, 3.0, 8.5])
sub("A matriz")
n.p("Analisadas, da mais próxima à mais distante da usina: Barra 7, Linha 7-8, Linha 8-9 e "
    "Barra 6 (em azul). Trifásica nos quatro; monofásica e bifásica nas Barras 7 e 6. "
    "Sintonia inadequada nas Barras 7 e 6 (os três tipos) e na Linha 7-8 (trifásica). "
    "Barras 4, 5, 8 e 9: simuladas, em cinza, consultáveis no painel. Regime sem falta nas "
    "duas sintonias.")
sub("Fundamento: os tipos de falta e as redes de sequência")
bul("<b>Trifásica</b>: simétrica; só a rede de sequência positiva participa. Afunda a "
    "tensão, sem sequência negativa.",
    "<b>Bifásica (fase-fase)</b>: as redes positiva e negativa ficam em paralelo no ponto "
    "da falta; ali, a tensão de sequência negativa iguala a positiva. É a que mais gera "
    "sequência negativa.",
    "<b>Monofásica (fase-terra)</b>: as três redes (positiva, negativa e zero) ficam em "
    "série; a de sequência zero divide a tensão, e a negativa sai menor que na bifásica.")
box("banca", "<b>Por que observar até 0,6 s?</b> São 200 ms após a eliminação; essa janela "
    "delimita o alcance das conclusões sobre a recuperação.")
box("cuidado", "Não diga quantos cenários: o slide também não diz (28 &#215; 29, "
    "defesa_qa.pdf). &#8220;Não retorna&#8221; significa &#8220;não retorna dentro da "
    "janela de 200 ms&#8221;. Os 0,1 s de inicialização são exceção de método.")
ponte("como os resultados foram extraídos.")

# --- 18
slide(18, "Fluxo de análise", "Método", "Bruno, Victor, Bruno", "§4.3.3; métricas em §5.1-5.3")
box("msg", "Cada simulação do Simulink vira arquivos CSV, tratados em Python até um painel "
    "interativo.")
n.p("Ao fim de cada simulação o Simulink exporta os sinais em duas taxas de amostragem; o "
    "Python alinha as duas num eixo de tempo comum e calcula os mesmos indicadores para "
    "todos os cenários. Nenhuma métrica é lida à mão no gráfico.")
sub("As cinco métricas (saiba definir cada uma)")
tab(["Métrica", "Definição"], [
    ["Retenção de V<sub>d</sub>", "v<sub>d</sub> durante a falta em % do valor pré-falta"],
    ["Pico do erro de fase", "maior |&#916;&#952;| na falta, depois do 1º ciclo (o salto "
     "do 1º ciclo é descartado)"],
    ["Retorno à faixa de 2°", "tempo contado da eliminação até o erro entrar de vez em "
     "&#177;2°"],
    ["Componente de 120 Hz", "amplitude no espectro de v<sub>d</sub> durante a falta"],
    ["P e Q", "médias no intervalo da falta"],
], [4.4, 10.3])
sub("Fundamento: o espectro")
n.p("O espectro é a transformada de Fourier de v<sub>d</sub> na janela da falta. A "
    "resolução em frequência é o inverso da duração da janela:")
eq(r"\Delta f = \frac{1}{T} = \frac{1}{0{,}1\ \mathrm{s}} = 10\ \mathrm{Hz}",
   onde="Com 6 ciclos inteiros, 60 e 120 Hz caem exatamente em pontos do espectro, sem "
        "vazamento. Por isso o gráfico do capítulo 4 tem pontos a cada 10 Hz.")
nums([["9,2%", "retenção de V<sub>d</sub> na Barra 7, trifásica, nominal (exemplo da fala)"]])
box("banca", "<b>Dos dados aos resultados.</b> É assim que lemos os resultados: abrimos agora "
    "o painel interativo ao vivo, no modo apresentação.")
ponte("slide 19, abrir o painel.")

# =============================================================================
# PARTE II
# =============================================================================
parte("PARTE II · A passagem para o painel")
slide(19, "Demonstração ao vivo", "Porta para o painel", "Victor", "Figs. 5.10, 5.18")
box("msg", "A partir daqui os resultados são mostrados no painel interativo, no modo "
    "apresentação.")
sub("O que fazer")
bul("Antes da defesa: abrir output/pll_metrics.html no navegador do notebook da defesa "
    "(abre sem internet).",
    "No slide 19: Alt+Tab para o navegador e clicar <b>Modo apresentação</b> no cabeçalho. "
    "O painel entra em tela cheia, com fundo branco.",
    "Seta &#8594; ou PageDown avança; seta &#8592; ou PageUp volta; Esc sai. Nos capítulos "
    "com passos, cada avanço revela um passo; só no último a seta troca de capítulo.",
    "O indicador de segmentos no canto superior direito mostra &#8220;k de n&#8221;.")
sub("O que aparece em todo capítulo")
n.p("Número do capítulo (k/8), a referência no TCC (seção, figura, tabela), o título, a "
    "frase do passo, chips com os casos (clicar liga e desliga), o gráfico e, embaixo, "
    "cartões com os números de cada caso. Clicar num cartão sai do palco e abre o cenário "
    "nas abas.")
box("cuidado", "O slide 19 funciona como porta direta para os oito capítulos do Modo Apresentação (Capítulos 1 a 8) antes resumem os três blocos do Modo Apresentação "
    "(Capítulos 1 a 3, Capítulos 4 e 5, e Capítulos 6 a 8), servindo de roteiro visual antes "
    "de alternar para o navegador.")

# =============================================================================
# PARTE III
# =============================================================================
n.pagebreak()
n.h("PARTE III · Painel HTML, modo apresentação")
n.p("Oito capítulos, na ordem do Cap. 5 do TCC. A sequência conta uma história: onde caem "
    "as faltas, como o PLL parte, o que a distância faz, o que a sequência negativa faz, "
    "como o ganho menor parece ajudar, como ele perde o sincronismo e o que isso diz sobre "
    "o código de rede.")
tab(["Cor", "Significado"], [
    ["azul / laranja", "sintonia nominal / inadequada"],
    ["amarelo &#8594; verde &#8594; ciano &#8594; índigo", "capítulos só com a nominal: do "
     "ponto mais perto ao mais longe da usina"],
    ["cor = barra, traço = curto", "capítulo 4: laranja B7, verde-azulado B6; contínuo "
     "bifásica, tracejado monofásica, grafite trifásica"],
    ["faixa verde", "&#177;2° no erro de fase; &#177;5% em v<sub>d</sub>"],
    ["fundo rosado", "intervalo da falta (0,3 a 0,4 s)"],
], [5.6, 9.1])

# --- 1
cap(1, "Faltas destacadas", "Antes dos resultados · 6 passos", "01_faltas_m2.png",
    "Passo 2 de 6: Barra 7 em destaque, cartão à direita e régua de severidade embaixo")
box("msg", "Quatro pontos de falta, do mais próximo ao mais distante da usina; a pergunta é "
    "como a distância muda a resposta do SRF-PLL.")
tab(["Passo", "Em cena", "O que explicar"], [
    ["1", "Visão geral", "Outros pontos também receberam falta; a análise fica em quatro, "
     "do afundamento mais profundo ao mais raso, com uma linha simples e uma dupla."],
    ["2", "Barra 7", "Logo depois do T2: entre o inversor e a falta só há o transformador. "
     "Caso mais severo; ponto de partida da perda de sincronismo. 3&#966;, 2&#966;, 1&#966;; "
     "duas sintonias."],
    ["3", "Linha 7-8", "Sai da Barra 7; circuito simples, a linha inteira fica sob falta; "
     "ainda perto. Só trifásica; duas sintonias."],
    ["4", "Linha 8-9", "Dois circuitos em paralelo, falta em um; o outro continua conduzindo. "
     "Só trifásica, só nominal."],
    ["5", "Barra 6", "Ramo inferior, entre B4 e B9; três linhas em qualquer caminho até "
     "ela. Caso mais brando, contraponto da B7. 3&#966;, 2&#966;, 1&#966;; duas sintonias."],
    ["6", "Resumo", "Ordem B7, L7-8, L8-9, B6; os quatro com trifásica; B7 e B6 também com "
     "mono e bifásica (capítulo 4)."],
], [1.3, 2.4, 11.0])
sub("Fundamento: distância elétrica")
n.p("Durante uma falta franca, a tensão no ponto do defeito vai a quase zero. A tensão que "
    "sobra no inversor depende de quanta impedância existe entre ele e a falta: é um "
    "divisor de tensão. Com só o T2 no meio (Barra 7), sobra pouco; com três linhas no "
    "caminho (Barra 6), sobra bem mais. &#8220;Distância&#8221; aqui é impedância, não "
    "quilômetro.")
box("cuidado", "A régua é proporcional à tensão residual na Barra 2, mas nenhum número "
    "aparece de propósito (não está no TCC). A Barra 6 é a mais distante, não a 8. "
    "<b>Reserva</b> sem painel: slide 17 (matriz).")

# --- 2
cap(2, "Energização do inversor", "§5.1 · Figura 5.3 · 2 passos", "02_energ_p2.png",
    "Passo 2 de 2: as duas sintonias, marcas de acomodação e o fasor")
box("msg", "Na partida, o SRF-PLL trava na rede: o erro de fase entra na faixa de 2° em "
    "40 ms com a nominal e em 79 ms com a inadequada, quase o dobro.")
box("passo", "<b>1.</b> Só a nominal, com foco na partida: 40 ms.",
    "<b>2.</b> Entra a inadequada: 79 ms. Embaixo, v<sub>d</sub> entra em &#177;5% do valor "
    "final em 34 e 42 ms.")
sub("Como ler o fasor")
n.p("O círculo à direita mostra o ângulo do PLL contra a rede: a marca preta no topo é a "
    "rede, a cunha verde é a faixa de &#177;2°, e cada vetor é uma sintonia. O play percorre "
    "a janela a partir de t = 0: os vetores giram até parar no topo, que é o travamento.")
sub("O que explicar")
n.p("A inadequada oscila mais e demora mais, como esperado de um laço mais lento e menos "
    "amortecido (&#958; = 0,316, &#969;<sub>n</sub> 2,24 vezes menor). Mas, em regime, as "
    "duas chegam ao mesmo ponto de operação, e a falta só começa em 0,3 s, com as duas "
    "travadas: <b>a inadequada é lenta, não quebrada</b>. A diferença só aparece nas "
    "contingências.")
nums([["40 / 79 ms", "erro na faixa de 2°, nominal / inadequada (Fig. 5.3)"],
      ["34 / 42 ms", "v<sub>d</sub> na faixa de 5%, nominal / inadequada"]])
box("cuidado", "Os primeiros milissegundos saem da escala porque a tensão ainda é nula; por "
    "isso a partida fica fora das métricas. <b>Reserva</b>: slide oculto 24.")

# --- 3
cap(3, "Localização: quanto mais perto, mais severa", "§5.2 · Tabela 5.1 · Figura 5.7 · "
    "3 passos", "03_local_p1.png",
    "Passo 1 de 3: foco na falta, mini-mapa com a retenção de v<sub>d</sub> de cada ponto")
box("msg", "A mesma falta trifásica em quatro pontos: quanto mais perto da usina, menos "
    "tensão sobra e maior o erro, mas com a sintonia nominal o erro sempre volta.")
box("passo", "<b>1.</b> v<sub>d</sub> retém 9,2% na Barra 7 e 58,4% na Barra 6 (mini-mapa).",
    "<b>2.</b> Pico do erro de 37,3° na Barra 7 e 7,3° na Barra 6 (fasor).",
    "<b>3.</b> Com a nominal, o erro sempre volta à faixa de 2°: em até 112 ms (sem foco).")
tab(["Ponto", "Retenção de V<sub>d</sub>", "Pico do erro", "Retorno a 2°"], [
    ["Barra 7", "9,2%", "37,3°", "98 ms"],
    ["Linha 7-8", "11,3%", "32,5°", "98 ms"],
    ["Linha 8-9", "47,1%", "29,8°", "112 ms"],
    ["Barra 6", "58,4%", "7,3°", "76 ms"],
], [4.2, 3.5, 3.5, 3.5])
sub("O que explicar")
n.p("Sem sequência negativa, a trifásica só reduz a amplitude e dá um salto de fase; o "
    "120 Hz fica entre 0,0002 e 0,0011 pu. O erro é transitório: o laço tipo 2 (slide 7) "
    "leva o erro de volta a zero. As setas no topo vão da eliminação (0,4 s) até o instante "
    "em que o erro entra de vez na faixa; B7 e L7-8 dividem a mesma seta (98 ms). O eixo do "
    "erro está em &#177;60°: corta só o salto do 1º ciclo, que a métrica de pico já "
    "descarta.")
box("prova", "<b>Por que a Linha 8-9 demora mais (112 ms) que a Barra 7, que é mais "
    "severa?</b> O retorno mede a recuperação depois da eliminação, que depende do "
    "transitório pós-falta de cada topologia, não só da profundidade do afundamento. "
    "Confira no §5.2 se o TCC atribui causa antes de afirmar qualquer uma.")
box("cuidado", "<b>Reserva</b>: slide oculto 25 (Tabela 5.1, Fig. 5.7).")

# --- 4
cap(4, "Sequência negativa", "§5.3 · Tabela 5.3 · Figura 5.10 · 5 passos",
    "04_seqneg_p2.png", "Passo 5 de 5: espectro de v<sub>d</sub> na falta, destaque "
    "&#8220;&gt; 250&#215;&#8221; e matriz barra &#215; curto")
box("msg", "Nas faltas assimétricas, a sequência negativa aparece em v<sub>d</sub> como "
    "120 Hz, de 0,29 a 0,72 pu: mais de 250 vezes o maior valor das trifásicas (0,0011 pu).")
box("passo", "<b>1.</b> Em v<sub>abc</sub> (Barra 6): na trifásica as três fases caem por igual; na bifásica ficam desequilibradas.",
    "<b>2.</b> Animação das sequências: o PLL gira com a positiva; a negativa gira ao contrário e, vista do PLL, dá a volta a 120 Hz.",
    "<b>3.</b> Em dq (v<sub>d</sub> e v<sub>q</sub> no tempo): a positiva vira constante e a negativa vira oscilação de 120 Hz só na bifásica.",
    "<b>4.</b> Entrada do PI (v<sub>q</sub> e erro de fase): o PI lê o 120 Hz como erro de fase (pico salta de 7,3° na trifásica para 96,0° na bifásica).",
    "<b>5.</b> No espectro de v<sub>d</sub>, o 120 Hz das assimétricas vai de 0,29 a 0,72 pu: mais de 250 vezes o das trifásicas.")
sub("Fundamento: de onde vem o pico em 120 Hz")
n.p("É a equação do slide 4 aparecendo no gráfico: a sequência negativa vira "
    "V<sup>&#8722;</sup>cos(2&#969;t) em v<sub>d</sub> e o mesmo em v<sub>q</sub>. O PLL não "
    "distingue essa ondulação de um erro de fase real: ela entra em v<sub>q</sub>, passa "
    "pelo PI (a 2,32&#183;&#969;<sub>n</sub>, quase dois terços passam) e contamina o ângulo, "
    "o referencial inteiro e as potências.")
tab(["120 Hz em v<sub>d</sub> (pico do erro)", "Trifásica", "Bifásica", "Monofásica"], [
    ["Barra 7", "0,0002 pu (37,3°)", "0,72 pu (180,0°)", "0,59 pu (89,7°)"],
    ["Barra 6", "0,0011 pu (7,3°)", "0,39 pu (96,0°)", "0,29 pu (12,0°)"],
], [5.0, 3.2, 3.3, 3.2])
n.p("Na bifásica da B7, o erro passa de 90° em 17,8% do intervalo com a nominal e em 14,0% "
    "com a inadequada: nenhuma preserva o alinhamento.")
box("prova", "<b>Por que não pôr um notch em 120 Hz?</b> Reduz a ondulação, mas um filtro "
    "dentro do laço também atrasa e reduz a banda, que é o recurso de que a recuperação "
    "precisa. A saída estrutural é separar as sequências antes do laço (DDSRF, DSOGI: "
    "trabalho futuro, slide 21).")
box("alem", "<b>Bifásica pior que monofásica:</b> é a ligação das redes de sequência do slide "
    "17 (paralelo na bifásica, série na monofásica). <b>Pico em 60 Hz em algumas curvas:</b> "
    "componente contínua transitória nas fases, vista em dq a 60 Hz (slide 6).")
box("cuidado", "<b>Reserva</b>: slide oculto 26 (Fig. 5.10).")

# --- 5
cap(5, "Compromisso da sintonia", "§5.3 · Tabela 5.3 · Figura 5.14 · 3 passos",
    "05_comp_p2.png", "Passo 2 de 3: Barra 6 bifásica, nominal e inadequada")
box("msg", "Na bifásica da Barra 6, o ganho menor filtra melhor o 120 Hz: o pico do erro cai "
    "de 96,0° para 34,5° e o retorno de 48 para 30 ms.")
box("passo", "<b>1.</b> Com a nominal, o 120 Hz da falta passa para o erro de fase: pico de "
    "96,0°.",
    "<b>2.</b> Com a inadequada, o 120 Hz em v<sub>d</sub> é quase o mesmo (0,39 e 0,37 pu), "
    "mas o erro fica em 34,5° e volta em 30 ms.",
    "<b>3.</b> Aqui, o ganho menor parece vantagem. E numa falta mais severa? (sem foco)")
sub("O que explicar")
n.p("A perturbação na tensão é a mesma nas duas; o que muda é quanto dela chega ao ângulo. "
    "Pela tabela do slide 11, a nominal deixa passar 0,63 do 120 Hz e a inadequada 0,13. Na "
    "Barra 6 a tensão positiva que sobra (v<sub>d</sub> médio de 0,72 pu) sustenta o "
    "sincronismo, e a filtragem vence.")
n.p("Mas o mesmo ganho menor deixa a recuperação lenta onde a tensão cai mais: na Barra 7 o "
    "retorno quase dobra (46 &#8594; 95 ms na monofásica, 51 &#8594; 96 ms na bifásica) e na "
    "trifásica da Barra 6 vai de 76 para 106 ms. <b>A frase-ponte do passo 3 é a virada da "
    "defesa</b>: o capítulo seguinte responde.")
box("cuidado", "<b>Reserva</b>: slide oculto 27 (Fig. 5.14, Tab. 5.3) e apêndice 23.")

# --- 6
cap(6, "Perda de sincronismo", "§5.4 · Figuras 5.18 e 5.19 · 3 passos", "06_sinc_p3.png",
    "Passo 3 de 3: erro de fase e P na Barra 7 trifásica; o &#8220;66,8%&#8221; fica sob "
    "o fasor")
box("msg", "Na Barra 7 trifásica, a sintonia decide o sincronismo: com a nominal o erro volta "
    "em 98 ms; com a inadequada percorre toda a faixa de &#177;180° até o fim, e a usina "
    "absorve potência ativa em 66,8% do tempo após a eliminação.")
box("passo", "<b>1.</b> O caso mais severo: com a nominal, o erro volta à faixa de 2° em 98 ms.",
    "<b>2.</b> A tensão retém quase o mesmo (9,2% e 8,2%), mas com a inadequada o erro "
    "percorre toda a faixa de &#177;180° (escorregamento de ciclo): perde o sincronismo.",
    "<b>3.</b> O ganho que filtrava o 120 Hz na Barra 6 é o que perde o sincronismo aqui.")
sub("Fundamento: escorregamento de ciclo")
n.p("O ângulo estimado deixa de acompanhar a rede e passa a girar em relação a ela: o erro "
    "varre &#177;180° sem parar, e cada &#8220;dente de serra&#8221; do gráfico é uma volta "
    "perdida. No fasor, o vetor laranja dá voltas enquanto o azul fica no topo.")
sub("Fundamento: por que P fica negativa")
n.p("É a equação do slide 12 com &#916;&#952; girando. Com a corrente comandada no eixo d:")
eq(r"P = \frac{3}{2}V\,i_d\cos\Delta\theta",
   onde="Modelo qualitativo (despreza o i<sub>q</sub> do ONS e a variação de V): se "
        "&#916;&#952; varre todos os ângulos, cos&#916;&#952; troca de sinal e P oscila "
        "entre positivo e negativo, como no gráfico de baixo. O número a citar é o medido: "
        "66,8% do tempo absorvendo, média &#8722;0,40 pu. A malha de corrente não falhou; o "
        "referencial é que está girando, e o inversor vira uma carga oscilante.")
sub("Fundamento: por que só a combinação colapsa")
n.p("Pela fórmula do slide 7, com U &#8776; 0,09 pu na falta (&#8730;U &#8776; 0,3):")
tab(["Na falta (U &#8776; 0,09 pu)", "&#969;<sub>n,ef</sub>", "&#958;<sub>ef</sub>"], [
    ["Nominal", "&#8776; 98 rad/s", "&#8776; 0,21"],
    ["Inadequada", "&#8776; 44 rad/s", "&#8776; 0,09"],
], [6.7, 4.0, 4.0])
n.p("A inadequada atravessa a falta praticamente sem amortecimento. Nenhum fator isolado "
    "explica o colapso: a nominal na Barra 7 recupera (98 ms) e a inadequada na trifásica "
    "da Barra 6 também (106 ms). O colapso aparece na combinação de falta severa com "
    "sintonia inadequada, e ocorre também na Linha 7-8 (retenção de 9,7%).")
nums([["9,2% / 8,2%", "retenção de V<sub>d</sub>, nominal / inadequada"],
      ["98 ms / não retorna", "retorno à faixa de 2° (dentro dos 200 ms)"],
      ["66,8%", "tempo pós-falta absorvendo potência ativa, inadequada (média &#8722;0,40 pu)"]])
box("cuidado", "A tabela de &#969;<sub>n,ef</sub> é conta de bolso (além do TCC). Os cartões "
    "do palco também mostram 44,0° (pico da inadequada) e 5,6% (P absorvida da nominal); o "
    "número de fala é o 66,8%. <b>Reserva</b>: slides ocultos 26 e 28 (Figs. 5.18 a 5.21).")

# --- 7
cap(7, "Código de rede", "§5.5 · Figuras 2.1 e 2.2 · Tabela 5.2 · 5 passos",
    "07_ons_p4.png", "Passo 2 de 5: Barra 7 realçada, caixa &#8220;0,09 pu&#8221; no ponto "
    "saturado da rampa")
box("msg", "O inversor cumpre a letra do Submódulo 2.10 nas trifásicas, mas permanecer "
    "conectado não basta.")
sub("Os dois painéis")
n.p("Esquerda: tensão da fase mais afundada no inversor contra a curva de suportabilidade "
    "(Fig. 2.1). Direita: a rampa da Fig. 2.2 (slide 15), com o ponto de operação de cada "
    "caso (V médio, i<sub>q,ref</sub> médio).")
tab(["Curva de suportabilidade (Fig. 2.1)", "Limite"], [
    ["inferior, de 0 a 0,5 s", "0,2 pu: abaixo disso a desconexão é permitida"],
    ["inferior, de 0,5 a 1 s", "rampa de 0,2 a 0,85 pu"],
    ["superior, até 2,5 s", "1,2 pu"],
], [6.7, 8.0])
box("passo", "<b>1.</b> Só a regra: permanecer conectado e injetar reativo conforme o "
    "afundamento.",
    "<b>2.</b> Barra 7 e Linha 7-8 + o dilema: tensão abaixo de 0,2 pu, desconexão permitida, "
    "e mesmo assim conectado com i<sub>q</sub> saturado em 1 pu; mas com a tensão abaixo de 10%, "
    "a corrente máxima entrega só 0,09 pu de reativo.",
    "<b>3.</b> Mais longe, a injeção acompanha o afundamento: na Barra 6, i<sub>q,ref</sub> médio "
    "de 0,72 pu contra 0,76 pu da rampa, entregando muito mais reativo.",
    "<b>4.</b> Outros curtos acesos: nas assimétricas e na perda de sincronismo o inversor "
    "também fica conectado, mas a potência carrega 120 Hz ou se inverte e drena energia.",
    "<b>5.</b> Cartão de fecho: &#8220;O inversor permaneceu conectado?&#8221; Essa pergunta "
    "é insuficiente: é preciso acompanhar o rastreamento angular durante toda a contingência "
    "e na recuperação.")
tab(["Ponto", "V média (pu)", "i<sub>q</sub> pela rampa", "i<sub>q,ref</sub> média"], [
    ["Barra 7", "0,10", "1,00", "1,00"],
    ["Linha 7-8", "0,11", "1,00", "1,00"],
    ["Linha 8-9", "0,48", "1,00", "0,99"],
    ["Barra 6", "0,58", "0,76", "0,72"],
], [4.2, 3.5, 3.5, 3.5])
sub("Fundamento: o dilema do passo 2")
eq(r"Q \approx V\cdot i_q \approx 0{,}09 \cdot 1{,}0 \approx 0{,}09\ \mathrm{pu}",
   onde="V entre 0,09 e 0,10 pu (0,10 na tabela, arredondado). A corrente é a máxima, mas "
        "a tensão não está lá para virar potência. Cumprir a regra e saturar a corrente "
        "quase não ajuda a rede.")
imagem_palco("07_ons_p6.png", "Passo 5 de 5: cartão de fecho, a tese do trabalho em uma "
             "tela", alt=6.2)
box("cuidado", "&#8220;Fora da região&#8221; da B7 e da L7-8 é leitura aprovada como exceção "
    "(o TCC não diz isso com essas palavras). As simulações acabam 0,3 s depois do início da "
    "falta, então só o patamar de 0,2 pu da curva tem dado. <b>Reserva</b>: slide oculto 29.")

# --- 8
cap(8, "Todos os casos", "Tabelas 5.1 a 5.3", "08_sintese.png",
    "Tabela com os indicadores de todos os casos do TCC")
box("msg", "Não é para apresentar linha por linha: é o ponto de apoio para as perguntas.")
n.p("Cada linha tem a seção do TCC (§5.1 a §5.4), e clicar nela abre o cenário nas abas. As "
    "linhas &#8220;não retorna&#8221; são a Barra 7 e a Linha 7-8 trifásicas inadequadas. "
    "As Barras 4, 5, 8 e 9 não estão aqui, mas estão nas abas por cenário.")
n.p("<b>Volta ao PowerPoint:</b> Esc (sai da tela cheia) e Alt+Tab para o slide 20.")

# =============================================================================
# PARTE IV
# =============================================================================
parte("PARTE IV · De volta ao PowerPoint")
slide(20, "Síntese dos resultados", "Conclusão", "Bruno, Victor, Bruno, Victor", "Cap. 6")
box("msg", "O sincronismo do SRF-PLL é uma decisão de estabilidade do sistema elétrico.")
sub("Os três pontos de apoio à conclusão")
bul("<b>1. Faltas simétricas</b>: com a sintonia nominal, o SRF-PLL reconverge em todos os "
    "pontos; a severidade do afundamento depende diretamente da distância elétrica até a usina.",
    "<b>2. Faltas assimétricas</b>: a fragilidade é estrutural: a componente de sequência "
    "negativa introduz oscilação de 120 Hz que o PI não rejeita, contaminando as potências "
    "injetadas P e Q.",
    "<b>3. Sensibilidade de ganhos</b>: reduzir os ganhos atenua a falta, mas retarda o "
    "restabelecimento e leva ao escorregamento de ciclo na B7, fazendo o inversor drenar "
    "potência da rede.")
sub("Fundamento: por que &#8220;decisão de estabilidade&#8221;")
n.p("A classificação clássica de estabilidade (ângulo, frequência, tensão) foi pensada para "
    "máquinas síncronas. A classificação estendida (Hatziargyriou et al., 2020, relatório IEEE PES TR77) "
    "acrescenta a <b>estabilidade guiada por conversores</b>, causada pela interação entre o "
    "controle do conversor, como o PLL, e a rede. O que o TCC mostra cabe nela: a sintonia "
    "do PLL, que costuma ser tratada como detalhe do equipamento, decide se a usina sustenta "
    "ou drena a rede numa falta.")
box("banca", "<b>Qual é a conclusão central?</b> Permanecer conectado é insuficiente: a "
    "conformidade deve auditar o erro angular dinâmico durante a falta e em toda a "
    "recomposição.")
box("cuidado", "No slide 20, os três cartões destacam diretamente os três pontos conceituais "
    "de apoio à conclusão (sem números isolados no topo), pois todos os indicadores quantitativos "
    "acabaram de ser percorridos no painel interativo.")
ponte("o que fica para depois.")

slide(21, "Trabalhos futuros e encerramento", "Conclusão", "Victor, Bruno, Victor", "Cap. 7")
box("msg", "Dois eixos dão continuidade ao estudo, a partir dos limites deste trabalho.")
sub("Eixo 1: estruturas de sincronismo")
n.p("A fragilidade do capítulo 4 vem de o SRF-PLL misturar as duas sequências no mesmo "
    "v<sub>q</sub>. As alternativas separam antes do laço:")
bul("<b>DDSRF-PLL</b> (referencial síncrono duplo desacoplado): usa dois referenciais, um a "
    "+&#969; e outro a &#8722;&#969;, e uma rede de desacoplamento que tira de cada um a "
    "ondulação causada pelo outro. O PLL roda só sobre a sequência positiva.",
    "<b>DSOGI-PLL</b> (integrador generalizado de segunda ordem duplo): filtros SOGI geram "
    "versões em quadratura das tensões em &#945;&#946;, um cálculo de sequência positiva "
    "extrai só a positiva, e o SRF-PLL comum trabalha sobre ela.")
n.p("Nos dois casos, o 120 Hz deixa de entrar em v<sub>q</sub> sem precisar reduzir a banda: "
    "é a saída para o compromisso dos capítulos 5 e 6.")
sub("Eixo 2: força da rede e múltiplos inversores")
n.p("Varrer a impedância de Thévenin (SCR, slide 8) para mapear a fronteira de perda de "
    "sincronismo e substituir mais máquinas síncronas por conversores, para estudar a "
    "interação entre vários PLLs em rede fraca.")
sub("Limites (diga sem defensividade)")
n.p("IEEE 9 barras com nível de curto fixo, duas sintonias contrastantes, janela de 200 ms "
    "pós-falta: o trabalho identifica e explica um mecanismo, não um envelope universal de "
    "projeto.")
box("cuidado", "Eixos de salto de fase e RoCoF foram descartados: não proponha.")
ponte("agradecimento e abertura para perguntas, com o painel aberto.")

# =============================================================================
# PARTE V
# =============================================================================
parte("PARTE V · Conteúdo adicional",
      "O apêndice do deck (slides 22 e 23) e os slides ocultos (24 a 29) não fazem parte da "
      "apresentação. Servem de apoio quando a banca pergunta algo que pede número de "
      "parâmetro ou a tabela completa. Vale conhecê-los para saber que existem e onde estão.")

slide(22, "Parâmetros: rede, filtro LCL e controle", "Apêndice", "não tem fala",
      "Cap. 3 e 4")
box("msg", "Todos os parâmetros do modelo num slide: base do sistema, conversor, Thévenin, "
    "filtro LCL e ganhos das duas malhas.")
tab(["Quando a banca perguntar", "Onde está no slide"], [
    ["Tensão do barramento CC", "coluna 1: 136,36 kV (1,5 &#215; 90,91 kV do cálculo)"],
    ["Impedância de Thévenin", "coluna 1: R<sub>th</sub> = 10,04 m&#937;, L<sub>th</sub> = "
     "1,16 mH"],
    ["Passo de integração", "coluna 1: 5 &#956;s (elétrico) e 200 &#956;s (controle)"],
    ["L<sub>1</sub>, L<sub>2</sub>, C<sub>f</sub>, R<sub>d</sub>",
     "coluna 2: 30,42 mH, 0,289 mH, 42,47 &#956;F e as resistências de amortecimento"],
    ["Ganhos de corrente e do PLL", "coluna 3: 14,74 e 3.537,8 (corrente); 460 e 105.820; "
     "92 e 21.164"],
], [5.0, 9.7])
box("cuidado", "Vários desses valores não estão no TCC (são do modelo). Por que o "
    "V<sub>cc</sub> é 1,5 vezes o do cálculo: com o valor do cálculo, o PWM senoidal "
    "sobremodulava na escala de 100 MW.")

slide(23, "Tabelas 5.1, 5.2 e 5.3 completas", "Apêndice", "não tem fala", "Cap. 5")
box("msg", "As três tabelas do Cap. 5 num slide: trifásicas com o suporte do ONS e "
    "assimétricas nas duas sintonias.")
n.p("É a mesma informação do capítulo 8 do painel, em formato de slide. Use quando o painel "
    "não estiver à mão. O cartão de baixo resume por que o efeito da sintonia se inverte "
    "entre a Barra 6 (a inadequada filtra melhor) e a Barra 7 (a inadequada recupera "
    "devagar): é a história dos capítulos 5 e 6.")
box("cuidado", "O cartão da esquerda menciona um ganho efetivo &#8220;12 vezes&#8221; menor; "
    "prefira a explicação do capítulo 6 deste roteiro (&#969;<sub>n</sub> e &#958; caem com "
    "&#8730;U).")

n.h("Slides ocultos: a reserva do painel")
tab(["Slide", "Substitui o capítulo", "Conteúdo"], [
    ["24", "2 · Energização", "Fig. 5.3, 34/40 ms e 42/79 ms"],
    ["25", "3 · Localização", "Fig. 5.7 e Tabela 5.1"],
    ["26", "4 · Sequência negativa", "Figs. 5.10 e 5.18, 250&#215;, 98 ms"],
    ["27", "5 · Compromisso", "Fig. 5.14 e a parte assimétrica da Tabela 5.3"],
    ["28", "6 · Perda de sincronismo", "Figs. 5.20 e 5.21, 66,8%, média &#8722;0,40 pu"],
    ["29", "7 · Código de rede", "Fig. 2.2 e Tabela 5.2, 0,09 pu"],
], [1.6, 5.0, 8.1])
n.p("Se o navegador falhar, mostre esses slides na ordem da tabela (indo direto pelo número) "
    "e siga o mesmo roteiro da Parte III.")

n.h("Outros materiais")
tab(["Material", "Para quê"], [
    ["defesa_qa.pdf", "respostas prontas para os pontos em que deck e TCC se cruzam "
     "(contagem de cenários, 22.547 &#215; 23.368 MW, sobrecorrentes, grid-forming)"],
    ["criterio_acomodacao_srf_pll.pdf", "por que o critério de 1% no t<sub>s</sub>"],
    ["sintonia_srf_pll_nota_tecnica.pdf", "derivação completa dos ganhos do PLL"],
    ["medicao_escorregamento_srf_pll.pdf", "como o escorregamento de ciclo é medido"],
], [5.6, 9.1])

# =============================================================================
n.pagebreak()
n.h("Folha de números")
tab(["Grupo", "Número", "O que é"], [
    ["Motivação", "23.368 MW (34,5%); 265 GW&#183;s", "Brasil 2023: carga perdida; inércia"],
    ["", "> 2,5 GW; 0,63 Hz", "Ibéria 2025"],
    ["", "11.066 MW; 73%", "Chile 2025"],
    ["Modelo", "100 MW = 1 pu; 100 MVA; 60 Hz", "UFV na Barra 2 (era G2 de 192 MVA)"],
    ["", "16.329,93 V", "pico nominal de fase, base do pu do PLL"],
    ["", "5 kHz; 30,71 mH; 9.068,99 rad/s", "PWM; L<sub>est</sub>; ressonância do LCL"],
    ["PLL nominal", "460; 105.820", "K<sub>p</sub>; K<sub>i</sub>"],
    ["", "325,3 rad/s (51,8 Hz); 0,707; 20 ms", "&#969;<sub>n</sub>; &#958;; t<sub>s</sub>"],
    ["PLL inadequada", "92; 21.164", "&#215; 0,2"],
    ["", "145,5 rad/s; 0,316", "&#969;<sub>n</sub>; &#958;"],
    ["", "754 rad/s = 2,32&#183;&#969;<sub>n</sub>", "120 Hz contra a banda nominal"],
    ["Protocolo", "0,1 / 0,3 / 0,4 / 0,6 s", "inicialização / falta / eliminação / fim"],
    ["Energização", "40 / 79 ms; 34 / 42 ms", "erro em 2°; v<sub>d</sub> em 5%"],
    ["Trifásicas", "9,2 / 11,3 / 47,1 / 58,4%", "retenção B7 / L7-8 / L8-9 / B6"],
    ["", "37,3 / 32,5 / 29,8 / 7,3°", "pico do erro"],
    ["", "98 / 98 / 112 / 76 ms", "retorno a 2°"],
    ["", "0,0002 a 0,0011 pu", "120 Hz nas trifásicas"],
    ["Assimétricas", "0,29 a 0,72 pu; &gt; 250&#215;", "120 Hz em v<sub>d</sub>"],
    ["", "17,8% / 14,0%", "tempo com erro &gt; 90°, B7 bifásica, nom. / inad."],
    ["Compromisso", "96,0° &#8594; 34,5°; 48 &#8594; 30 ms", "B6 bifásica, pico; retorno"],
    ["", "46 &#8594; 95; 51 &#8594; 96; 76 &#8594; 106 ms", "retorno B7 mono; B7 bi; B6 tri"],
    ["Sincronismo", "9,2% / 8,2%; 98 ms / não retorna", "B7 trifásica nom. / inad."],
    ["", "66,8% (média &#8722;0,40 pu); 9,7%", "P absorvida, inadequada; retenção L7-8 inad."],
    ["ONS", "(0,85 &#8722; V)/0,35; 0,5 pu", "rampa; saturação em 1 pu"],
    ["", "0,10 pu &#8594; Q = 0,09 pu; 0,72 contra 0,76",
     "B7: tensão e reativo; B6: i<sub>q,ref</sub> contra a rampa"],
], [2.8, 5.6, 6.3])

out = n.build()
print(out)
if "--preview" in sys.argv:
    print(render_preview(out, sys.argv[sys.argv.index("--preview") + 1]))
