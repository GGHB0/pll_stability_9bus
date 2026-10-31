import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Temp\tcc_banca\unpacked\word\document.xml', 'r', encoding='utf-8') as f:
    text = f.read()

# Test Section remissions in text:
def renum_sec_match(m):
    prefix = m.group(1) # 'Seção' or 'Seções'
    sec = m.group(2)
    parts = sec.split('.')
    first = int(parts[0])
    if first in (2, 3, 4, 5):
        new_first = first - 1
        return f"{prefix} {new_first}." + ".".join(parts[1:])
    return m.group(0)

text = re.sub(r'\b(Seções|Seção)\s+([2-5]\.\d+(?:\.\d+)*)\b', renum_sec_match, text)

# Chapters:
text = text.replace("no Capítulo 2", "na Seção 1")
text = text.replace("do Capítulo 2", "da Seção 1")
text = text.replace("Capítulo 2,", "Seção 1,")
text = text.replace("no Capítulo 3", "na Seção 2")
text = text.replace("do Capítulo 3", "da Seção 2")
text = text.replace("Capítulo 3 ", "Seção 2 ")
text = text.replace("no Capítulo 4", "na Seção 3")
text = text.replace("do Capítulo 4", "da Seção 3")
text = text.replace("Capítulo 4 ", "Seção 3 ")
text = text.replace("no Capítulo 5", "na Seção 4")
text = text.replace("do Capítulo 5", "da Seção 4")
text = text.replace("Capítulo 5 ", "Seção 4 ")
text = text.replace("no Capítulo 6", "na Conclusão")
text = text.replace("do Capítulo 6", "da Conclusão")
text = text.replace("Capítulo 6 ", "Conclusão ")
text = text.replace("Capítulo 7", "seção de Trabalhos Futuros")

# And handle the split run:
text = text.replace(
    'no Capítulo </w:t></w:r><w:r><w:lastRenderedPageBreak/><w:t>3:',
    'na Seção </w:t></w:r><w:r><w:lastRenderedPageBreak/><w:t>2:'
)

clean_text = re.sub(r'<[^>]+>', '', text)
print('--- Remaining Capítulos: ---')
for m in re.finditer(r'Capítulo\s*[0-9]?', clean_text):
    start = max(0, m.start() - 30)
    end = min(len(clean_text), m.end() + 30)
    print(clean_text[start:end])

print('--- Seção remissions in clean text: ---')
for m in re.finditer(r'Seç[oõ]es?\s+[1-5]\.[0-9]+(?:\.[0-9]+)*', clean_text):
    start = max(0, m.start() - 20)
    end = min(len(clean_text), m.end() + 20)
    print(clean_text[start:end])

