import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Temp\tcc_banca\unpacked\word\document.xml', 'r', encoding='utf-8') as f:
    text = f.read()

pos_body = 386321
p_start = text.rfind('<w:p ', 0, pos_body)
idx_next = text.find('w:val="Ttulo', pos_body + 100)
p_end = text.rfind('<w:p ', 0, idx_next)

sub = text[p_start:p_end]
paras = re.findall(r'<w:p\b[^>]*>.*?</w:p>', sub, re.S)
print(f'Number of paragraphs in 2.1.4: {len(paras)}')
for i, p in enumerate(paras):
    clean = re.sub(r'<[^>]+>', '', p)
    print(f'P{i}: {clean[:100]}')

