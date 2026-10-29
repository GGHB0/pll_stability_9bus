"""Guia de estudos e roteiro de fala da defesa (.docx).

Roda o mesmo conteudo/ do roteiro de estudo em PDF, desviando cada bloco para o
Word, e acrescenta as falas cronometradas (falas/), o cronograma de 30 min, o mapa
do TCC, os slides de reserva e as perguntas da banca.
Saída: output/Roteiro_e_Guia_de_Estudos_Defesa_TCC.docx + cópia no OneDrive.
"""
from caminhos import OUTPUT, conteudo_texto, entregar, salvar
from gw_builder import WordRoteiroBuilder
from gw_hooks import ambiente
from gw_util import *  # noqa: F401,F403

NOME = "Roteiro_e_Guia_de_Estudos_Defesa_TCC.docx"


def main():
    doc = Document()
    for section in doc.sections:
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)
        section.top_margin = Cm(1.6)
        section.bottom_margin = Cm(1.6)
        section.left_margin = Cm(2.0)
        section.right_margin = Cm(2.0)

    wb = WordRoteiroBuilder(doc)

    # Cabeçalho principal
    wb.add_header_banner(
        title="Roteiro e Guia Completo de Estudo da Defesa (30 Minutos)",
        subtitle="Slide a slide e capítulo a capítulo, na ordem em que a apresentação acontece "
                 "(PPTX 1–20, Painel HTML Modo Apresentação 1–8 e volta ao PPTX 21–22), com os "
                 "fundamentos de cada tema, a sequência do TCC e as falas completas cronometradas",
        meta_left="<b>Victor Hugo de Avelar Rezende e Bruno Henrique de Oliveira</b><br/>"
                  "Comportamento do SRF-PLL de Inversores Frente a Contingências em Sistemas Elétricos",
        meta_right="<b>Guia Final Unificado (Word + Palco)</b><br/>26 de outubro de 2026",
    )

    exec_env = ambiente(wb)
    # o laço numerado da abertura usa Paragraph() do reportlab: vira item de lista no Word
    body_code = conteudo_texto().replace(
        'n.story.append(Paragraph(f, S_BUL, bulletText=f"{i}."))', 'wb_bul_num(i, f)')
    exec_env["wb_bul_num"] = lambda i, f: wb.bul(f, numbered=False) if i == 0 else wb.p(f"<b>{i}.</b> {f}")
    exec(body_code, exec_env)

    entregar(salvar(doc, OUTPUT / NOME), NOME)


if __name__ == "__main__":
    main()
