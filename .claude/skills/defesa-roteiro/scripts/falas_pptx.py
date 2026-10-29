"""Falas da defesa em PPTX: um slide por item, só com a fala (apoio de ensaio).

Ordem da apresentação: slides 1-18, palco 1-8, slides 19-20, já na numeração do
deck atual. Termos e números-chave saem em negrito (DESTAQUES). Texto em falas/.
Saída: output/Falas_Defesa_TCC.pptx + cópia no OneDrive.
"""
import re

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt

from caminhos import OUTPUT, entregar
from falas import PALCO_ROTEIRO, SLIDES_CONCLUSAO, SLIDES_ROTEIRO

NOME = "Falas_Defesa_TCC.pptx"

AZUL = RGBColor(0x1F, 0x4E, 0x79)
CINZA = RGBColor(0x59, 0x59, 0x59)
ALERTA = RGBColor(0xE0, 0x18, 0x2D)  # vermelho: o que se bate o olho para não esquecer
COR = {"Bruno": RGBColor(0x1F, 0x6F, 0xB4), "Victor": RGBColor(0x0F, 0x8A, 0x7E)}

# Numeração da skill (deck antigo, com a bancada no 9) → numeração do deck atual:
# a bancada virou cartão do slide 8, e do 10 em diante tudo desce uma posição.
def no_deck(n):
    return n if n <= 8 else n - 1


itens = (
    [(f"Slide {no_deck(it['num'])}", it) for it in SLIDES_ROTEIRO if it["num"] != 9]
    + [(f"Painel · Cap. {it['num']}", it) for it in PALCO_ROTEIRO]
    + [(f"Slide {no_deck(it['num'])}", it) for it in SLIDES_CONCLUSAO]
)

# Negrito vermelho no que escapa da memória na hora: números com unidade (pela regex
# NUMERO), nomes, datas, locais, listas e as frases-chave. Conceito que ninguém esquece
# ("SRF-PLL", "sintonia nominal") fica sem destaque, para o vermelho não perder força.
DESTAQUES = sorted([
    # contexto e eventos
    "cinco blocos", "professor Oscar", "professor André", "micro e minigeração",
    "15 de agosto de 2023", "Quixadá e Fortaleza II", "descartou falta de inércia",
    "colapso foi de tensão", "Península Ibérica", "sobretensão", "Chile",
    "11 mil megawatts", "de 48 para 30 milissegundos",
    "controle e o sincronismo dos inversores", "cadeia causal", "desvio angular",
    # modelagem
    "barramento CC ideal", "filtro de acoplamento LCL", "VCO", "segunda ordem",
    "G1 e G3", "Barra 2", "equivalente de Thévenin", "PSIM", "fontes ideais",
    "0,707", "0,316", "critério de 1%", "Kp igual a 460", "Ki igual a 105.820",
    "reduzindo esses ganhos em 80%", "quatro passos", "notch", "um ciclo da rede",
    "separação funcional", "decide quanto injetar", "decide em que direção",
    "0,85", "regra de prioridade", "o que sobra", "Figura 4.2",
    # método e resultados
    "retenção de tensão", "pico de erro de fase", "tempo de retorno definitivo",
    "oscilação de 120 hertz", "as potências médias",
    "Barra 7", "Linha 7-8", "Linha 8-9", "circuito duplo", "Barra 6",
    "três linhas de transmissão", "Teorema de Fortescue", "velocidade dupla",
    "espectro de Fourier", "escorregamento de ciclo", "mais a menos 180 graus",
    "virando uma carga", "curva de suportabilidade", "dilema físico", "potência suja",
    "permanecer conectado não basta", "auditar o rastreamento angular",
    "perguntar se o inversor permaneceu conectado é insuficiente",
    "fragilidade é estrutural", "erro angular dinâmico",
    "DDSRF", "DSOGI-PLL", "relação de curto-circuito", "redes fracas",
], key=len, reverse=True)
UNIDADES = ("terawatts-hora|gigawatts|megawatts|quilovolts|milissegundos|segundos?|graus|"
            "radianos por segundo|quilohertz|hertz|milihenries|p\\.u\\.|vezes|ciclos|%")
