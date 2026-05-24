# Diagramas — SRF-PLL

Diagramas usados na secao "Arquitetura do SRF-PLL" do README principal.

| Arquivo | Tipo | Tema | Fonte de conteudo |
|---|---|---|---|
| `pll_system_circuit.svg` | SVG (circuito) | VSI + filtro LCL + Z_th + rede, com amostragem de tensao no PCC pelo PLL | `.claude/kb/inverter/lcl_filter.md`, `.claude/kb/pll/srf_pll_theory.md` |
| `pll_control_loop.svg` | SVG (controle) | Blocos do laco SRF-PLL: Park, PI (Kp+Ki/s), somador, integrador 1/s, realimentacao de fase | `.claude/kb/pll/srf_pll_theory.md`, `.claude/kb/pll/pll_gains_methodology.md` |
| `contingencies_attack.svg` | SVG (circuito + controle) | Circuito de referencia com 4 marcadores de falta + paineis dos 4 cenarios com mini-formas de onda de u_q | `.claude/kb/pll/pll_contingencies.md` |
| `gains_tradeoff.mmd` | Mermaid | Trade-off Kp/Ki (Secao 4.3 - Analise de Sensibilidade) | `.claude/kb/pll/pll_contingencies.md` |

## Convencoes visuais

- **Paleta:** navy `#0B132B` para tracos do circuito, laranja `#F97316` para destaques (alinhado com `assets/banner.svg`)
- **Cores de contingencia consistentes entre diagramas:**
  - Sag simetrico / assimetrico: vermelho `#c92a2a`
  - Salto de fase / RoCoF: laranja `#e8590c`
  - Sondagem de tensao (V): azul `#1971c2`
  - Realimentacao de fase: roxo `#7c3aed`
- **Sem acentos** nos arquivos `.mmd` e em IDs SVG; acentos OK em texto SVG renderizado
- Fonte: `ui-sans-serif, system-ui` (cai para fonte do sistema)
- Fundo branco explicito (`<rect fill="#ffffff">`) para visibilidade em dark mode do GitHub

## Editar / exportar

GitHub renderiza SVG via `<img>` e Mermaid em blocos ` ```mermaid ` direto no README.

Para exportar o Mermaid como SVG/PNG (ex.: usar no TCC):

```bash
npm install -g @mermaid-js/mermaid-cli
mmdc -i gains_tradeoff.mmd -o gains_tradeoff.svg
```

Os SVGs ja podem ser convertidos para PNG/PDF com:

```bash
# via Inkscape (recomendado para qualidade)
inkscape pll_system_circuit.svg --export-type=png --export-dpi=300

# ou via rsvg-convert
rsvg-convert -f pdf pll_control_loop.svg -o pll_control_loop.pdf
```
