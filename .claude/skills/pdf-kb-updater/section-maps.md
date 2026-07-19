# Mapas de Seções de PDFs da Bibliografia

Páginas relevantes ao TCC em PDFs já explorados. Página = física do PDF
(1-indexed), não a impressa no rodapé.

## Yazdani & Iravani — *Voltage-Sourced Converters* (473 p.)

| Seção | Páginas | Conteúdo |
|-------|---------|---------|
| §8.3.4–8.3.5 | 233–238 | SRF-PLL: modelo, H(s) com zeros ±j2ω₀, Exemplo 8.1 |
| §8.4.1 | 241–244 | PI de corrente: kp=L/τi, ki=(R+ron)/τi |
| §8.4.2 | 246–248 | Critério de VDC: ≥ 2V̂t ou 1,74V̂t (3°H) |
| §8.6 | 256–265 | DC-bus voltage controller |
| §12.4.1 | 364–367 | PLL no sistema HVDC |
| §12.5.2–12.5.4 | 379–387 | PLL + controle de corrente sob falta assimétrica |
| Apêndice B | 448–452 | Base pu para VSC (Tabelas B.1, B.2) |

## ENTSO-E — *Grid Incident in Spain and Portugal on 28 April 2025* — Final Report (472 p.)

Arquivo: `Final Report on the Grid Incident in Spain and Portugal on 28 April 2025.pdf`

| Seção | Páginas | Conteúdo |
|-------|---------|---------|
| §1 Management Summary | 6–28 | Resumo completo: linha do tempo, análise técnica, root cause tree (Fig. 1-15, p.23), recomendações |
| §2.4 Inertia | 50–54 | Inércia do sistema ibérico antes do evento |
| §2.5 Oscillations | 54–80 | Dados das oscilações 0,63 Hz e 0,2 Hz pré-blackout |
| §3.1 Dynamic Behaviour | 116–140 | Comportamento dinâmico durante o incidente (PMU) |
| §4.1 Voltage control | 206–231 | Análise da falha de controle de tensão |
| §4.2 Oscillations | 231–278 | Análise modal: oscilação forçada converter-driven (0,63 Hz) e inter-área (0,2 Hz) |
| §4.6 Root Cause Tree | 331–336 | Árvore de causa raiz detalhada |
| §9 Conclusion & Recommendations | 451–465 | Conclusões e recomendações (numeradas, ligadas à árvore) |

Pontos de interesse para o TCC: oscilação 0,63 Hz classificada como
*converter-driven forced oscillation*; RES com fator de potência fixo sem
suporte de tensão; trips de sobretensão de inversores (< 1 MW e utility-scale)
com ajustes fora dos requisitos; paralelo com o apagão BR de ago/2023.
