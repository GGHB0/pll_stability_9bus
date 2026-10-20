---
name: tcc-pptx-editor
description: Edita o deck da defesa do TCC (Defesa_TCC_SRF-PLL.pptx, no OneDrive) com python-pptx — texto e títulos dos slides, tabelas, troca de figura, notas do apresentador (roteiro Bruno/Victor), slide novo no padrão visual, tempo de fala, conferência de números e legendas contra o TCC DOCX, render em PNG e entrega com backup. Ativar quando o usuário falar em "apresentação", "slides", "slide N", "PPT/PPTX", "defesa", "banca", "roteiro de fala", "notas do apresentador" ou pedir para mexer no deck. Não edita o TCC DOCX (ver tcc-docx-editor).
version: 1.3.0
---

# Skill: tcc-pptx-editor

Edita o deck da defesa (`config.py`; hoje `Defesa_TCC_SRF-PLL.pptx`, na
pasta `Template Modelo TCC` do OneDrive), sempre no **mesmo caminho**, com
backup datado em `_backups\defesa\`. Ferramenta: **python-pptx** no `.venv`
(XML cru só onde ele não chega: animação, transição, cirurgia em grupo).

Pastas: `referencia/` (lido em toda edição), `casos/` (fluxos ocasionais),
`scripts/`. Mapa slide a slide e pendências no KB:
[deck_map.md](../../kb/tcc-pptx/deck_map.md) e
[pendencias.md](../../kb/tcc-pptx/pendencias.md).

## Leitura obrigatória

- `referencia/design.md`: grade, cores do tema, fontes, tamanhos, as caixas
  que se repetem ("Cartão de destaque", "Moldura da figura", "Pergunta da
  banca"...). Slide novo ou forma nova **copia uma existente**, não nasce do zero.
- `referencia/entrega.md`: staging, finalize, entrega, sessões em paralelo.
- `referencia/armadilhas.md`: python-pptx, PowerPoint COM, OneDrive.

## Casos

- `casos/sincronia_tcc.md`: número, figura ou legenda do deck contra o TCC
  canônico e o KB. **Toda edição de conteúdo passa por aqui**: o deck é
  resumo do TCC e não pode dizer outra coisa.
- `casos/roteiro_fala.md`: notas `[Bruno]`/`[Victor]`, tempo (30 min de
  defesa, só o corpo conta), redação falada.
- `casos/troca_figura.md`: PNG novo do TCC ou do dashboard numa moldura.
- `casos/figura_dedicada.md`: gráfico do Cap. 5 redesenhado para projeção
  (mesmos dados, tamanho da caixa do slide), em `scripts/figuras/`.
- `casos/troca_template.md`: achar, comparar e aplicar um template visual
  novo (SlidesCarnival, export do Canva, cores `srgbClr` × `schemeClr`).

## Convenções de conteúdo

- **Título é uma frase-afirmação** (o que o slide prova), não um rótulo.
  Duas linhas no máximo em 28 pt. Exceção aprovada (slide 5, 2026-10-19):
  título curto + **frase de abertura** logo abaixo (`referencia/design.md`).
- **Sem travessão "—"**, como no TCC. Sem nome de código na tela
  (`BAD_PLL`, `params.m`): na tela e na fala é "sintonia inadequada".
- **Sem RoCoF, sem "reaquisitar"** (memória do projeto, valem aqui também).
- **Deck = TCC entregue, sem acréscimo** (regra do Victor, 2026-10-17):
  todo número e afirmação da tela **e das notas** é o do TCC, com o mesmo
  arredondamento. Divergiu → vira o valor do TCC. Não está no TCC → sai,
  mesmo que esteja no KB ou no modelo. Nunca propor ressalva, aviso ou
  errata na fala. **Exceção de método** (Victor, 2026-10-18): etapa de
  modelagem que o TCC não descreve (bancada do PLL entre duas fontes
  ideais, montagem do inversor em etapas, slides 9 e 12) pode entrar como
  etapa, **sem número** fora do TCC; registrar em `pendencias.md` cada
  exceção aprovada. Erro do próprio TCC: o deck evita os dois lados, avisar o
  Victor, e a explicação vai para o material de perguntas
  (`scripts/notas/gen_defesa_qa.py`, skill tcc-pdf-notes).
- Legenda de figura: `Figura X.Y do TCC: <descrição curta>`, conferida por
  `check_pptx.py --tcc`. Renumerou figura no TCC → atualizar as legendas.
- Apêndice (depois do slide DIVIDER) é material para perguntas: não entra no
  tempo de fala, mas segue as mesmas regras de número e legenda.

## Divisão de trabalho por modelo

Mesma regra da `tcc-docx-editor`: o critério é custo total.

| Nível | Quem | Faz |
|---|---|---|
| Síntese | principal | Mensagem do slide, título, roteiro de fala, decisão de layout |
| Scripting | `pptx-scripter` (Sonnet) | `gen_*.py` a partir de spec fechada, quando a edição é grande ou repetitiva |
| Execução | `pptx-runner` (Haiku) | Staging, dumps, render, rodar scripts, finalize, entrega |
| Revisão | `slide-validator` (Sonnet) | Números × TCC/KB e defeitos visuais nos PNGs, antes da entrega |

- **Direto, sem agente**: 1-5 trocas de texto, uma figura, notas de até ~3
  slides. A spec teria o tamanho do script.
- **`slide-validator` sempre** que a entrega mexer em número, tabela,
  figura ou layout. Só nota de fala → basta o `tempo_fala.py`.
- Sessão em Sonnet não escala para Opus por conta própria.

## Scripts (`scripts/`, `python.exe` = `.venv\Scripts\python.exe`)

- `dump_slides.py <pptx> [--slides 3-7] [--notas] [--sem-texto] [--xml N]`:
  formas com nome, índice, tipo, caixa em polegadas, texto, tabelas, notas
- `find_text.py <pptx> <padrão> [--regex] [--notas] [-i]`: ocorrências e total
- `check_pptx.py <pptx> [--tcc <docx>] [--slides 1-16]`: FALHA = forma fora
  do slide, legenda "Figura X.Y do TCC" inexistente/tipo trocado; AVISO =
  texto talvez vazando (heurística), < 11 pt, imagem < 150 px/in, fonte fora
  do tema, travessão, nome de código, slide sem notas. Código 1 se FALHA
- `tempo_fala.py <pptx> [--ppm 130] [--limite 30]`: minutos por slide e por
  orador; código 1 acima do limite
- `troca_imagem.py <in> <slide> <forma> <png> <out> [--esticar]`: troca a
  mídia mantendo a caixa (cabe pela proporção, centrado)
- `diff_slides.py <antes> <depois> [--sem-notas]`: texto, tabelas, notas e
  hash das imagens, slide a slide
- `render.ps1 -In <pptx> -Out <pasta> [-Slides "3,5"] [-Folha]`: PNG pelo
  PowerPoint + folha-resumo 4 colunas
- `pptx_finalize.ps1 -In <montado> -Out <final> [-Pdf]`: prova que o
  PowerPoint abre sem reparo e regrava
- `entrega.ps1 -Final <final> -Dest <canônico> -Md5Staging <md5>`: fecha o
  PowerPoint pelo COM, MD5, backup, cópia, reabre
- `template_util.py`: `Rascunho` (formas para layouts), `desloca`,
  `rotulo_secao`, `estilo_chapado` (troca de template)
- `pptx_util.py`: `abrir`, `formas` (entra em grupos), `texto_forma`,
  `notas`, `falas`, `faixa` para os `gen_*.py`
- `edicoes.py`: classe `Edicao` com as edições conferidas (`troca_run`,
  `tira_run`, `notas`, `troca_img`, `linha_nova`, `alturas`, `duplica_slide`,
  `renumera_ids`, `move_slides`, `frase_abertura`) e `rodar`, que
  executa os grupos `g_*` do script. **Base de todo `gen_*.py`**
- `montagem.py`: `escreve` (parágrafos com subscrito `_{x}` e sobrescrito
  `^{x}`), `caixa` (polegadas), `copia`, `duplica_grupo` (etapa nova a
  partir de caixa + título + corpo), `tira`. Não reescrever no `gen_*.py`
- `folha_opcoes.py <saida.png> <rotulo=png>... [--recorte y0,y1]`: empilha
  os PNGs de variantes para a prévia com opções
- `figuras/gen_figs_defesa.py [5.3,5.7,...]` + `figuras/estilo.py`: figuras
  dedicadas ao deck em `assets/charts/defesa/` (`casos/figura_dedicada.md`)

## Workflow padrão

```
1. STAGING: OneDrive → C:\Temp\defesa_<tema>\deck.pptx; guardar o MD5
2. INSPEÇÃO: dump_slides (--sem-texto para achar a forma-alvo) / find_text;
   render.ps1 -Folha dos slides envolvidos (o "antes")