NUMERO = rf"\d+(?:[.,]\d+)*\s?(?:{UNIDADES})"
PADRAO = re.compile("|".join([re.escape(t) for t in DESTAQUES] + [NUMERO]))


def corrido(par, texto, tam, cor):
    """Escreve o texto, pondo em negrito vermelho os trechos de DESTAQUES e os números."""
    pos = 0
    for m in PADRAO.finditer(texto):
        if m.start() > pos:
            run(par, texto[pos:m.start()], tam, cor)
        run(par, m.group(), tam, ALERTA, True)
        pos = m.end()
    if pos < len(texto):
        run(par, texto[pos:], tam, cor)

def caixa(slide, x, y, w, h):
    tf = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)).text_frame
    tf.word_wrap = True
    return tf


def run(par, texto, tam, cor, negrito=False):
    r = par.add_run()
    r.text = texto
    r.font.size, r.font.bold, r.font.name = Pt(tam), negrito, "Calibri"
    r.font.color.rgb = cor



def main():
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    vazio = prs.slide_layouts[6]

    capa = prs.slides.add_slide(vazio)
    tf = caixa(capa, 0.8, 2.6, 11.7, 2.4)
    run(tf.paragraphs[0], "Falas da defesa", 44, AZUL, True)
    run(tf.add_paragraph(), "Comportamento do SRF-PLL de Inversores Frente a Contingências em Sistemas Elétricos", 22, CINZA)
    p = tf.add_paragraph()
    run(p, "Bruno", 20, COR["Bruno"], True)
    run(p, "  ·  ", 20, CINZA)
    run(p, "Victor", 20, COR["Victor"], True)
    p = tf.add_paragraph()
    p.space_before = Pt(18)
    run(p, "Em vermelho: ", 18, ALERTA, True)
    run(p, "números, nomes e frases-chave para bater o olho e não esquecer.", 18, CINZA)

    for rotulo, it in itens:
        s = prs.slides.add_slide(vazio)
        barra = s.shapes.add_shape(1, 0, 0, prs.slide_width, Inches(0.12))
        barra.fill.solid()
        barra.fill.fore_color.rgb = AZUL
        barra.line.fill.background()

        tf = caixa(s, 0.6, 0.3, 12.1, 0.9)
        run(tf.paragraphs[0], f"{rotulo}  ", 16, CINZA, True)
        titulo = re.sub(r"\s*\((NOVO|Mapa|Tabelas|Conclusão)[^)]*\)", "", it["titulo"])
        run(tf.paragraphs[0], titulo, 26, AZUL, True)

        n = sum(len(t) for _, t in it["falas"])
        tam = 28 if n < 600 else 26 if n < 800 else 24 if n < 1000 else 22 if n < 1200 else 20
        tf = caixa(s, 0.6, 1.3, 12.1, 5.9)
        primeiro = True
        for quem, texto in it["falas"]:
            texto = re.sub(r"\s*(\(Seta →[^)]*\))\s*", r"\n\n\1 ", texto).strip()
            for k, bloco in enumerate(texto.split("\n\n")):
                p = tf.paragraphs[0] if primeiro else tf.add_paragraph()
                primeiro = False
                p.space_after = Pt(8)
                if k == 0:
                    run(p, f"{quem}: ", tam, COR[quem], True)
                m = re.match(r"(\(Seta →[^)]*\)) ?(.*)", bloco, re.S)
                if m:
                    run(p, m.group(1) + " ", tam - 4, CINZA, True)
                    bloco = m.group(2)
                corrido(p, bloco, tam, RGBColor(0x26, 0x26, 0x26))

    saida = OUTPUT / NOME
    try:
        prs.save(saida)
    except PermissionError:
        saida = saida.with_name(saida.stem + "_atualizado" + saida.suffix)
        prs.save(saida)
    print(f"[OK] Salvo em: {saida} ({len(prs.slides)} slides)")
    entregar(saida, NOME)


if __name__ == "__main__":
    main()
