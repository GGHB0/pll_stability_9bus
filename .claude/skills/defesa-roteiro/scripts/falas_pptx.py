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
COR = {"Bruno": RGBColor(0x1F, 0x6F, 0xB4), "Victor": RGBColor(0xD9, 0x6C, 0x00)}

# Numeração da skill (deck antigo, com a bancada no 9) → numeração do deck atual:
# a bancada virou cartão do slide 8, e do 10 em diante tudo desce uma posição.
def no_deck(n):
    return n if n <= 8 else n - 1


itens = (
    [(f"Slide {no_deck(it['num'])}", it) for it in SLIDES_ROTEIRO if it["num"] != 9]
    + [(f"Painel · Cap. {it['num']}", it) for it in PALCO_ROTEIRO]
    + [(f"Slide {no_deck(it['num'])}", it) for it in SLIDES_CONCLUSAO]
)

# Termos e números-chave em negrito (o mais longo primeiro, para não partir expressões).
DESTAQUES = sorted([
    "SRF-PLL", "transformada de Park", "sintonia nominal", "sintonia inadequada",
    "reduzindo esses ganhos em 80%", "reduzir os ganhos", "sequência negativa", "sequência positiva",
    "120 hertz", "escorregamento de ciclo", "Submódulo 2.10", "equivalente de Thévenin",
    "filtro LCL", "Teorema de Fortescue", "erro angular dinâmico", "rastreamento angular",
    "distância elétrica", "fragilidade é estrutural", "permanecer conectado não basta",
    "perguntar se o inversor permaneceu conectado é insuficiente", "virando uma carga",
    "compromisso de filtragem", "separação funcional", "decide quanto injetar", "decide em que direção",
    "fator de amortecimento em 0,707", "Kp igual a 460", "Ki igual a 105.820",
    "20 para 100 milissegundos", "5 vezes mais lento", "9.068 radianos por segundo",
    "23.368 megawatts", "34,5% da carga nacional", "96,8 gigawatts", "100 megawatts",
    "9,2%", "58,4%", "37 graus", "7 graus", "96 graus", "34,5 graus", "0,72 p.u.",
    "250 vezes", "66,8%", "0,09 p.u.", "40 milissegundos", "79 milissegundos",
    "98 milissegundos", "112 milissegundos", "0,3 segundos", "6 ciclos", "200 milissegundos",
    "cinco métricas", "DDSRF", "DSOGI-PLL", "relação de curto-circuito",
    "colapso foi de tensão", "controle e o sincronismo dos inversores",
    "oscilação de 120 hertz", "desvio angular",
], key=len, reverse=True)
PADRAO = re.compile("|".join(re.escape(t) for t in DESTAQUES))


def corrido(par, texto, tam, cor):
    """Escreve o texto, pondo em negrito os trechos de DESTAQUES."""
    pos = 0
    for m in PADRAO.finditer(texto):
        if m.start() > pos:
            run(par, texto[pos:m.start()], tam, cor)
        run(par, m.group(), tam, AZUL, True)
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
