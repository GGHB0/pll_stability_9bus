---
name: svg-diagrams
description: Cria qualquer SVG do projeto (diagramas, esquemáticos, curvas de norma, banners, ilustrações para README/KB/TCC) e exporta para PNG. Ativar sempre que o usuário pedir para criar/desenhar/gerar/ajustar um SVG, PNG, diagrama, esquemático, figura, banner ou ilustração — mesmo sem mencionar o formato (ex.: "precisa de uma figura do circuito do filtro LCL", "desenha o esquemático do VSI", "cria a curva do ONS", "atualiza o banner"). Também cobre gráficos com dados reais de simulação (waveforms, séries temporais do dashboard) e figuras didáticas que mostram como uma métrica é calculada — ver `data_charts.md`. Também usar para converter um SVG existente do repositório em PNG.
version: 2.0.0
---

# SVG Diagrams — Skill de Criação de Figuras e Exportação PNG

Cria SVGs no padrão visual do projeto e exporta o PNG correspondente. Vale para
qualquer arte vetorial do repositório: figuras do TCC (inseridas manualmente pelo
usuário no DOCX canônico — esta skill **não edita o docx**, ver
`tcc-docx-editor`), diagramas do README, ilustrações da KB e banner.

Destino padrão: `assets/diagrams/` para diagramas técnicos; `assets/` para artes
gerais (banner etc.). Na dúvida sobre o destino, pergunte.

Antes de desenhar, olhe 1-2 SVGs existentes em `assets/diagrams/` (ex.:
`pll_system_circuit.svg`, `current_control_dq_blocos.svg`) para absorver o
estilo real, não só a tabela abaixo.

## Mapa da skill

| Arquivo | Quando ler |
|---|---|
| `armadilhas.md` | **sempre**, antes do primeiro `<text>`/`<path>`: subscritos, chapéu `ω̂`, setas |
| `legibilidade.md` | figura que vai para o TCC: fonte px → pt na página, piso de fonte, roteiro "letra pequena" (recorte de viewBox, subscrito × seta) |
| `data_charts.md` | figura cujo conteúdo vem de CSV/simulação (matplotlib, gerador de SVG) |
| `export_png.md` | se `scripts/export_png.ps1` falhar ou para entender o que ele faz |
| `scripts/export_png.ps1` | SVG → PNG (Edge headless, lê o viewBox sozinho) |

## Figuras Orientadas a Dado — ver `data_charts.md`

Quando o conteúdo da figura vem do repositório e muda a cada re-simulação, ela
**não** é escrita à mão. Os casos abaixo estão todos detalhados em
`data_charts.md` (ler antes de começar qualquer um deles); os dois últimos são
variantes do caso didático:

| Caso | Ferramenta | Destino | Referência |
|---|---|---|---|
| Gráfico de dados reais (waveform, série temporal) | matplotlib direto do CSV | `assets/charts/` | `scripts/gen_regime_waveforms.py` |
| Layout desenhado, conteúdo lido do disco (matriz, inventário) | gerador que emite SVG | `assets/diagrams/` | `scripts/gen_matriz_cenarios.py` |
| Gráfico didático de métrica (mostrar de onde sai um número) | matplotlib + anotação | `assets/charts/` | `scripts/gen_retencao_didatica.py` |
| Anotar um oscilograma que já existe (área, patamar, média) | matplotlib + anotação | `assets/charts/` | `scripts/gen_potencia_didatica.py` |
| Plano de estado, quando o eixo do tempo é o gráfico errado | matplotlib | `assets/charts/` | `scripts/gen_plano_pq.py` |

Em todos, o script gerador é versionado em `scripts/gen_<nome>.py` e os números
saem calculados na hora, nunca digitados. O `savefig` do matplotlib gera SVG
**e** PNG direto, dispensando o `export_png.ps1`, que é só para SVG desenhado à mão.

> **Antes de dar qualquer uma delas por pronta, validar a legibilidade no
> tamanho da página** (`figsize` × largura de inserção). É o erro mais caro e
> mais invisível: o PNG em tamanho natural nunca denuncia. Procedimento em
> `data_charts.md`, seção "Validar a legibilidade no tamanho da página".

Para diagrama conceitual estável (circuito, laço de controle), nada disso se
aplica: continua sendo SVG escrito à mão, seguindo as convenções abaixo.

## Convenção Visual

