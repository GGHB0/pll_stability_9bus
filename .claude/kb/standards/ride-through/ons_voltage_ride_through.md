---
name: ons-voltage-ride-through
aliases: [ons-voltage-ride-through]
description: Envelope de suportabilidade a subtensões e sobretensões dinâmicas (ONS Subm. 2.10 §5.7, Figura 13) e leitura das Figuras 2.1 e 2.2 do TCC
source: ONS, Submódulo 2.10, rev. 2025.02, itens 5.2.4, 5.7 e 5.8, pp.24-31 (texto extraído em ~/pdfext/ons_2_10_full_text.txt)
references:
  - "OPERADOR NACIONAL DO SISTEMA ELÉTRICO (ONS). Procedimentos de Rede — Submódulo 2.10: Requisitos técnicos mínimos para a conexão às instalações de transmissão. Revisão 2025.02, vigência 01/03/2025."
---

# ONS Submódulo 2.10 — Envelope de Tensão (§5.7) e Figuras do TCC

## O que a área do envelope significa

§5.7.1: diante de variações temporárias de tensão decorrentes de distúrbios na
Rede Básica, a central "deve continuar operando (sem desconexão), se a tensão
nos terminais dos aerogeradores ou inversores permanecer dentro da região
indicada na Figura 13".

- **Dentro do envelope:** permanência obrigatória, sem desconexão.
- **Fora (abaixo da borda inferior ou acima da superior):** a norma deixa de
  exigir a permanência, ou seja, a desconexão é permitida.
- **t = 0** é o início do distúrbio.
- §5.7.1.1: vale para qualquer distúrbio (rejeição de carga, defeito simétrico
  ou assimétrico) e é aferido pela **fase com maior variação**. Não é a tensão
  de sequência positiva, que é a grandeza da Figura 14 (§5.8).

| Borda | Trecho | Valor |
|---|---|---|
| Inferior | 0 a 0,5 s | 0,2 pu |
| Inferior | 0,5 a 1 s | rampa 0,2 → 0,85 pu |
| Inferior | 1 a 5 s | 0,85 pu |
| Inferior | após 5 s | 0,9 pu |
| Superior | 0 a 2,5 s | 1,2 pu |
| Superior | após 2,5 s | 1,1 pu |

O título do §5.7 é "subtensões **e sobretensões** dinâmicas": a figura tem as
duas bordas. A legenda da Figura 2.1 do TCC fala só em subtensões.

A Figura 13 do ONS termina logo depois de 5 s. A norma não diz que a faixa
0,9–1,1 pu vale "indefinidamente": a operação em tensão não nominal por tempo
ilimitado está no §5.2.4 (a), que remete ao critério do Submódulo 2.3. Por
isso a figura do TCC deixa a borda direita aberta, sem rótulo.

## Figura 14 (§5.8), corrente reativa: convenção de sinal

Na figura do ONS, ΔI_Q/I_n = +1 na subtensão (fornecimento) e −1 na
sobretensão (consumo). O código da [[ons-2-11]] usa o sinal oposto no
`iq_ref` (negativo = injeção), por convenção do eixo dq. **Não é erro da
figura.** A zona 0,85–1,10 pu é a banda morta, sem injeção adicional.
Ajustes padrão (§5.8.3): V1 = 0,5 pu e V2 = 1,2 pu.

## Figuras 2.1 e 2.2 do TCC (refeitas em 2026-09-26)

A primeira versão copiava o desenho do ONS sem rotular as áreas, com "Time
(s)", a legenda interna "Figura 13" duplicando a legenda ABNT e travessão no
título. Duas versões por figura, em `assets/diagrams/`:

| Destino | Arquivos | Diferença |
|---|---|---|
| TCC (Word) | `ons_voltage_ridethrough_envelope_tcc`, `ons_reactive_current_curve_tcc` | Sem título nem fonte internos (vão na legenda ABNT); viewBox 740 px, fontes de 13 a 15 px (~8 a 9 pt a 16 cm) |
| README | `ons_voltage_ridethrough_envelope`, `ons_reactive_current_curve` | Mesmo desenho, com título e notas de norma (§5.7.1.1, §5.2.4, §5.8.2, §5.8.4, sinal) |

A versão README é o desenho da `_tcc` envolvido em título e rodapé. Qualquer
mudança no desenho vai **primeiro** na `_tcc` e depois é propagada.

## Relacionados

- [[lvrt-standards]]: conceito geral de LVRT e o equivalente IEEE 1547
- [[ons-2-11]]: implementação da Figura 14 no Simulink
- [[tcc-historico-entregas]]: entrega das figuras no V10
