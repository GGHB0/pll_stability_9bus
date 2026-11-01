# -*- coding: utf-8 -*-
"""Texto (ou XML bruto) de um intervalo de blocos do corpo.

Uso: python.exe dump_blocks.py <document.xml> <ini> <fim> [--raw] [--math]
     (fim inclusivo; --raw imprime o XML completo de cada bloco;
      --math acrescenta o texto linear das equações OMML, para conferir
      remissões "(3.5) é X" contra o conteúdo real da equação)
"""
import re, io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

xml = open(sys.argv[1], encoding='utf-8').read()
start, end = int(sys.argv[2]), int(sys.argv[3])
raw = '--raw' in sys.argv
math = '--math' in sys.argv

body = xml[xml.index('<w:body>'):]
blocks = re.findall(r'<w:tbl>.*?</w:tbl>|<w:p\b[^>]*>.*?</w:p>|<w:p\b[^>]*/>', body, re.S)


def text_of(b):
    # <w:tab/> e <w:br/> viram separador: sem isso a lista de siglas cola
    # "GD" + tab + "Geração" em "GDGeração" e \bGD\b não casa
    return ''.join(m.group(1) if m.group(1) is not None else (' ' if m.group(0) == '<w:br/>' else '	')
                   for m in re.finditer(r'<w:t(?:\s[^>]*)?>([^<]*)</w:t>|<w:tab/>|<w:br/>', b))


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
        line = f'[{i:3d}] ({style_of(b)}) {text_of(b).strip()}'
        if math and '<m:oMath' in b:
            line += '  | math: ' + ''.join(re.findall(r'<m:t(?:\s[^>]*)?>([^<]*)</m:t>', b))
        print(line)