| Elemento | Cor | Uso |
|---|---|---|
| Traços de circuito, texto principal | `#0B132B` (navy) | linhas, caixas neutras, títulos |
| Destaque / controle digital | `#F97316` (laranja) | blocos de controle, setas de comando |
| Fonte CC / grandezas "boas" | `#166534` (verde) | fonte primária, indicadores positivos |
| Conversor / VSI | `#1d4ed8` (azul forte), fundo `#dbeafe` | bloco do inversor |
| Filtro / elemento passivo | `#b45309` (âmbar), fundo `#fef3c7` | filtro LCL, elementos de acoplamento |
| Sensoriamento / medição | `#1971c2` (azul) | sondas de tensão/corrente, realimentação |
| Contingência (sag simétrico/assimétrico) | `#c92a2a` (vermelho) | ver `README.md` da pasta para o restante da paleta de faltas |

Regras fixas:
- `viewBox` proporcional ao conteúdo (não fixar `width`/`height` no elemento raiz — deixe o
  viewport de exportação controlar a escala real).
- Fundo branco explícito: `<rect width="..." height="..." fill="#ffffff"/>` como primeiro filho.
- Fonte: `font-family="ui-sans-serif, system-ui, -apple-system, sans-serif"`.
- Texto em português com acentos é permitido no SVG (diferente dos `.mmd`, que devem ficar sem acento).


Legibilidade no TCC, em uma linha: `pt ≈ font_px × L_cm × 28,35 / W_viewBox`;
piso ~13 px para W≈920 (≈ 7 pt). Não cabe → encolher o `viewBox`, nunca
aumentar a fonte. Detalhes e tabela em `legibilidade.md`.

## Figura pedida pelo orientador "similar à do livro X"

A figura do livro é **referência de estilo, não de conteúdo**. O pedido
costuma vir de comentário do Oscar e pede adaptação ao modelo. Roteiro:

1. **Comentário:** `tcc-docx-editor/scripts/dump_comments.py <docx> --grep "fig"`
   traz o pedido exato e o trecho ancorado.
2. **Figura do livro:** `grep -n "FIGURE 8.10" ~/pdfext/*.txt` (o texto
   extraído já está lá; sem extração, `pdf-extractor`). Nunca `find /` no
   disco: trava por minutos.
3. **Modelo real:** `slx-explorer/scripts/slx_subsystem.py <SID|nome>` (o
   grafo de ligações mostra o que existe) e a netlist do PSIM (`PSim/*.txt`).
4. **Desenhar** só o que o modelo tem. Bloco do livro ausente no modelo
   (ex.: desacoplamento ωL e feedforward) fica **fora da figura, inclusive
   da planta**: o Victor quer "só o que realmente está no nosso
   controlador" (2026-10-02; v_g e ωL na planta foram recusados). **Fonte: "Adaptado de Autor (ano)."** sempre que a figura se
   apoia numa obra, mesmo desenhada sobre o modelo (D10 em
   `tcc-abnt-layout/decisoes.md`); "Os autores (2026)." só sem obra por trás.
5. **Conferir o texto do TCC:** se o parágrafo promete o bloco ausente, avisar
   o usuário e propor a frase corrigida (não editar o DOCX daqui).

Caso de referência: `current_control_dq_blocos.svg` (2026-10-02).

## Exportar para PNG

```powershell
.claude\skills\svg-diagrams\scripts\export_png.ps1 assets\diagrams\figura.svg   # -Scale 3 por padrão
```

Pelo Git Bash: `powershell.exe -NoProfile -ExecutionPolicy Bypass -File
.claude/skills/svg-diagrams/scripts/export_png.ps1 <svg>`. Grava o PNG ao lado
do SVG. **Conferir o PNG com `Read`** antes de dar por pronto: subscrito,
seta e colisão só aparecem no raster.

## Depois de Criar a Figura

- Se o arquivo ficou em `assets/diagrams/`, adicione uma linha na tabela de
  `assets/diagrams/README.md` (arquivo, tipo, tema, fonte de conteúdo).
- Achado sobre o modelo durante o desenho (ex.: bloco que a KB descreve e o
  `.slx` não tem) vai para a KB do tema, não só para a conversa.
- Confirme que o `.svg` e os `.md` da skill continuam ≤ 200 linhas
  (`.claude/rules/limits.md`) — se crescer, quebre em elementos reutilizáveis
  (`<defs>`/`<use>`) em vez de duplicar blocos.
- Não toque no `.docx` — a inserção da figura no Word é manual pelo usuário.
