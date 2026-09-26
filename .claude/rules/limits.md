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
| `kb/pll/` | SRF-PLL, com subpastas `teoria/`, `sintonia/` (ganhos do PI), `contingencias/`, `notch/` (histórico) |
| `kb/inverter/` | VSI, filtro LCL, controle de corrente |
| `kb/power-system/` | Rede e estabilidade, com subpastas `ieee9bus/` (topologia, linhas, Thevenin), `inercia/` (H, estimação, virtual), `estabilidade/` (classificação, panorama IEA) |
| `kb/simulation/` | Workflow notebook↔params.m, Vcc override, runtime (Ts/fsw/Tsc) |
| `kb/standards/` | Normas, com subpastas `qualidade-energia/` (harmônicos, IEEE 519, 1547 Cl.7) e `ride-through/` (LVRT, ONS) |
| `kb/events/` | Blecautes reais, uma subpasta por evento: `brasil-2023/`, `chile-2025/`, `iberia-2025/` |
| `kb/dashboard/` | Relatório HTML, com subpastas `dados/`, `graficos/`, `cards/`, `layout/` |
| `kb/tcc-word/` | TCC DOCX: `content_map`/`pendencias` na raiz; subpastas `conteudo/`, `docx/`, `revisao-fragmento/`, `historico/` |
| `kb/psim/` | Fase inicial de modelagem no PSIM (Altair), anterior ao Simulink — registro histórico |

## Subpastas temáticas

- **Doc novo vai na subpasta do tema**, nunca solto na raiz de uma pasta que já
  tem subpastas. Raiz só guarda doc transversal (ex.: `tcc-word/content_map.md`).
  Nenhuma subpasta serve → criar uma nova e registrá-la na tabela acima.
- **Dividir em subpastas** quando a pasta passar de ~8 docs: nomes em
  português, kebab-case, por tema (`sintonia/`) ou por evento (`chile-2025/`).
  Com ≤ 8 docs, fica plana (`inverter/`, `simulation/`).
- **`_index.yaml` aninhado** (formato de `pll/_index.yaml`): `folder`,
  `description`, `files:` da raiz, depois `subfolders:` com `folder`,
  `description` e `files:` próprios. O `kb_links.py all` acrescenta o doc
  novo no fim do `files:` da raiz: mover a entrada à mão para o bloco da
  subpasta (subpasta nova também é entrada manual).
- **Ao mover doc:** `git mv` (preserva histórico), corrigir links markdown
  relativos e menções por caminho (`pll/x.md` → `pll/sintonia/x.md`) no repo
  inteiro (skills, agentes, CLAUDE.md, README, `assets/`, `docs/`, notebooks).
  Menção solta vira `[[slug]]`, que não quebra com move. Rodar o `all` e
  atualizar a tabela acima.

MATLAB/Simulink é ferramenta — conhecimento sobre implementação vai na pasta do tema, não em pasta separada.

Exceção — `kb/psim/`: o PSIM foi o **ambiente legado** onde a modelagem começou,
não a implementação atual. Por ser uma fase histórica distinta (não a ferramenta
corrente), tem pasta própria. Isso **não** autoriza uma pasta `kb/simulink/`: o
Simulink é a ferramenta atual e seu conhecimento continua por tema.
