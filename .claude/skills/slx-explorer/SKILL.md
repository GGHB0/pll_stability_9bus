---
name: slx-explorer
description: This skill should be used when the user asks about the Simulink model, specific blocks, parameters, subsystems, signals, or wants to inspect, modify, or understand anything inside pll_stability_9bus.slx or GridTiedInverterOptimalI2.slx. Activate when the user mentions "Simulink", "modelo", "bloco", "subsistema", "parâmetro do modelo", "InitFcn", "SID", or asks to read/change something in the .slx file.
version: 2.0.0
---

# SLX Explorer — Inspeção do Modelo Simulink sem MATLAB

O `.slx` é um ZIP de XMLs: cada subsistema mora em
`simulink/systems/system_<SID>.xml`. Leitura é feita por script, não por
trecho de código colado a cada sessão.

## Ferramenta principal: `scripts/slx_subsystem.py`

```bash
PY=.venv/Scripts/python.exe
$PY .claude/skills/slx-explorer/scripts/slx_subsystem.py 3974          # por SID
$PY .claude/skills/slx-explorer/scripts/slx_subsystem.py "PWM Control" # por nome (parcial)
$PY .claude/skills/slx-explorer/scripts/slx_subsystem.py 3963 --slx outro.slx --all-params
```

Imprime duas partes:

1. **Blocos**: tipo, nome, SID e os parâmetros que definem comportamento
   (Gain, Numerator/Denominator, Inputs do Sum, GotoTag, saturação do
   integrador...). Layout e cor ficam de fora; `--all-params` mostra tudo.
2. **Ligações**: `origem → destino[:inN]`, com nomes resolvidos e `Branch`
   aninhados expandidos.

**Use a parte de ligações para perguntas de estrutura** ("tem desacoplamento
ωL?", "o que vem depois do PI?", "tem feedforward?"). A lista de blocos diz o
que existe; só o grafo diz como está ligado. Em 2026-10-02 foi o grafo do
PWM Control que mostrou PI → notch → `m_dq`, sem ramo ωL nem `v_g`.

**Bloco na lista ≠ bloco em uso.** Antes de afirmar que um bloco atua,
achar o nome dele no grafo. No `3963`, o `Sinusoidal Measurement (PLL,
Three-Phase)` e o notch 120 Hz do PLL aparecem na lista, mas não têm
nenhuma ligação; o PLL que atua é Park → `Selector2` (v_q) → `PI` →
`Angle`. A KB descreveu o bloco solto como "o PLL do projeto" até
2026-10-02. "Quem usa o sinal X?" se responde seguindo X no grafo, não
pelo nome (`Vdq_rede` é só rótulo de scope).

Nome ambíguo → o script lista os candidatos com SID; repetir com o SID.
Subsistema dentro de subsistema: rodar no pai, pegar o SID do filho, rodar
de novo.

## Mapa dos subsistemas

SIDs, hierarquia e descrição funcional de cada bloco:
[simulink_model.md](../../kb/inverter/simulink_model.md). Pontos de entrada usuais:
`root` (rede IEEE 9 barras), `3896` (UFV Model), `3963` (Optimal
Controller), `3974` (PWM Control), `3997` (PWM VB).

## Parâmetros numéricos

**Não copiar valores para cá** (mudam a cada rodada). Fonte da verdade:
`params.m` na raiz; workflow e divergências propositais (Vcc ×1,5, ganhos
÷4) em [params_workflow.md](../../kb/simulation/params_workflow.md). Para ler o `InitFcn` gravado no `.slx`:

```python
import zipfile, xml.etree.ElementTree as ET
z = zipfile.ZipFile('pll_stability_9bus.slx')
root = ET.fromstring(z.read('simulink/blockdiagram.xml'))
print(next(p.text for p in root.iter('P') if p.get('Name') == 'InitFcn'))
```

## Equivalente no PSIM (modelo legado)

O PSIM não tem `.slx`, mas tem netlist em texto (`PSim/*.txt`): uma linha
por componente, `TIPO NOME nó1 nó2 ... parâmetros`. Para seguir um sinal,
grepar o número do nó:

```bash
grep -n -E "(^| )(53|78)( |$)" "PSim/01_Sistema PLL_vfinal_100MVA (backup)1.txt"
```

Componentes e nós já mapeados em [psim_netlists.md](../../kb/psim/psim_netlists.md).

## Armadilhas

- Saída com acento quebra no console do Windows: o script já força UTF-8;
  em código avulso, `PYTHONIOENCODING=utf-8`.
- Modificar o `.slx` por XML é possível mas arriscado: esta skill é para
  leitura. Escrita pontual (parâmetro de bloco) vai pelo MATLAB, por SID,
  porque nome de bloco pode ter quebra de linha (`Inverter
Active &
  Reactive Power `) e quebra o caminho em `set_param`:

  ```bash
  cp pll_stability_9bus.slx "$TEMP/antes.slx"
  matlab -batch "load_system('pll_stability_9bus'); h=Simulink.ID.getHandle('pll_stability_9bus:4060'); set_param(h,'Gain','2/3'); save_system('pll_stability_9bus')"
  ```

  Depois, extrair os dois ZIPs e conferir com `diff` que o
  `system_<SID>.xml` do pai mudou só no parâmetro. O resto do diff é
  reserialização do save (`ModelVersionFormat`, `Open=on`, ordem de opções
  no `configSet0.xml`, `visible` do Stateflow). O `.slx` pode ter
  alterações locais de outra pessoa: `save_system` as mantém, nunca
  `git checkout` antes.
- **Bloco de medição também se confere pela física.** O SID 4055 calculava
  P e Q com ganho 1/√3 nos dois (P saía ×√3/2, Q ×1,5) até 2026-10-03, e
  passou meses despercebido. Sinal derivado: refazer a conta a partir dos
  abc exportados e comparar com o valor logado ([simulink_model.md](../../kb/inverter/simulink_model.md)).
