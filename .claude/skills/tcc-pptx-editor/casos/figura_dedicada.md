# Figura dedicada ao deck

Continuação de `SKILL.md`; complementa `casos/troca_figura.md`. Pedido do
Victor (2026-10-18): as figuras do Cap. 5 do TCC, encolhidas na moldura do
slide, ficam ilegíveis no projetor. O deck usa então uma **versão
redesenhada dos mesmos dados**, no tamanho da caixa do slide.

## Quando fazer

- Gráfico gerado por script do projeto (`scripts/gen_*.py`, Cap. 5) cujo
  texto, na escala do slide, cai abaixo de ~11 pt, ou com painéis
  espremidos (2x2 em menos de 6 in).
- Diagrama de blocos fica idêntico ao do TCC, salvo pedido do Victor:
  a Fig. 4.3 (slide 7) e a Fig. 3.2 (slide 5) foram redesenhadas em 2026-10-18 em SVG à mão
  (`assets/diagrams/pll_control_loop_defesa.svg`, skill `svg-diagrams`),
  com os mesmos blocos, sinais e ligações; equação que sai da figura vira
  texto nativo num cartão do slide (deepcopy de um cartão vizinho;
  runs Cambria Math 20 pt, subscrito `baseline=-25000`, sobrescrito `30000`).

## O que muda e o que nunca muda

| Pode mudar | Nunca muda |
|---|---|
| Tamanho (= caixa da imagem no slide), fonte, espessura de linha | Dados, janela de tempo, eixos e escala |
| Título interno (sai: o título do slide faz o papel) | Séries mostradas e a cor de cada sintonia |
| Anotação cujo número já está na tabela ou nos cartões do slide (sai) | Valor anotado que fica (mesmo do TCC, calculado pela mesma função) |
| Posição da legenda e dos rótulos "falta"/"eliminação" | Painéis: um 2x2 do TCC continua 2x2 |
| Nota de rodapé explicativa (vai para a fala) | Nada anotado que o TCC não traga |

- Legenda no slide: **"Figura X.Y do TCC: ..."**, como antes (Victor,
  2026-10-18): a banca acha a figura no texto e o `check_pptx.py --tcc`
  segue conferindo o número.
- Cores do `design.md` (azul `2563EB` nominal, laranja `EA580C`
  inadequada); fonte Calibri; piso 12 pt na tela.

## Onde fica o código

- `scripts/figuras/estilo.py`: `aplica()` (rcParams do deck), `figura(caixa)`
  no tamanho exato em polegadas, `eixos`, `salva` (SVG + PNG 300 dpi em
  `assets/charts/defesa/`).
- `scripts/figuras/gen_figs_defesa.py`: uma função `fig_<N_M>()` por figura
  e o dicionário `CAIXA` com a caixa da imagem de cada slide. **Dados e
  métricas sempre pelas funções do gerador do TCC** (`gen_erro_fase.load`,
  `rel_window`, `metrics`; `gen_espectro_vd.espectro`; P/Q por
  `src/pipeline/pq.py`), nunca leitura própria do CSV: assim o número é o
  do TCC por construção.
- `estilo.aplica()` vem **depois** de importar os geradores do TCC, que
  mexem no rcParams ao importar.

```text
python.exe .claude\skills\tcc-pptx-editor\scripts\figuras\gen_figs_defesa.py 5.7,5.18
```

## Fluxo

1. Caixa da imagem no slide (`dump_slides.py`); se a moldura for estreita
   demais para o conteúdo, alargar na grade do `design.md` (2 colunas =
   5,82 in) e estreitar o vizinho no mesmo `gen_*.py` do staging.
2. `fig_<N_M>` nova (molde: as existentes) → rodar → ler o PNG.
3. `gen_*.py` do staging com `ed.troca_img` (a proporção já casa com a
   caixa) → `check_pptx --tcc` → render.
4. `slide-validator` com a figura nova **e** a original do TCC
   (`assets/charts/<nome>.png` ou a mídia do deck anterior) lado a lado.
5. Entrega e KB como sempre (`deck_map`: coluna de figura aponta para
   `assets/charts/defesa/`).

Figura nova com o padrão já fixado: spec para o `pptx-scripter` (figura do
TCC, função do gerador que dá os dados, caixa, o que sai).

## Feitas

| Slide | Figura | Arquivo | O que saiu |
|---|---|---|---|
| 14 | 5.3 | `fig_5_3` | nota "nos primeiros ms..." |
| 16 | 5.7 | `fig_5_7` | 4 caixas pico/retorno (na tabela), legenda 1º ciclo/faixa |
| 17 | 5.10 | `fig_5_10` | nota das trifásicas em 120 Hz (faixa do slide 16) |
| 7 | 4.3 (diagrama) | `pll_control_loop_defesa.svg` | título interno, rótulos cinza; equações viram cartão |
| 5 | 3.2 (diagrama) | `vsi_grid_blocos_defesa.svg` | notação u → v, SRF-PLL em laranja, letras maiores |
| 17 | 5.18 | `fig_5_18` | linhas de pico/retorno (98 ms no cartão), legenda 1º ciclo/faixa |

Pendentes (apêndice): 5.14 (slide 22), 5.5/5.6 (23), 5.20/5.21 (26).
