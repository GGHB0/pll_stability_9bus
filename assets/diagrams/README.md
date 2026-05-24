# Diagramas — SRF-PLL

Fontes Mermaid (`.mmd`) dos diagramas usados no README principal e em apresentacoes.

| Arquivo | Tema | Fonte de conteudo |
|---|---|---|
| `srf_pll_structure.mmd` | Estrutura do laco SRF-PLL com ganhos Kp/Ki do projeto | `.claude/kb/pll/srf_pll_theory.md`, `.claude/kb/pll/pll_gains_methodology.md` |
| `contingencies_attack_points.mmd` | Mapa das 4 contingencias e onde cada uma ataca o laco | `.claude/kb/pll/pll_contingencies.md` |
| `gains_tradeoff.mmd` | Trade-off Kp/Ki (Secao 4.3 - Analise de Sensibilidade) | `.claude/kb/pll/pll_contingencies.md` |

## Editar / exportar

GitHub renderiza Mermaid nativamente em blocos ` ```mermaid ` no README.

Para exportar como SVG/PNG (ex.: usar no TCC):

```bash
# instala mermaid-cli
npm install -g @mermaid-js/mermaid-cli

# exporta um diagrama
mmdc -i srf_pll_structure.mmd -o srf_pll_structure.svg
```

## Convencoes

- Sem acentos no texto (consistente com o README principal)
- Letras gregas escritas por extenso ou em notacao ASCII (`w_n`, `phi_i`, `delta-phi`)
- Cores por categoria de contingencia mantidas consistentes entre diagramas
