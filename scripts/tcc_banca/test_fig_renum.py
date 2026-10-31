import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Temp\tcc_banca\unpacked\word\document.xml', 'r', encoding='utf-8') as f:
    text = f.read()

# Captions:
text = text.replace("<w:t>Figura 2.</w:t>", "<w:t>Figura 1.</w:t>")
text = text.replace("<w:t>Figura 3.</w:t>", "<w:t>Figura 2.</w:t>")
text = text.replace("<w:t>Figura 4.</w:t>", "<w:t>Figura 3.</w:t>")
text = text.replace("<w:t>Figura 5.</w:t>", "<w:t>Figura 4.</w:t>")
text = text.replace("<w:t>Tabela 4.</w:t>", "<w:t>Tabela 3.</w:t>")
text = text.replace("<w:t>Tabela 5.</w:t>", "<w:t>Tabela 4.</w:t>")

# Body remissions for figures
# Remember:
# Figura 2.x -> Figura 1.x
# Figura 3.x -> Figura 2.x
# Figura 4.1 -> Figura 3.1
# Figura 4.2 -> Figura 3.2
# Old Figura 4.3 -> Figura 3.4 (since new Figura 3.3 is the ONS logic diagram)
# Figura 5.x -> Figura 4.x
def renum_fig_match(m):
    prefix = m.group(1) # 'Figura' or 'Figuras'
    cap = int(m.group(2))
    num = int(m.group(3))
    if cap == 2:
        return f"{prefix} 1.{num}"
    elif cap == 3:
        return f"{prefix} 2.{num}"
    elif cap == 4:
        if num <= 2:
            return f"{prefix} 3.{num}"
        else:
            return f"{prefix} 3.{num+1}"
    elif cap == 5:
        return f"{prefix} 4.{num}"
    return m.group(0)

text = re.sub(r'\b(Figuras?)\s+([2-5])\.(\d+)\b', renum_fig_match, text)

# Tables:
def renum_tab_match(m):
    prefix = m.group(1) # 'Tabela' or 'Tabelas'
    cap = int(m.group(2))
    num = int(m.group(3))
    if cap == 4:
        return f"{prefix} 3.{num}"
    elif cap == 5:
        return f"{prefix} 4.{num}"
    return m.group(0)

text = re.sub(r'\b(Tabelas?)\s+([4-5])\.(\d+)\b', renum_tab_match, text)

# Check counts in clean text
clean_text = re.sub(r'<[^>]+>', '', text)
for term in ['Figura 1.', 'Figura 2.', 'Figura 3.', 'Figura 4.', 'Figura 5.', 'Tabela 3.', 'Tabela 4.', 'Tabela 5.']:
    m = list(re.finditer(re.escape(term), clean_text))
    print(f'{term}: {len(m)} occurrences')

