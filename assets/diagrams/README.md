# Diagramas — SRF-PLL

Diagramas usados na secao "Arquitetura do SRF-PLL" do README principal.

| Arquivo | Tipo | Tema | Fonte de conteudo |
|---|---|---|---|
| `pll_system_circuit.svg` | SVG (circuito) | VSI + filtro LCL + Z_th + rede, com amostragem de tensao no PCC pelo PLL | `.claude/kb/inverter/lcl_filter.md`, `.claude/kb/pll/srf_pll_theory.md` |
| `pll_control_loop.svg` | SVG (controle) | Blocos do laco SRF-PLL: Park, PI (Kp+Ki/s), somador, integrador 1/s, realimentacao de fase | `.claude/kb/pll/srf_pll_theory.md`, `.claude/kb/pll/pll_gains_methodology.md` |
| `contingencies_attack.svg` | SVG (circuito + controle) | Circuito de referencia com 4 marcadores de falta + paineis dos 4 cenarios com mini-formas de onda de u_q | `.claude/kb/pll/pll_contingencies.md` |
| `gains_tradeoff.mmd` | Mermaid | Trade-off Kp/Ki (Secao 4.3 - Analise de Sensibilidade) | `.claude/kb/pll/pll_contingencies.md` |
| `vsi_grid_schematic.svg` / `.png` | SVG (blocos) | Figura 2.1 do TCC — esquematico generico VSI conectado a rede (fonte CC -> VSI -> filtro LCL -> PAC -> rede), com bloco de controle digital abstrato | `.claude/kb/tcc-word/content_map.md` |
| `voltage_sag_profile.svg` / `.png` | SVG (curva) | Figura 2.6 do TCC — perfil caracteristico de afundamento de tensao V(t): profundidade, duracao, tensao residual, limiar 0,9 pu | `.claude/kb/pll/pll_contingencies.md`, Bollen 2000 |
| `vsi_lcl_pwm_circuit.svg` / `.png` | SVG (circuito + controle) | Figura 3.1 do TCC — sistema GFL completo: circuito VSI trifasico 2 niveis (IGBTs S1-S6 + diodos antiparalelos), filtro LCL (L1/Cf/L2), TCs tipo janela (i_abc) e TP no PAC (u_abc), PAC Barra 2, e controle digital detalhado (abc->dq, SRF-PLL, bloco "Submodulo 2.10" / ONS_2_11 gerando i_d,ref e i_q,ref, PIs de corrente dq, dq->abc, PWM) | `.claude/kb/inverter/lcl_filter.md`, `.claude/kb/inverter/simulink_model.md`, `.claude/kb/standards/ons_2_11.md` |

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
