# -*- coding: utf-8 -*-
"""Injeta um document.xml editado num DOCX template (ZIP) e grava o resultado.

Uso: python.exe repack.py <template.docx> <document.xml> <saida.docx>

O template deve ser o MESMO DOCX que originou o XML (estágio de staging) —
só word/document.xml é substituído; todo o resto (styles, comments, media,
rels) vem intacto do template.
"""
import zipfile, io, sys
import xml.etree.ElementTree as ET

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

template, new_xml, output = sys.argv[1], sys.argv[2], sys.argv[3]

data = open(new_xml, 'rb').read()
ET.fromstring(data)  # aborta aqui se o XML estiver malformado
print('XML bem formado: OK')

with zipfile.ZipFile(template, 'r') as zin, \
     zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        if item.filename == 'word/document.xml':
            zout.writestr(item, data)
        else:
            zout.writestr(item, zin.read(item.filename))

with zipfile.ZipFile(output, 'r') as z:
    print(f'entries: {len(z.namelist())}')
    print(f'document.xml size: {z.getinfo("word/document.xml").file_size}')
print(f'OK: {output}')
