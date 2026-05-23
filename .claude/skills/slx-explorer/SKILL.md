---
name: slx-explorer
description: This skill should be used when the user asks about the Simulink model, specific blocks, parameters, subsystems, signals, or wants to inspect, modify, or understand anything inside pll_stability_9bus.slx or GridTiedInverterOptimalI2.slx. Activate when the user mentions "Simulink", "modelo", "bloco", "subsistema", "parâmetro do modelo", "InitFcn", "SID", or asks to read/change something in the .slx file.
version: 1.0.0
---

# SLX Explorer — Skill de Inspeção do Modelo Simulink

O arquivo `.slx` é internamente um ZIP com XMLs. **Não é necessário abrir o MATLAB** para ler a estrutura — use Python direto.

## Como Ler o Modelo

```python
import zipfile, xml.etree.ElementTree as ET, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

path = r'C:\projetos\pll_stability_9bus\pll_stability_9bus.slx'
with zipfile.ZipFile(path, 'r') as z:
    # Listar todos os arquivos internos
    for name in z.namelist():
        print(name)

    # Ler um sistema específico
    xml = z.read('simulink/systems/system_root.xml').decode('utf-8', errors='replace')
```

## Arquivos-Chave Dentro do .slx

| Arquivo | Conteúdo |
|---|---|
| `simulink/blockdiagram.xml` | InitFcn, parâmetros globais, configurações de simulação |
| `simulink/systems/system_root.xml` | Nível raiz: rede IEEE 9 barras, todos os top-level blocks |
| `simulink/systems/system_3896.xml` | UFV Model (subsistema do inversor VSI) |
| `simulink/systems/system_3963.xml` | Optimal Controller (PLL + controle dq) |
| `simulink/systems/system_3974.xml` | PWM Control (PI + filtros Notch) |
| `simulink/systems/system_3997.xml` | PWM VB (comparador SPWM, carrier triangular ±1) |
| `simulink/systems/system_3904.xml` | Gate Driver (6-pulse, Simulink→Simscape) |
| `simulink/systems/system_3933.xml` | Measurement inverter (sensores I/V) |
| `simulink/systems/system_3146.xml` | Gen1@Bus1 (AVR + Governor) |
| `simulink/systems/system_3214.xml` | Gen2@Bus2 (AVR + Governor) |

## Extrair Blocos de um Subsistema

```python
with zipfile.ZipFile(path, 'r') as z:
    xml = z.read('simulink/systems/system_XXXX.xml').decode('utf-8', errors='replace')
root = ET.fromstring(xml)
for block in root.iter('Block'):
    btype = block.get('BlockType', '')
    bname = block.get('Name', '').replace('\n', ' ')
    sid   = block.get('SID', '')
    # Parâmetros diretos
    params = {p.get('Name'): p.text for p in block.findall('P') if p.text}
    # Parâmetros de instância (blocos de biblioteca)
    idata  = {p.get('Name'): p.text for p in block.findall('InstanceData/P') if p.text}
    print(f'[{btype}] {bname} (SID={sid})')
```

## Ler o InitFcn (Parâmetros Numéricos)

```python
with zipfile.ZipFile(path, 'r') as z:
    xml = z.read('simulink/blockdiagram.xml').decode('utf-8', errors='replace')
root = ET.fromstring(xml)
for p in root.iter('P'):
    if p.get('Name') == 'InitFcn':
        print(p.text)
```

## Parâmetros Atuais do InitFcn (Referência Rápida)

```matlab
Vcc = 136363.6 V    L1 = 30.42 mH    L2 = 0.289 mH
C1  = 42.47 µF      wres = 9068.99 rad/s (fres ≈ 1443 Hz)
Kp  = 29.48/4       Ki  = 7075.6/4
Rth = 0.01004 Ω     Lth = 1.16 mH
Ts  = 5e-6 s        fsw = 5000 Hz    Tsc = 2e-4 s
```

## Encontrar um Subsistema por Nome (quando o SID é desconhecido)

```python
with zipfile.ZipFile(path, 'r') as z:
    # Buscar em system_root pelo nome do bloco
    xml = z.read('simulink/systems/system_root.xml').decode('utf-8', errors='replace')
root = ET.fromstring(xml)
for block in root.iter('Block'):
    if 'Nome Procurado' in block.get('Name', ''):
        print(block.get('SID'), block.get('Name'))
        # O SID mapeia para system_{SID}.xml
```

## Salvar Output em Arquivo (evitar encoding errors no PowerShell)

```powershell
python -c "
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
# ... código aqui ...
" | Out-File -Encoding utf8 ".claude\kb\_tmp_output.txt"
```

Lembre de deletar arquivos `_tmp_*.txt` após usar.

## Referência da Arquitetura

Ver `kb/inverter/simulink_model.md` para hierarquia completa de subsistemas e descrição funcional de cada bloco.
