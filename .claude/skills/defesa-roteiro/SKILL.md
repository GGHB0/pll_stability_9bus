---
name: defesa-roteiro
description: Gera os materiais de ensaio da defesa do TCC a partir de uma fonte única de falas — roteiro de falas e tempo (.docx), guia de estudos (.docx), roteiro de estudo (PDF) e áudios de ensaio (edge-tts). Ativar quando o usuário pedir para mudar uma fala, um tópico, o cronograma de 30 min, o guia ou o roteiro de estudo, gerar os áudios, ou alinhar esses materiais a uma mudança no deck ou no palco do dashboard. Não edita o deck (ver tcc-pptx-editor) nem o palco (ver dashboard-html-editor).
version: 1.0.0
---

# Skill: defesa-roteiro

Materiais de ensaio da defesa (30 min: PPTX 1-19 → palco do dashboard 1-8 →
PPTX 20-21, mais apêndice e reserva 22-29). Tudo roda com o Python do `.venv`
do repo, sem subagente: serve igual para Claude Code, Antigravity ou outro agente.

## Estrutura

| Pasta | O que guarda | Quem lê |
|---|---|---|
| `falas/` | **Fonte única** das falas: slides 1-21, palco 1-8, apêndice e reserva, tópicos "O que falar" da modelagem | os quatro geradores |
| `conteudo/` | Texto do roteiro de estudo (fundamentos, números, caixas, perguntas da banca), em arquivos numerados | PDF e guia |
| `scripts/` | Geradores e layout (`rf_*` roteiro, `gw_*` guia, `pdf_*` PDF, `au_*` áudios) | `gerar.py` |

Nenhum gerador guarda fala própria. Mudou uma fala → muda num lugar só, e os
quatro materiais saem iguais depois de gerados de novo.

## Como gerar

```text
.venv\Scripts\python.exe .claude\skills\defesa-roteiro\scripts\gerar.py docs
.venv\Scripts\python.exe .claude\skills\defesa-roteiro\scripts\gerar.py audios
```

- Alvos: `roteiro`, `guia`, `pdf`, `audios`, `docs` (= roteiro + guia + pdf).
- Saídas em `output/` (não versionado): `Roteiro_Falas_e_Tempo_Defesa_TCC.docx`,
  `Roteiro_e_Guia_de_Estudos_Defesa_TCC.docx`, `roteiro_estudo_defesa.pdf`,
  `audios_defesa/`.
- Os dois `.docx` também são copiados para `Template Modelo TCC` no OneDrive
  (pasta compartilhada entre Victor e Bruno). Para testar sem mexer no OneDrive:
  `gerar.py docs --sem-onedrive`.
- `audios` precisa de internet e leva minutos (uma chamada de síntese por fala).

### Pré-requisitos

1. `.venv\Scripts\pip install -r requirements.txt` (traz `python-docx` e `edge-tts`).
2. Miniaturas dos slides em `C:\Temp\defesa_roteiro\png\s01.png...`: render do
   deck pela skill `tcc-pptx-editor` (`render.ps1`), sempre sobre uma cópia.
3. Telas do palco em `output/verifica_palco/1920x1080/`:
   `.venv\Scripts\python.exe scripts\verifica_palco.py` (depois de `app.py`).
4. Pasta do TCC no OneDrive: achada sozinha em
   `~/OneDrive/Meus Bagulhos/Arquivos/UERJ/TCC - Victor e Bruno` (Victor) ou
   `~/OneDrive/UERJ/TCC - Victor e Bruno` (Bruno). Em outra máquina, copiar
   `config.example.py` para `config.py` (gitignored) e ajustar `TCC_DIR`.

## Onde mexer

| Pedido | Arquivo |
|---|---|
| Fala de um slide (1-19) | `falas/slides_*.py` / `falas/slide_19.py`: campo `falas` do slide |
| Fala de um capítulo do palco | `falas/palco.py`: campo `falas` do capítulo |
| Fala dos slides 20-21 ou fala curta do apêndice/reserva | `falas/conclusao.py` |
| Fala completa de reserva (22-29), só no guia | `falas/reserva.py` |
| Pontos a comentar, mensagem, tempo-alvo (`dur_s`), atenção | mesmo item em `falas/`: `pontos`, `msg`, `dur_s`, `atencao` |
| Tópicos "O que falar" da modelagem (5-16) | `falas/topicos.py` |
| Fundamentos, números, caixas de banca/cuidado, legendas | `conteudo/NN_*.py` (procurar `slide(N,` ou `cap(N,`) |
| Cronograma de 30 min e mapa do TCC no guia | `scripts/gw_cronograma.py` |
| Visual de um documento | `scripts/rf_*.py`, `scripts/gw_*.py`, `scripts/pdf_*.py` |

Formato de uma fala: lista de tuplas `("Bruno" | "Victor", "texto")`. No palco,
`(Seta →)` marca o clique; os áudios tiram essas rubricas sozinhos. Não usar
colchetes `[ ]` dentro do texto (o parser dos áudios corta neles).

### `conteudo/`

Os arquivos são executados em ordem alfabética, como um script só, pelo PDF e
pelo guia (`exec`): não têm `import` e chamam `slide()`, `cap()`, `box()`,
`tab()`, `eq()`, `n.p()`... de `scripts/pdf_blocos.py`. O guia troca cada uma
dessas funções pela versão em Word (`scripts/gw_hooks.py`), então função nova
no PDF exige a irmã no guia. Arquivo passando de 200 linhas: dividir num
ponto entre dois comandos e renumerar os seguintes.

## Regras de conteúdo

- O deck só traz o que está no TCC entregue (VFinal), com o mesmo valor; as
  falas seguem o deck. Número novo → conferir no TCC antes.
- Frases do palco seguem o que a tela mostra: o texto do palco mora em
  `src/report/roteiro.py`. Mudou o capítulo no dashboard → ajustar `falas/palco.py`
  e a caixa do capítulo em `conteudo/`.
- Termos: "sintonia inadequada" (nunca BAD_PLL), "escorregamento de ciclo",
  "simulação computacional" (sem a sigla de transitórios eletromagnéticos),
  "recuperar o sincronismo" (nunca "reaquisitar"), sem RoCoF.
- Cores: azul = nominal, laranja = inadequada.

## Conferência

1. `gerar.py docs --sem-onedrive` roda sem erro.
2. Abrir os três arquivos de `output/` e olhar o item mexido nos três.
3. Mudança só de organização do código: as saídas têm de sair idênticas às de
   antes (comparar o `word/document.xml` dos `.docx` e o texto das páginas do PDF).
4. Entregar: `gerar.py docs` (sem a opção) copia os `.docx` para o OneDrive.

Mapa do deck e do palco: [deck_map.md](../../kb/tcc-pptx/deck_map.md).
