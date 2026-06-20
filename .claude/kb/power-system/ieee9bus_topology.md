---
name: ieee9bus-topology
description: Topologia do IEEE 9-bus modificado — base, adaptação TCC, cargas, geradores
---

# IEEE 9-bus — Topologia e Adaptação

## Base do Sistema

```
V_base = 20 kV    S_base = 100 MVA    Z_base = 4 Ω    f = 60 Hz
```

## Topologia Original

9 barras: 3 geradores síncronos (G1, G2, G3), 3 transformadores, 6 linhas de transmissão,
3 cargas. Rede de transmissão em 230 kV; terminais de geração em tensões próprias.

```
G1 (16.5 kV) → Trafo T1 → Bus 4 ─── Bus 5 ─── Bus 7 ─── Bus 2 ← G2 (18 kV)
                                  └── Bus 6 ─── Bus 9 ─── Bus 3 ← G3 (13.8 kV)
                                           └── Bus 8
```

Geradores:
- G1 @ Bus 1 (16.5 kV) → via TF 1-4 conecta à Barra 4 (230 kV)
- G2 @ Bus 2 (18 kV)   → via TF 2-7 conecta à Barra 7 (230 kV)
- G3 @ Bus 3 (13.8 kV) → via TF 3-9 conecta à Barra 9 (230 kV)

## Diagrama Unifilar Autoral

Arquivo SVG criado para o TCC: `assets/diagrams/ieee9bus_unifilar.svg`

Convenções do diagrama:
- Fundo branco, fonte Segoe UI, viewBox 920×680
- Barras de 230 kV: traço espesso preto vertical (⊥ ao condutor horizontal)
- Barras de gerador (1, 2, 3): traço espesso verde (#166534) ou âmbar (#b45309 para Bus 2/UFV)
- Transformadores T1/T2/T3: par de círculos (símbolo IEC), cor azul (#1e40af)
  - T2 centralizado entre B2 e B7: cx=174, cx=200
  - T3 centralizado entre B9 e B3: cx=719, cx=745
- Linhas de transmissão: traço fino (#4b5563), conexão perpendicular ao corpo das barras
  - L5-7 e L6-9: saem lateral da barra vertical → descem até barra horizontal
  - L4-5 e L4-6: saem da base das barras 5/6 → dobra → entram pelo topo da Barra 4
- Parâmetros R/X/B em três linhas separadas, próximos à respectiva linha
- Cargas A/B/C: traço vermelho (#b91c1c) com seta apontando para baixo

## Adaptação para o TCC

**G2 (Barra 2) substituído pelo inversor VSI grid-tied** com PLL SRF.
Sistema híbrido resultante:
- G1, G3 → máquinas síncronas com AVR + Governor
- Barra 2 → ponto de conexão (PAC) do VSI — inversor conecta via filtro LCL

No .slx: subsistema `Gen2@Bus2 PV 1.025 pu 163 MW` está **comentado** (Commented: on)
e substituído pelo subsistema `UFV Model` (SID=3896).

## Cargas

| Carga   | Barra | P (MW) | Q (MVAr) | V_rated |
|---------|-------|--------|----------|---------|
| Load A  | 5     | 125    | 50       | 230 kV  |
| Load B  | 6     | 90     | 30       | 230 kV  |
| Load C  | 8     | 100    | 35       | 230 kV  |

## Dados dos Geradores Síncronos

| Gerador | MVA   | kV   | xd     | xd'    | xq     | xq'    | xl     |
|---------|-------|------|--------|--------|--------|--------|--------|
| G1      | 247.5 | 16.5 | 0.1460 | 0.0608 | 0.0969 | 0.0969 | 0.0336 |
| G2      | 192.0 | 18.0 | 0.8958 | 0.1198 | 0.8645 | 0.1969 | 0.0521 |
| G3      | 128.0 | 13.8 | 1.3125 | 0.1813 | 1.2578 | 0.2500 | 0.0742 |

Todos os reatâncias em p.u. na base própria da máquina.
Fonte: Tabela 2.1 — Anderson & Fouad, "Power System Control and Stability".
