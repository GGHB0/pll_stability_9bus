---
name: pdf-kb-updater
description: Extrai conteúdo de qualquer PDF (livro ou artigo) e atualiza os arquivos KB em .claude/kb/. Ativar quando o usuário pedir para "buscar referência", "checar no [autor/título]", "atualizar KB com PDF", mencionar um artigo ou livro pelo nome, ou pedir para explorar um PDF novo e ver o que vale extrair.
version: 2.3.0
---

# PDF → KB Updater

Workflow para extrair conhecimento de qualquer PDF e atualizar `.claude/kb/`.
Scripts pypdf prontos em [scripts.md](scripts.md); exemplos em
[examples.md](examples.md).

## Dois Modos de Operação

| Modo | Quando | Fluxo |
|---|---|---|
| **Dirigido** | Usuário pede tópico/seção específica | Passos 0 → 4 |
| **Exploratório** | Usuário entrega um PDF sem tópico definido, ou pede para "ver o que tem de interessante" | Passos 0–1 → Varredura → proposta ao usuário → Passos 2–4 |

## Divisão de Trabalho por Modelo

A extração é mecânica; a síntese exige julgamento. Separar:

| Etapa | Quem executa |
|---|---|
| Passos 0–2 + varredura (localizar PDF, TOC, skim, extrair seções, triagem) | Subagente **`pdf-extractor`** (Haiku) — `.claude/agents/pdf-extractor.md` |
| Varredura: seleção do que propor + Passos 3–4 (síntese, escrita dos `.md`, MEMORY.md) | Modelo principal |

Delegar via Agent tool com `subagent_type: "pdf-extractor"`, passando o
caminho do PDF e os intervalos de páginas (ou o tópico a localizar, ou o
pedido de varredura). O subagente devolve os caminhos dos `.txt` em
`~/pdfext/` + índice do conteúdo; o modelo principal então lê **direto dos
`.txt`** as seções que vai usar — não confiar em paráfrase do subagente para
conteúdo técnico da KB.

**Quando NÃO delegar:** pedido pontual em PDF já mapeado em
[section-maps.md](section-maps.md) (1–2 extrações pequenas) — o overhead do
subagente não compensa; rodar os scripts inline.

## Ambiente

Rodar os scripts sempre com o Python do venv do projeto:
```powershell
.venv\Scripts\python.exe script.py
```
`pypdf` **não** está no `requirements.txt` — se der `ModuleNotFoundError`,
instalar com `.venv\Scripts\pip install pypdf` (não adicionar ao requirements;
é dependência só desta skill).

Nunca usar `print()` com texto do PDF no terminal — Windows (cp1252) causa
`UnicodeEncodeError`. Salvar sempre em arquivo UTF-8 e ler com `Read`.

## Passo 0 — Localizar o PDF

**Pasta padrão de bibliografia:**
```
C:\Users\victo\OneDrive\Meus Bagulhos\Arquivos\UERJ\TCC - Victor e Bruno\Bibliografia\
```

Se o usuário não fornecer o caminho completo, listar os PDFs (script "Listar
PDFs" em scripts.md), ler `~/pdfext/lista.txt` e confirmar com o usuário.
Caminho absoluto fornecido → usar direto.

## Passo 1 — Ler Metadados e Sumário

Rodar o script "Metadados + sumário" (scripts.md) → `~/pdfext/toc.txt`.
Antes, checar se o PDF já está em [section-maps.md](section-maps.md).

**PDFs sem sumário (artigos):** extrair as primeiras 4–6 páginas para
identificar seções e depois as páginas relevantes ao tópico buscado.

## Varredura Exploratória (só no modo exploratório)

Objetivo: **ler o PDF por amostragem para descobrir o que vale buscar**,
antes de qualquer extração integral.

1. Delegar ao `pdf-extractor`: com o TOC em mãos, rodar o script "Varredura
   exploratória" (scripts.md) — 1ª página de cada seção nível 1–2 →
   `skim_*.txt` — e montar `~/pdfext/_index.txt` com bullets por seção.
2. Modelo principal lê `_index.txt` e os `skim_*.txt` das seções promissoras,
   cruzando com:
   - os KBs existentes (não duplicar conteúdo já sintetizado);
   - o escopo do TCC: SRF-PLL/GFL, contingências severas, IEEE 9 barras,
     LVRT/normas, oscilações, inércia/VSG, eventos (apagões).
3. Apresentar ao usuário uma **lista priorizada**: seção → páginas → por que
   interessa ao TCC → KB alvo (arquivo novo ou append). Incluir também o que
   foi descartado, em 1 linha.
4. **Aguardar aprovação** antes de extrair na íntegra. Aprovado → Passo 2
   com as seções escolhidas.
5. PDF grande e reutilizável (livro-texto, relatório) → registrar o mapa de
   seções em section-maps.md.

## Passo 2 — Extrair Seções na Íntegra

Rodar o script "Extrair seções" (scripts.md) com o dict
`sections = {'nome.txt': (START, END)}` — todas as seções de interesse de uma
vez, um `.txt` por seção em `~/pdfext/`. Atenção ao limite de ~25k tokens por
`Read` (dividir seções longas — ver nota em scripts.md).

## Passo 3 — Identificar o que Atualizar

Verificar os KBs existentes antes de criar arquivos novos:

```
.claude/kb/
├── project-scope.md
├── pll/          — srf_pll_theory, pll_gains_methodology, pll_contingencies
├── inverter/     — lcl_filter, simulink_model, vsc_reference
├── power-system/ — ieee9bus_topology, ieee9bus_thevenin, machine_inertia,
│                   inertia_estimation, virtual_inertia
├── standards/    — lvrt (IEEE 1547-2018), ONS
├── events/       — apagões e distúrbios (BR ago/2023, Ibéria abr/2025)
├── simulation/   — workflow de export, Vcc override, runtime
├── dashboard/    — relatório HTML (dados/, graficos/, cards/, layout/)
└── tcc-word/     — estrutura OOXML e mapa de conteúdo do DOCX
```

Relatórios de eventos/incidentes vão em `kb/events/`, com prefixo do evento
no nome do arquivo (ex.: `iberia_2025_*.md`).

Regras:
- **Máx 200 linhas** por arquivo de KB
- Conteúdo que não cabe: criar novo arquivo na subpasta temática correta
- Arquivo novo: adicionar entrada em `MEMORY.md`:
  `C:\Users\victo\.claude\projects\C--projetos-pll-stability-9bus\memory\MEMORY.md`

## Passo 4 — Atualizar KB

Usar `Edit` (append ao final) para arquivo existente, ou `Write` para novo.

Frontmatter obrigatório em qualquer arquivo KB:
```markdown
---
name: slug-do-arquivo
description: Uma linha descrevendo o conteúdo (usada para decidir relevância)
source: Sobrenome Autor, Título Abreviado, ano, §seção ou p.páginas
---
```

## PDFs com Mapa de Seções Conhecido

Antes de rodar o Passo 1 num PDF já mapeado, consultar
[section-maps.md](section-maps.md) (mesma pasta desta skill) — evita
re-extrair o sumário. Ao mapear um PDF novo que provavelmente será
reutilizado, **adicionar o mapa lá** com as páginas das seções relevantes.
