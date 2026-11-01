# -*- coding: utf-8 -*-
import zipfile, sys, xml.etree.ElementTree as ET
sys.stdout.reconfigure(encoding='utf-8')

docx_path = r'C:\Temp\tcc_test_read.docx'
with zipfile.ZipFile(docx_path, 'r') as z:
    xml = z.read('word/document.xml').decode('utf-8')

root = ET.fromstring(xml)
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
paragraphs = root.findall('.//w:p', ns)

for i in range(528, 540):
    p = paragraphs[i]
    paraId = p.attrib.get('{http://schemas.microsoft.com/office/word/2010/wordml}paraId')
    t = ''.join(x.text for x in p.findall('.//w:t', ns) if x.text)
    print(f'P{i} [paraId={paraId}]: {t[:120]}')
