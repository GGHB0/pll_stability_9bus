# -*- coding: utf-8 -*-
"""Mapa de títulos (Ttulo1..Ttulo4) com índice de bloco.

Uso: python.exe dump_headings.py <document.xml>
"""
import re, io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

xml = open(sys.argv[1], encoding='utf-8').read()
body = xml[xml.index('<w:body>'):]
blocks = re.findall(r'<w:tbl>.*?</w:tbl>|<w:p\b[^>]*>.*?</w:p>|<w:p\b[^>]*/>', body, re.S)


def text_of(b):
    return ''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', b))


def style_of(b):
    m = re.search(r'<w:pStyle w:val="([^"]+)"', b)
    return m.group(1) if m else '-'


for i, b in enumerate(blocks):
    tag = style_of(b)
    if tag.startswith('Ttulo'):
        t = text_of(b).strip()
        if t:
            print(f'[{i:3d}] ({tag}) {t[:110]}')
print(f'\ntotal de blocos: {len(blocks)}')
