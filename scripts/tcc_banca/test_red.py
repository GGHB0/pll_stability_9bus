with open(r'C:\Temp\tcc_banca\unpacked\word\document.xml', 'r', encoding='utf-8') as f:
    text = f.read()

count = text.count('FF0000')
print('Total occurrences of red color FF0000:', count)