3. CONFERÊNCIA: casos/sincronia_tcc.md para todo número/figura que entra
4. PLANO (principal): slide, forma, texto antigo → novo, notas, layout
5. SCRIPT: C:\Temp\defesa_<tema>\gen_<tema>.py sobre edicoes.Edicao, uma
   função g_<grupo> por tipo de edição (txt, tab, img, notas...), lendo SEMPRE
   o deck do staging e gravando montado.pptx. PowerPoint recusou → bisseção:
   gen_<tema>.py <grupo> <saída> + render de cada variante
   PRÉVIA (toda mudança visível na tela): render -Folha do montado com os
   slides alterados e os vizinhos que a mudança afeta; ler os PNGs, corrigir
   o óbvio (quebra de título, texto encostando) e mostrar ao Victor o caminho
   completo do PNG + o que muda e o que fica igual. Só staging, nada no
   OneDrive. Ajuste pedido → nova prévia. AGUARDAR APROVAÇÃO do Victor
   (só nota de fala dispensa prévia: basta o texto no plano). Escolha de
   gosto (cor, destaque, título) → 2 a 4 variantes var_<X>.pptx no mesmo
   staging + folha_opcoes.py, com uma recomendação; a escolhida é a entregue
6. CHECKS: check_pptx --tcc (0 FALHA) + tempo_fala + render dos slides
   alterados → ler os PNGs; slide-validator quando couber
7. FINALIZE: pptx_finalize.ps1 [-Pdf]
8. ENTREGA: entrega.ps1 → diff_slides backup × canônico: só o que o plano previa
9. KB: deck_map / pendencias / historico_entregas (tcc-pptx/)
```
