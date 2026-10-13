# -*- coding: utf-8 -*-
"""Compara o texto visível de dois DOCX, parágrafo a parágrafo (conferência pós-entrega).

Uso: python.exe diff_texto.py <antes.docx> <depois.docx>

Lê só w:t e w:tab de cada w:p do document.xml, então bookmark (_Toc), ID,
rsid e paraId que o Word renumera ao salvar não aparecem. O número de página
no fim das linhas do sumário (tab + dígitos) é descartado. Imprime cada
parágrafo removido (-) e incluído (+), com o índice no arquivo de depois, e a
contagem de comentários e de "Feito." de cada lado.

Lê com o Word aberto: se o lock impedir, copia pela API do Windows (CopyFileW),
como o dump_comments.py. O backup de _backups/ é o "antes" natural.
Código de saída: 0 sempre; quem decide se o diff é o esperado é quem roda.
"""
import ctypes, difflib, io, os, re, sys, zipfile

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

P = re.compile(r'<w:p[ >].*?</w:p>', re.S)
T = re.compile(r'<w:t(?:\s[^>]*)?>([^<]*)</w:t>|<w:tab/>')
PAG = re.compile(r'\t\d+$')


def open_docx(path, n):
    try:
        return zipfile.ZipFile(path)
    except PermissionError:
        tmp = rf'C:\Temp\_diff_texto_{n}.docx'
        os.makedirs(r'C:\Temp', exist_ok=True)
        if not ctypes.windll.kernel32.CopyFileW(os.path.abspath(path), tmp, False):
            raise
        return zipfile.ZipFile(tmp)


def ler(path, n):
    z = open_docx(path, n)
    doc = z.read('word/document.xml').decode('utf-8')
    paras = []
    for p in P.findall(doc):
        txt = ''.join(m.group(1) if m.group(1) is not None else '\t' for m in T.finditer(p))
        paras.append(PAG.sub('', txt).rstrip())
    com = z.read('word/comments.xml').decode('utf-8') if 'word/comments.xml' in z.namelist() else ''
    return paras, com.count('<w:comment '), com.count('>Feito.</w:t>')


def main(a, b):
    pa, ca, fa = ler(a, 'a')
    pb, cb, fb = ler(b, 'b')
    sm = difflib.SequenceMatcher(None, pa, pb, autojunk=False)
    n = 0
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal':
            continue
        for t in pa[i1:i2]:
            print(f'-      {t[:300]}')
        for k, t in enumerate(pb[j1:j2], j1):
            print(f'+ {k:5d} {t[:300]}')
        print()
        n += 1
    print(f'{n} trecho(s) diferente(s) · parágrafos {len(pa)} → {len(pb)}')
    print(f'comentários {ca} → {cb} · "Feito." {fa} → {fb}')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
