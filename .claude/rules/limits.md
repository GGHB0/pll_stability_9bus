---
name: file-size-limits
type: rule
applies_to: [kb, commands, rules]
---

# Limites de Arquivo

- Nenhum arquivo dentro de `.claude/` pode ultrapassar **200 linhas**.
- Qualquer arquivo `.md` do repositório (não só `.claude/`) que ultrapassar
  **200 linhas** deve ser fragmentado em arquivos menores por subtema —
  proativamente, sem esperar o usuário pedir.
  - **Exceção**: `README.md` — ponto de entrada padrão do projeto, fica de
    fora dessa regra mesmo acima de 200 linhas.
- Se o conteúdo crescer além disso, dividir em arquivos menores por tema.
- Formatos aceitos por pasta:
  - `kb/` → `.md` (texto narrativo, bases de conhecimento)
  - `commands/` → `.yaml` (comandos estruturados, reutilizáveis)
  - `rules/` → `.md` (regras e restrições para o Claude)

# Estrutura de KB

Subpastas criadas sob demanda, quando o primeiro conteúdo chegar:

| Pasta | Conteúdo |
|---|---|
| `kb/pll/` | Teoria SRF-PLL + implementação Simulink do PLL |
| `kb/inverter/` | VSI, filtro LCL, controle de corrente |
| `kb/power-system/` | IEEE 9 barras, Ybarra, Thevenin |
| `kb/simulation/` | Workflow notebook↔params.m, Vcc override, runtime (Ts/fsw/Tsc) |
| `kb/standards/` | IEEE 1547-2018, ONS, LVRT |
| `kb/events/` | Apagão BR agosto 2023 |
| `kb/dashboard/` | Relatório HTML, com subpastas `dados/`, `graficos/`, `cards/`, `layout/` |

MATLAB/Simulink é ferramenta — conhecimento sobre implementação vai na pasta do tema, não em pasta separada.
