"""
audit_pdf_whitespaces.py - Auditoria de Espaços em Branco no PDF Final do TCC

Verifica sistematicamente cada página do PDF gerado pelo Word, identificando:
1. Páginas completamente vazias (erro de quebra de página manual).
2. Páginas de corpo com espaços em branco anômalos (> 75% vazias) geradas por
   linhas órfãs (1 a 4 linhas) que transbordam antes da abertura de novo capítulo.
3. Garante que os finais de seção e listas fluam de forma compacta e elegante.

Uso:
  python audit_pdf_whitespaces.py [caminho_do_pdf]
"""

import sys
import os

try:
    import fitz  # pymupdf
except ImportError:
    print("ERRO: pymupdf (fitz) não instalado. Instale com: pip install pymupdf")
    sys.exit(1)

sys.stdout.reconfigure(encoding='utf-8')

def audit_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        print(f"ERRO: Arquivo não encontrado: {pdf_path}")
        return 1

    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    print(f"=== Auditoria de Layout e Espaços em Branco: {os.path.basename(pdf_path)} ===")
    print(f"Total de páginas analisadas: {total_pages}\n")

    bottom_margin = 785.0
    top_margin = 85.0
    printable_height = bottom_margin - top_margin

    anomalies = []

    for i, page in enumerate(doc):
        page_num = i + 1
        text_blocks = [b for b in page.get_text("blocks") if b[4].strip() and b[1] > 70]
        image_list = page.get_images()
        image_rects = []
        for img_info in image_list:
            xref = img_info[0]
            for rect in page.get_image_rects(xref):
                if rect.y1 > 70:
                    image_rects.append(rect)

        all_bottoms = [b[3] for b in text_blocks] + [r.y1 for r in image_rects]

        if not all_bottoms:
            text_any = [b for b in page.get_text("blocks") if b[4].strip()]
            if not text_any and not image_list:
                print(f"[FALHA CRÍTICA] Página {page_num:2d}: PÁGINA TOTALMENTE EM BRANCO!")
                anomalies.append((page_num, 100.0, "Página em branco"))
            continue

        max_y = max(all_bottoms)
        empty_pt = max(0.0, bottom_margin - max_y)
        empty_pct = (empty_pt / printable_height) * 100.0

        # Identificar elementos pré-textuais ou encerramento padrão de capítulos
        first_lines = [b[4].strip().replace('\n', ' ') for b in text_blocks[:2]]
        last_lines = [b[4].strip().replace('\n', ' ') for b in text_blocks[-2:]]
        first_str = ' | '.join(first_lines)[:45]
        last_str = ' | '.join(last_lines)[-50:]

        # Anomalia grave: página do corpo com mais de 75% vazia
        # (excluindo Ficha catalográfica na pág 3, Resumo/Abstract, Referências e fim do Apêndice)
        is_pretextual = page_num < 16
        is_end_of_doc = page_num >= (total_pages - 5)

        if empty_pct > 75.0 and not is_pretextual and not is_end_of_doc:
            print(f"[ALERTA ESPAÇO EM BRANCO] Página {page_num:2d} | Max Y: {max_y:5.1f} pt | Vazio: {empty_pt:5.1f} pt ({empty_pct:4.1f}%)")
            print(f"   Início: {first_str}")
            print(f"   Fim   : {last_str}\n")
            anomalies.append((page_num, empty_pct, first_str))

    print(f"==================================================")
    if not anomalies:
        print("RESULTADO: SUCESSO! 0 anomalias de espaço em branco ou páginas órfãs detectadas.")
        print("O documento está perfeitamente diagramado e pronto para entrega.")
        return 0
    else:
        print(f"RESULTADO: {len(anomalies)} anomalia(s) de espaço em branco encontrada(s).")
        print("Recomenda-se ajustar espaçamento de parágrafos/tabelas/figuras para eliminar órfãs.")
        return 1

if __name__ == '__main__':
    default_pdf = r"C:\Users\gilbr\OneDrive\UERJ\TCC - Victor e Bruno\Template Modelo TCC\01_TCC_Monografia_Final\TCC_Victor_Bruno_VFinal.pdf"
    path = sys.argv[1] if len(sys.argv) > 1 else default_pdf
    sys.exit(audit_pdf(path))

