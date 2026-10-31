import fitz, sys
sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r'C:\Users\gilbr\.gemini\antigravity\brain\99efb55e-396a-47dd-b76b-64d8c3d024b9\.user_uploaded\media_1793298637318_ef89fa75.pdf'
doc = fitz.open(pdf_path)
print(f'Total pages: {len(doc)}')

annot_count = 0
for page_num in range(len(doc)):
    page = doc[page_num]
    annots = list(page.annots())
    if annots:
        print(f'Page {page_num + 1}: {len(annots)} annotations')
        for a in annots:
            info = a.info
            content = info.get('content', '')
            print(f'   Type: {a.type[1]}, Subj: {info.get("subject", "")}, Content: {content[:100]}')
        annot_count += len(annots)

print(f'Total annotations found: {annot_count}')

