---
name: claude-index
description: Índice de navegação do sistema .claude/ — o que existe, onde está e quando usar
---

# Índice do Sistema .claude/

## Knowledge Base — `kb/`

| Arquivo | Quando usar |
|---|---|
| `kb/project-scope.md` | Visão geral do TCC: capítulos, status, motivação, conexões entre artefatos |
| `kb/pll/srf_pll_theory.md` | Teoria do SRF-PLL: Park transform, modelo linear, tipo 2, equivalência EPLL |
| `kb/pll/pll_gains_methodology.md` | Kp/Ki (eqs. 3.21-3.22 TeseAGP), Lest, tabela de margem de fase vs. Lg |
| `kb/pll/pll_contingencies.md` | 4 cenários de contingência, métricas IAE/ISE/LVRT, trade-off dos ganhos |
| `kb/inverter/lcl_filter.md` | Dimensionamento L1/L2/C1, critérios de ripple e ressonância, filtro Notch |
| `kb/inverter/simulink_model.md` | Arquitetura completa do .slx: SIDs, InitFcn, hierarquia de subsistemas |
| `kb/power-system/ieee9bus.md` | Topologia IEEE 9 barras, impedâncias, metodologia Ybarra→Zbarra→Z22 |
| `kb/power-system/machine_inertia.md` | Equação de oscilação, critério das áreas iguais, cadeia H↓→RoCoF→PLL lock-loss→P=0 |
| `kb/standards/lvrt.md` | LVRT IEEE 1547-2018, suporte reativo, ligação com evento 15/08/2023 |

## Comandos — `commands/`

| Arquivo | Conteúdo |
|---|---|
| `commands/git.yaml` | Fluxo padrão de commit/push/branch com regras do projeto |

## Skills — `skills/`

| Skill | Quando ativa |
|---|---|
| `skills/slx-explorer/` | Qualquer pergunta sobre o modelo Simulink (.slx): blocos, parâmetros, subsistemas |

## Regras — `rules/`

| Arquivo | Regra |
|---|---|
| `rules/limits.md` | Máximo 200 linhas por arquivo; formatos por pasta; mapa de temas da KB |

## Fluxo de Ingestão de PDFs

1. Usuário fornece o PDF e indica o tema
2. Extrair via `PyPDF2` (disponível no ambiente)
3. Salvar na subpasta correta de `kb/` respeitando o limite de 200 linhas
4. Fazer commit + push

## Conexões Importantes

- **TeseAGP** = tese de doutorado do coorientador Prof. André Guilherme Peixoto Alves
- **Kp/Ki divididos por 4 duas vezes**: veja `kb/pll/pll_gains_methodology.md`
- **Capítulo 4 do TCC está vazio**: é o trabalho principal restante (simulações EMT)
- **Gen2@Bus2** ainda existe no .slx junto com o UFV Model — verificar se desconectado
