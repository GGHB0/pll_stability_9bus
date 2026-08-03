---
name: tcc-pdf-notes
description: Cria notas técnicas em PDF do projeto (documentos de uma coluna, A4, com equações numeradas, tabelas e bibliografia) usando reportlab. Ativar sempre que o usuário pedir para gerar/criar/atualizar um PDF, uma nota técnica, um documento explicativo, um memorando ou "algo para o Bruno/professor/orientador" — mesmo sem mencionar PDF. Também usar para ajustar uma nota já existente em output/.
version: 1.0.0
---

# TCC PDF Notes — Notas Técnicas em PDF

Gera documentos técnicos autocontidos: explicação de um método, defesa de uma
escolha de projeto, runbook para o Bruno. **Não** é para o TCC em si (ver
`tcc-docx-editor`) nem para figuras (ver `svg-diagrams`).

## Onde as coisas ficam

| O quê | Onde |
|---|---|
| Biblioteca `pdfnote.py` | `scripts/notas/pdfnote.py` |
| Geradores | `scripts/notas/gen_<assunto>.py` |
| PDFs gerados | `output/<assunto>.pdf` — **versionados** (`!output/*.pdf`) |
| PNGs de conferência | pasta scratchpad da sessão, nunca no repositório |

Python: sempre `.venv\Scripts\python.exe`. Depende de `reportlab` e
`pypdfium2`, ambos já em `requirements.txt`.

## API

```python
import sys; from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pdfnote import Note, render_preview, XI, SQ, AP, AR, DL, TAU, WN, W0, MINUS

n = Note(title="...", subtitle="...", out=ROOT / "output" / "x.pdf",
         meta_left="...<br/>...", meta_right="Nota técnica<br/>2 de agosto de 2026",
         running_head="...")
n.h("1. Seção")            # título de seção
n.p("parágrafo justificado")
n.eq("K<sub>p</sub> = 2ξω<sub>n</sub>", "1")   # bloco com barra lateral + número
n.table(["Col A", "Col B"], [["a", "b"]], [4.0, 10.7])   # larguras em cm
n.note("observação em cinza, recuada")
n.gap(8)                   # espaçador em pt
n.refs(["SOBRENOME, Nome. Título. Editora, ano."])
out = n.build()
```

Largura útil da coluna: **14,7 cm** — a soma das larguras de tabela precisa
fechar nisso.

Marcação aceita nos textos: `<b>`, `<i>`, `<sub>`, `<super>`, `<br/>` e
entidades HTML (`&#231;` para ç, `&#160;` para espaço fixo em milhares).
Acentos podem ir literais também; entidades são só mais seguras contra
problemas de encoding no Windows.

## Workflow

1. Escrever/editar `scripts/notas/gen_<assunto>.py`.
2. Rodar com preview:
   `.venv\Scripts\python.exe scripts\notas\gen_<assunto>.py --preview <scratchpad>`
3. **Ler os PNGs gerados** — sempre. Erros de layout (glifo faltando, tabela
   estourando a coluna, vão grande antes de quebra de página) só aparecem
   visualmente.
4. Iterar até o layout fechar.
5. Antes de entregar, rodar o agente `note-validator` (Sonnet) sobre o PDF, os
   PNGs e a KB do tema. Corrigir o que ele marcar como `BLOQUEIA`.
6. Entregar o PDF com `SendUserFile`.

Divisão de modelo: o passo 2 é mecânico e vai para o agente `pdf-note-runner`
(Haiku); o passo 5 exige julgamento e vai para o `note-validator` (Sonnet); a
redação do conteúdo e as decisões de layout ficam no modelo principal.
Agente novo só aparece na lista na sessão seguinte à criação.

## Armadilhas já pagas

- **`rise` em `<sub>`/`<super>`**: o reportlab desalinha o avanço horizontal e
  os índices saem soltos no meio da linha. Usar o padrão, sem `rise` nem `size`.
- **Fontes embutidas não têm grego.** Por isso a biblioteca registra o Times
  New Roman por TTF. Conferido presente: `ω ξ δ τ θ Δ √ ≈ → ← ± ≤ · — ₀ ²`.
  **Ausente: `✓` (U+2713)** — não usar; marcar com negrito.
- **Canvas não interpreta entidades HTML.** Vale para `running_head` e para o
  título nos metadados; a biblioteca já limpa os dois com `_plain()`. Se algum
  texto novo for parar no canvas, aplicar o mesmo tratamento.
- **Vão grande no fim da página** costuma ser um bloco `eq` que não coube por
  poucos pontos: uma linha com `<super>` pede mais altura que o `leading`
  nominal. Reduzir o padding do bloco ou a margem inferior resolve.
- **Não** usar `Read` direto no PDF para conferir: depende de `pdftoppm`, que
  não está instalado. Usar `render_preview()`, que passa por `pypdfium2`.

## Convenção visual

Times New Roman, uma coluna, A4, margens 2,4 cm laterais. Azul de destaque
`#1A4A6E` em títulos, cabeçalho de tabela e barra lateral das equações; corpo
`#14232E`; texto secundário `#5A6B78`; fundo de bloco `#F4F7F9`.

Estrutura que funciona bem: título e subtítulo, faixa de metadados, seções
numeradas, e uma seção final acionável (ex.: "Antes de simular") quando a nota
tem leitor operacional. Bibliografia completa no fim, no mesmo formato do
`references:` da KB — as duas precisam bater.

## Depois de gerar

Nota nova ou revisada que documente decisão técnica deve ter o conteúdo
correspondente na KB (`.claude/kb/`). O PDF é o entregável; a KB é a memória.
Não deixar um sem o outro.
