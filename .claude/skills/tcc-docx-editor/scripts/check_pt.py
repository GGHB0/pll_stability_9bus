# -*- coding: utf-8 -*-
"""Varredura de portugues sobre o document.xml do TCC.

Uso: python.exe check_pt.py <document.xml> [--corpo <ini>]
     (--corpo N ignora blocos abaixo de N; o pre-textual e o sumario sao cheios
      de resto de template e poluem o resultado. Sem --corpo, varre tudo.)

Nao corrige nada: so lista candidatos com bloco e contexto, para triagem manual.
Todo achado precisa de olho humano — "onde" locativo e legitimo, "o mesmo" as
vezes e mesmo adjetivo, e placeholder pode ser pendencia consciente.

Ver revisao_pt.md para o que cada classe significa e como decidir.
"""
import io
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

xml = open(sys.argv[1], encoding='utf-8').read()
ini = 0
if '--corpo' in sys.argv:
    ini = int(sys.argv[sys.argv.index('--corpo') + 1])

body = xml[xml.index('<w:body>'):]
BLOCKS = re.findall(r'<w:tbl>.*?</w:tbl>|<w:p\b[^>]*>.*?</w:p>|<w:p\b[^>]*/>', body, re.S)


def texto(b):
    return ''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', b))


def estilo(b):
    if b.startswith('<w:tbl>'):
        return 'TBL'
    m = re.search(r'<w:pStyle w:val="([^"]+)"', b)
    return m.group(1) if m else '-'


# rotulo -> (regex, comentario)
PADROES = [
    ('regencia "capacidade/possibilidade EM"', r'\b(?:capacidade|possibilidade|dificuldade)\s+(?:d[eoa]s?\s+[\wçãéêíóúâôõ]+\s+)?em\s+\w+r\b'),
    ('"implicar EM"',                          r'implica\w*\s+em\b'),
    ('"onde" (so vale para lugar)',            r'\bonde\b'),
    ('"atraves de" (preferir "por meio de")',  r'atrav[ée]s\s+d'),
    ('"Diferente de" (adverbio)',              r'\bDiferente\s+d[eoa]'),
    ('anglicismo',                             r'\bperformance\b|\bsetup\b|\bdeletar\b'),
    ('virgula entre relativo e verbo',         r'\bque,\s+\w+[aei]m?\b'),
    ('duplo espaco',                           r'\S  \S'),
    ('espaco antes de pontuacao',              r'\w\s+[,;.](?!\s*\d)'),
    ('residuo de LaTeX',                       r'\$[^$]{1,12}\$|\\\w+\{'),
    ('placeholder do template',                r'\[(?:INSERIR|FIGURA|T[ÍI]TULO|DADOS|ANO|AUTORES|A CONFIRMAR)|A CONFIRMAR\]|\bXX\b|XXf\.'),
    ('em-dash (proibido no TCC)',              r'—'),
    ('separador de milhar com espaco',         r'\d\s\d{3}\b'),
    ('erro de digitacao ja visto',             r'anancilar|acomplamento|possue|atravez|Switch On To Fault'),
]

for rotulo, padrao in PADROES:
    achados = []
    for i, b in enumerate(BLOCKS):
        if i < ini:
            continue
        t = texto(b)
        for m in re.finditer(padrao, t, re.I):
            s, e = max(0, m.start() - 45), min(len(t), m.end() + 45)
            achados.append(f'  [{i:3d}] ...{t[s:e]}...')
    print(f'--- {rotulo}: {len(achados)} ---')
    for a in achados[:25]:
        print(a)
    if len(achados) > 25:
        print(f'  (+{len(achados) - 25} outros)')
    print()

# ponto final ausente em paragrafo de corpo
print('--- paragrafo de corpo sem ponto final ---')
for i, b in enumerate(BLOCKS):
    if i < ini:
        continue
    t, s = texto(b).strip(), estilo(b)
    if s.startswith('Ttulo') or s.startswith('Sumrio') or s == 'TBL' or len(t) < 40:
        continue
    if not t.endswith(('.', ':', ';', '?', '!', ']')):
        print(f'  [{i:3d}] ...{t[-70:]}')
