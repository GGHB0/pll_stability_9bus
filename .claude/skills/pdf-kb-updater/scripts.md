# Scripts pypdf da skill pdf-kb-updater

Rodar sempre com `.venv\Scripts\python.exe`. Nunca imprimir texto do PDF no
terminal (cp1252 → `UnicodeEncodeError`); salvar em arquivo UTF-8 com
`errors='replace'` e ler com o tool `Read`.

## Listar PDFs da bibliografia (Passo 0)

```python
import os, glob
bib = r'C:\Users\victo\OneDrive\Meus Bagulhos\Arquivos\UERJ\TCC - Victor e Bruno\Bibliografia'
with open(os.path.expanduser('~/pdfext/lista.txt'), 'w', encoding='utf-8') as f:
    for p in sorted(glob.glob(os.path.join(bib, '**', '*.pdf'), recursive=True)):
        f.write(os.path.relpath(p, bib) + '\n')
print('lista salva')
```

## Metadados + sumário (Passo 1)

```python
import os
from pypdf import PdfReader

path = r'CAMINHO_COMPLETO.pdf'
r = PdfReader(path)
out_dir = os.path.expanduser('~/pdfext')
os.makedirs(out_dir, exist_ok=True)

m = r.metadata or {}
lines = [
    f"Título : {m.get('/Title', '—')}",
    f"Autor  : {m.get('/Author', '—')}",
    f"Páginas: {len(r.pages)}",
    '--- SUMÁRIO ---',
]

def collect_outline(items, indent=0):
    for item in items:
        if isinstance(item, list):
            collect_outline(item, indent + 2)
        else:
            try:
                lines.append(' ' * indent + item.title +
                             ' -> p.' + str(r.get_destination_page_number(item) + 1))
            except Exception:
                lines.append(' ' * indent + str(item))

collect_outline(r.outline)
if not r.outline:
    lines.append('(sem sumário — artigo ou PDF sem marcadores)')

with open(os.path.join(out_dir, 'toc.txt'), 'w', encoding='utf-8', errors='replace') as f:
    f.write('\n'.join(lines))
print('TOC salvo ->', out_dir)
```

## Varredura exploratória (modo exploratório)

Extrai a primeira página de cada seção de nível 1–2 do outline, em blocos de
10 seções por arquivo (`skim_01.txt`, `skim_02.txt`, …):

```python
import os
from pypdf import PdfReader

r = PdfReader(r'CAMINHO_COMPLETO.pdf')
out_dir = os.path.expanduser('~/pdfext')
os.makedirs(out_dir, exist_ok=True)

secs = []
def walk(items, depth=0):
    for it in items:
        if isinstance(it, list):
            if depth < 2:
                walk(it, depth + 1)
        else:
            try:
                secs.append((it.title, r.get_destination_page_number(it)))
            except Exception:
                pass
walk(r.outline)

CHUNK = 10
for i in range(0, len(secs), CHUNK):
    fname = os.path.join(out_dir, f'skim_{i // CHUNK + 1:02d}.txt')
    with open(fname, 'w', encoding='utf-8', errors='replace') as f:
        for title, p0 in secs[i:i + CHUNK]:
            f.write(f'=== SECAO: {title} (p.{p0 + 1}) ===\n')
            f.write((r.pages[p0].extract_text() or '') + '\n\n')
print(f'{len(secs)} secoes em {(len(secs) + CHUNK - 1) // CHUNK} arquivos skim')
```

**PDF sem outline** (artigo): extrair 1 página a cada 8–10 no mesmo formato
(`=== PAGE N ===`) para inferir a estrutura.

## Extrair seções na íntegra (Passo 2)

Todas as seções de interesse de uma vez — um arquivo por seção:

```python
import os
from pypdf import PdfReader

r = PdfReader(r'CAMINHO_COMPLETO.pdf')
out_dir = os.path.expanduser('~/pdfext')
os.makedirs(out_dir, exist_ok=True)

# nome_do_arquivo: (START, END)  — 1-indexed, END inclusivo
sections = {
    'secao_a.txt': (6, 28),
    'secao_b.txt': (331, 336),
}

for fname, (start, end) in sections.items():
    with open(os.path.join(out_dir, fname), 'w', encoding='utf-8', errors='replace') as f:
        for page_num in range(start - 1, end):
            text = r.pages[page_num].extract_text() or ''
            f.write(f'=== PAGE {page_num + 1} ===\n{text}\n\n')
print('done')
```

**Limite do Read:** ~25k tokens por chamada. Trechos com mais de ~15 páginas
densas serão truncados — leia o restante com `offset`, ou divida a seção em
arquivos menores no dict `sections`.
