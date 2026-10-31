import re

with open(r'C:\Temp\tcc_banca\unpacked\word\_rels\document.xml.rels', 'r', encoding='utf-8') as f:
    rels = f.read()

matches = re.findall(r'Id="rId(\d+)"', rels)
ids = sorted([int(x) for x in matches])
print('All rIds in document.xml.rels:', ids)
print('Max rId:', max(ids))

# print last 5 relationships
for m in re.finditer(r'<Relationship [^>]+/>', rels):
    pass
# print snippet of the end of rels
idx = rels.rfind('<Relationship')
print('Last relationships:')
print(rels[idx-200:])

