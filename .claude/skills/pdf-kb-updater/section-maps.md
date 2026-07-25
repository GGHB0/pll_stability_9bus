# Mapas de Seções de PDFs da Bibliografia

Páginas relevantes ao TCC em PDFs já explorados. Página = física do PDF
(1-indexed), não a impressa no rodapé.

## Yazdani & Iravani — *Voltage-Sourced Converters* (473 p.)

| Seção | Páginas | Conteúdo |
|-------|---------|---------|
| §2 DC/AC Half-Bridge | 23–46 | Conversor half-bridge, PWM (2.3.1), modelo comutado e médio |
| §4.2–4.6 Space Phasors & Frames | 69–113 | Space phasor, Clarke αβ (§4.5, p. 91–99), Park dq (§4.6, p. 101–113), potência e controle |
| §5 Two-Level VSC | 115–125 | Topologia VSC 2-níveis, estrutura, operação, modelos em αβ e dq |
| §8.1–8.6 dq-Frame Control | 204–242 | Controle em referencial dq: PLL (§8.3.4, p. 211–215), PI de corrente (§8.4.1, p. 217–225), DC-bus |
| §8.3.4–8.3.5 | 233–238 | SRF-PLL: modelo, H(s) com zeros ±j2ω₀, Exemplo 8.1 |
| §8.4.1 | 241–244 | PI de corrente: kp=L/τi, ki=(R+ron)/τi |
| §8.4.2 | 246–248 | Critério de VDC: ≥ 2V̂t ou 1,74V̂t (3°H) |
| §8.6 | 256–265 | DC-bus voltage controller |
| §12.4.1 | 364–367 | PLL no sistema HVDC |
| §12.5.2–12.5.4 | 379–387 | PLL + controle de corrente sob falta assimétrica |
| Apêndice B | 448–452 | Base pu para VSC (Tabelas B.1, B.2) |

**Arquivos .txt gerados em ~/pdfext/ durante mapeamento (2026-07-19):**
- `yazdani_half_bridge_pwm.txt` — Cap. 2, p. 23–46
- `yazdani_clarke_park.txt` — Cap. 4, p. 69–113
- `yazdani_two_level_vsc.txt` — Cap. 5, p. 115–125
- `yazdani_dq_frame_control.txt` — Cap. 8, p. 204–242

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

## IEEE Std 1547.2-2023 — Application Guide for IEEE Std 1547-2018 (291 p.)

Arquivo na bibliografia: `805035543-Ieee-Standard-1547-2018.pdf` — **atenção**,
o nome do arquivo é enganoso: o conteúdo real é o *Application Guide*
1547.2-2023 (comentado, com racional/tabelas/figuras), não o standard
normativo 1547-2018 puro. Confirmado pelo metadata `/Title` extraído via
pypdf — sempre checar `toc.txt` antes de assumir o conteúdo pelo nome do
arquivo.

| Seção | Páginas | Conteúdo |
|-------|---------|---------|
| §5.2–5.4 Reactive power capability / volt-var / volt-watt | 75–83 | Modos de controle reativo em regime permanente (contraste com DVS) |
| §6.2 Area EPS faults / região de operação contínua | 92–108 | Faltas, reclosing, região contínua 0,88–1,10 pu |
| §6.4 Voltage (mandatory trip + ride-through) | 113–127 | Table 8 (trip UV1/UV2/OV1/OV2 por categoria), regiões de operação, Dynamic Voltage Support (§6.4.2.6), Tabela 9 |
| Annex C — Illustration of ride-through/trip requirements | 231–234 | Figuras C.1–C.4 (só legendas/fonte extraível — curvas são imagens, valores numéricos completos estão nas Table 14/15/16 do 1547-2018 normativo, não neste guia) |
| Annex I — Case studies on DVS performance | 263–277 | Estudos de caso CAISO e Entergy: impacto de categoria/DVS na recuperação de tensão do sistema em alta penetração de DER |

**Arquivos .txt gerados em ~/pdfext/ (2026-07-25):**
- `ieee1547_53_54_voltvar.txt`, `ieee1547_62_faults.txt`,
  `ieee1547_64_voltage.txt`, `ieee1547_annexC_ridethrough.txt`,
  `ieee1547_annexI_casestudies.txt`

Sintetizado em `.claude/kb/standards/ieee1547_ride_through.md` e
`.claude/kb/standards/ieee1547_case_studies.md`.

## Hu, Meng, Bu, Ren — *Test and Analysis of LVRT Characteristic of Wind Farm* (6 p.)

Artigo curto (IJAPE Vol.2 Issue 4, 2013), sem outline — extraído por inteiro em
`~/pdfext/lvrt_windfarm_full.txt` (2026-07-25). Teste de campo real em turbina
PMSG 850 kW, norma chinesa Q/GDW392-2009. Conteúdo: fórmula de corrente reativa
dinâmica, dados de teste simétrico vs. assimétrico (desequilíbrio de corrente
entre fases). Sintetizado em
`.claude/kb/standards/china_lvrt_windfarm_test.md`.
