---
name: pdf-kb-updater
description: Extrai conteúdo de qualquer PDF (livro ou artigo) e atualiza os arquivos KB em .claude/kb/. Ativar quando o usuário pedir para "buscar referência", "checar no [autor/título]", "atualizar KB com PDF", mencionar um artigo ou livro pelo nome.
version: 2.0.0
---

# PDF → KB Updater

Workflow para extrair conhecimento de qualquer PDF e atualizar `.claude/kb/`.

## Passo 0 — Localizar o PDF

**Pasta padrão de bibliografia:**
```
C:\Users\victo\OneDrive\Meus Bagulhos\Arquivos\UERJ\TCC - Victor e Bruno\Bibliografia\
```

Se o usuário não fornecer o caminho completo, liste os PDFs disponíveis:

```python
import os, glob
bib = r'C:\Users\victo\OneDrive\Meus Bagulhos\Arquivos\UERJ\TCC - Victor e Bruno\Bibliografia'
with open(os.path.expanduser('~/pdfext/lista.txt'), 'w', encoding='utf-8') as f:
    for p in sorted(glob.glob(os.path.join(bib, '**', '*.pdf'), recursive=True)):
        f.write(os.path.relpath(p, bib) + '\n')
print('lista salva')
```

Leia com `Read: C:\Users\victo\pdfext\lista.txt` e confirme com o usuário qual arquivo usar.
Se o usuário fornecer um caminho absoluto direto, use-o sem listar.

## Passo 1 — Ler Metadados e Sumário

**IMPORTANTE:** nunca use `print()` direto no terminal — Windows (cp1252) causa `UnicodeEncodeError`.
Salve sempre em arquivo UTF-8:

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

Leia com `Read: C:\Users\victo\pdfext\toc.txt`.

**PDFs sem sumário (artigos):** extraia as primeiras 4–6 páginas para identificar seções e
depois as páginas relevantes ao tópico buscado.

## Passo 2 — Extrair Páginas para Arquivo Temporário

```python
import os
from pypdf import PdfReader

r = PdfReader(r'CAMINHO_COMPLETO.pdf')
out_dir = os.path.expanduser('~/pdfext')
os.makedirs(out_dir, exist_ok=True)

# Defina START e END (1-indexed, END inclusivo)
START, END = 1, 10

with open(os.path.join(out_dir, 'secao.txt'), 'w', encoding='utf-8', errors='replace') as f:
    for page_num in range(START - 1, END):   # range é 0-indexed
        text = r.pages[page_num].extract_text() or ''
        f.write(f'=== PAGE {page_num + 1} ===\n{text}\n\n')
print('done ->', out_dir)
```

Leia com `Read: C:\Users\victo\pdfext\secao.txt`.
Para múltiplos trechos, use nomes diferentes (`secao_a.txt`, `secao_b.txt`).

## Passo 3 — Identificar o que Atualizar

Verifique os KBs existentes antes de criar arquivos novos:

```
.claude/kb/
├── project-scope.md
├── pll/          — srf_pll_theory, pll_gains_methodology, pll_contingencies
├── inverter/     — lcl_filter, simulink_model, vsc_reference
├── power-system/ — ieee9bus_topology, ieee9bus_thevenin, machine_inertia,
│                   inertia_estimation, virtual_inertia
└── standards/    — lvrt (IEEE 1547-2018)
```

Regras:
- **Máx 200 linhas** por arquivo de KB
- Conteúdo que não cabe: criar novo arquivo na subpasta temática correta
- Arquivo novo: adicionar entrada em `MEMORY.md`:
  `C:\Users\victo\.claude\projects\C--projetos-pll-stability-9bus\memory\MEMORY.md`

## Passo 4 — Atualizar KB

Use `Edit` (append ao final) para arquivo existente, ou `Write` para novo.

Frontmatter obrigatório em qualquer arquivo KB:
```markdown
---
name: slug-do-arquivo
description: Uma linha descrevendo o conteúdo (usada para decidir relevância)
source: Sobrenome Autor, Título Abreviado, ano, §seção ou p.páginas
---
```

---

## Livros com Mapa de Seções Conhecido

### Yazdani & Iravani — *Voltage-Sourced Converters* (473 p.)

| Seção | Páginas | Conteúdo |
|-------|---------|---------|
| §8.3.4–8.3.5 | 233–238 | SRF-PLL: modelo, H(s) com zeros ±j2ω₀, Exemplo 8.1 |
| §8.4.1 | 241–244 | PI de corrente: kp=L/τi, ki=(R+ron)/τi |
| §8.4.2 | 246–248 | Critério de VDC: ≥ 2V̂t ou 1,74V̂t (3°H) |
| §8.6 | 256–265 | DC-bus voltage controller |
| §12.4.1 | 364–367 | PLL no sistema HVDC |
| §12.5.2–12.5.4 | 379–387 | PLL + controle de corrente sob falta assimétrica |
| Apêndice B | 448–452 | Base pu para VSC (Tabelas B.1, B.2) |

---

## Exemplos de Uso

```
"Busca no Kundur o critério das áreas iguais"
0. Listar PDFs → Kundur__Power_System_Stability_and_Control.pdf
1. TOC → Cap. 3 p.130 "Equal Area Criterion"
2. Extrair p.130-155 → ~/pdfext/secao.txt
3. Checar kb/power-system/ → não existe equal_area_criterion.md
4. Criar kb/power-system/equal_area_criterion.md com frontmatter
5. Adicionar entrada no MEMORY.md
```

```
"Busca no artigo IEEE 7767 o método de estimativa de inércia por CoI"
0. Usuário fornece caminho ou listar bibliografia
1. Sem sumário → extrair p.1-4 para estrutura
2. Buscar seção "Center of Inertia" → extrair páginas relevantes
3. Checar kb/power-system/inertia_estimation.md → existe, verificar linhas
4. Append ou criar inertia_estimation_2.md se >200 linhas
```
