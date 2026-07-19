# -*- coding: utf-8 -*-
"""Texto (ou XML bruto) de um intervalo de blocos do corpo.

Uso: python.exe dump_blocks.py <document.xml> <ini> <fim> [--raw]
     (fim inclusivo; --raw imprime o XML completo de cada bloco)
"""
import re, io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

xml = open(sys.argv[1], encoding='utf-8').read()
start, end = int(sys.argv[2]), int(sys.argv[3])
raw = '--raw' in sys.argv

body = xml[xml.index('<w:body>'):]
blocks = re.findall(r'<w:tbl>.*?</w:tbl>|<w:p\b[^>]*>.*?</w:p>|<w:p\b[^>]*/>', body, re.S)


def text_of(b):
    return ''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', b))


def style_of(b):
    if b.startswith('<w:tbl>'):
        return 'TBL'
    m = re.search(r'<w:pStyle w:val="([^"]+)"', b)
    return m.group(1) if m else '-'


for i in range(start, min(end + 1, len(blocks))):
    b = blocks[i]
    if raw:
        print(f'##### BLOCK {i} style={style_of(b)} #####')
        print(b)
        print()
    else:
        print(f'[{i:3d}] ({style_of(b)}) {text_of(b).strip()}')
