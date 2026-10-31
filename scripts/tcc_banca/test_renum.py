import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Temp\tcc_banca\unpacked\word\document.xml', 'r', encoding='utf-8') as f:
    text = f.read()

def renum_heading_t(m):
    tag_prefix = m.group(1)
    sec = m.group(2)
    parts = sec.split('.')
    first = int(parts[0])
    new_first = first - 1
    new_sec = f'{new_first}.' + '.'.join(parts[1:])
    return f'{tag_prefix}>{new_sec} '

matches = list(re.finditer(r'(<w:t(?: xml:space="preserve")?>)([2-5]\.\d+(?:\.\d+)*\.)\s+', text))
print(f'Total heading number matches: {len(matches)}')
for m in matches:
    old = m.group(0)
    new = renum_heading_t(m)
    print(f'{old} -> {new}')

