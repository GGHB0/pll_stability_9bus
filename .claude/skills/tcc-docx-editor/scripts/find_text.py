# -*- coding: utf-8 -*-
"""Localiza texto no corpo do documento, com índice de bloco e contexto.

Uso: python.exe find_text.py <document.xml> <padrão> [--regex]
     (padrão literal por default; --regex interpreta como regex Python)
"""
import re, io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

xml = open(sys.argv[1], encoding='utf-8').read()
pat = sys.argv[2] if '--regex' in sys.argv else re.escape(sys.argv[2])

body = xml[xml.index('<w:body>'):]
blocks = re.findall(r'<w:tbl>.*?</w:tbl>|<w:p\b[^>]*>.*?</w:p>|<w:p\b[^>]*/>', body, re.S)


def text_of(b):
    return ''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', b))


total = 0
for i, b in enumerate(blocks):
    t = text_of(b)
    for m in re.finditer(pat, t):
        total += 1
        s = max(0, m.start() - 80)
        e = min(len(t), m.end() + 60)
        print(f'[{i:3d}] ...{t[s:e]}...')
print(f'\ntotal: {total} ocorrencia(s)')
