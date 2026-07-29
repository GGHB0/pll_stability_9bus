# Mapas de Seções de PDFs da Bibliografia

Páginas relevantes ao TCC em PDFs já explorados. Página = física do PDF
(1-indexed), não a impressa no rodapé.

## Yazdani & Iravani — *Voltage-Sourced Converters* (473 p. — livro completo)

**ATENÇÃO (2026-07-28):** as linhas §2 e §4.2–4.6 abaixo (mapeadas em
2026-07-19) **não foram reverificadas** contra `toc_fixed_yazdani.txt` e podem
estar deslocadas — ver gotcha de paginação em [scripts.md](scripts.md). As
linhas §8.3.4/§8.4.1/§12.4.1/§12.5.2–12.5.4 batem exatamente com o TOC
resolvido e são confiáveis. As linhas novas (4.2.4/4.3.3/12.5.1–12.5.7) foram
extraídas e **lidas na íntegra** em 2026-07-28, confirmadas corretas.

| Seção | Páginas | Conteúdo |
|-------|---------|---------|
| §2 DC/AC Half-Bridge | 23–46 (não reverificado) | Conversor half-bridge, PWM (2.3.1), modelo comutado e médio |
| §4.2–4.6 Space Phasors & Frames | 69–113 (não reverificado) | Space phasor, Clarke αβ, Park dq, potência e controle |
| §4.2.4 Harmonics (space-phasor) | 103–104 | Harmônico como space-phasor; seq. pos/neg/zero por ordem n (Tabela 4.1) |
| §4.3.3 Asymmetrical 3-Phase Systems | 110 | Seção curta: sistema assimétrico não tem função de transferência space-phasor única; modelagem deve ir para αβ ou dq |
| §5 Two-Level VSC | 115–125 | Topologia VSC 2-níveis, estrutura, operação, modelos em αβ e dq |
| §8.1–8.6 dq-Frame Control | 204–242 | Controle em referencial dq: PLL (§8.3.4, p. 211–215), PI de corrente (§8.4.1, p. 217–225), DC-bus |
| §8.3.4–8.3.5 | 233–238 | SRF-PLL: modelo, H(s) com zeros ±j2ω₀, Exemplo 8.1 |
| §8.4.1 | 241–244 | PI de corrente: kp=L/τi, ki=(R+ron)/τi |
| §8.4.2 | 246–248 | Critério de VDC: ≥ 2V̂t ou 1,74V̂t (3°H) |
| §8.6 | 256–265 | DC-bus voltage controller |
| §12.4.1 | 364–367 | PLL no sistema HVDC |
| §12.5.1–12.5.4 | 376–382 | Tensão PCC sob falta (seq. simétricas), performance do PLL, controle de corrente dq, dinâmica do barramento CC — tudo sob falta assimétrica |
| §12.5.5 | 387–391 | Geração de 3º harmônico via ripple 2ω₀ do barramento CC; mitigação por feed-forward de VDC real |
| §12.5.6–12.5.7 | 391–393 | Fluxo de potência e controle de VDC sob falta assimétrica |
| Apêndice B | 448–452 | Base pu para VSC (Tabelas B.1, B.2) |

**Arquivos .txt gerados em ~/pdfext/:**
- `yazdani_half_bridge_pwm.txt`, `yazdani_clarke_park.txt`,
  `yazdani_two_level_vsc.txt`, `yazdani_dq_frame_control.txt` (2026-07-19,
  páginas não reverificadas)
- `FIX_yazdani_4.2.4_4.3.3_Harmonics_Asymmetrical.txt` (p.103–113),
  `FIX_yazdani_12.5.1_12.5.4_PLL_Asymmetrical_Fault.txt` (p.375–382),
  `FIX_yazdani_12.5.4_12.5.7_LowOrderHarmonics_Fault.txt` (p.382–393)
  (2026-07-28, páginas confirmadas via `get_destination_page_number`)

## TeseAGP — André G. P. Alves, COPPE/UFRJ (194 p.)

Título real: "Metodologia para Auto-Ajuste de Controladores de Corrente em
Conversores Fonte de Tensão Conectados a Redes Sujeitas a Distúrbios
Harmônicos". Coorientador do TCC.

| Seção | Páginas | Conteúdo |
|-------|---------|---------|
| §2.1.1 Ressonância/instabilidade | 31–39 | Impedância de rede, critério de Nyquist (Jessen&Fuchs, Harnefors), rede real medida na Alemanha |
| §2.5 Controladores Ressonantes | 58–60 | Cita IEEE 519-2014 + IEEE 1547-2018 como normas de limite de harmônico de corrente p/ unidades geradoras; exemplo publicado: 3ª/5ª/7ª de 8,53/3,44/1,65% → 0,613/0,474/0,388% |
| §5.2.2 Susceptibilidade a harm. ordem elevada | 135–138 | Distúrbio de tensão 3% → harmônico de corrente 7,02% sem compensação, 2,92% com ressonante |
| Apêndice D — Injeção Interharmônica | 189–193 | 90 Hz interharmônico → potência oscilante em 30 Hz → ripple no VCC e em id/iq |

**Arquivos .txt em ~/pdfext/ (2026-07-28):**
`FIX_teseagp_Revisao_Ressonancia_Problema.txt`,
`FIX_teseagp_Revisao_Ressonantes_Mitigacao.txt`,
`FIX_teseagp_Harm_Susceptibility_LCL.txt`,
`FIX_teseagp_Interharmonic_Consequences.txt`

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

| §7.3 Limitation of current distortion | 144–147 | Table 17/18 (limites % de harmônico ímpar/par por ordem), TRD 5%, background TDD→TRD, exclui distorção pré-existente da Area EPS (§7.3.1) |

**Arquivos .txt gerados em ~/pdfext/ (2026-07-25):**
- `ieee1547_53_54_voltvar.txt`, `ieee1547_62_faults.txt`,
  `ieee1547_64_voltage.txt`, `ieee1547_annexC_ridethrough.txt`,
  `ieee1547_annexI_casestudies.txt`
- `ieee1547_73_power_quality.txt` (p.138–149, gerado 2026-07-29)

Sintetizado em `.claude/kb/standards/ieee1547_ride_through.md`,
`.claude/kb/standards/ieee1547_case_studies.md` e (§7.3) em
`.claude/kb/standards/harmonic_significance_criteria.md`.

## Hu, Meng, Bu, Ren — *Test and Analysis of LVRT Characteristic of Wind Farm* (6 p.)

Artigo curto (IJAPE Vol.2 Issue 4, 2013), sem outline — extraído por inteiro em
`~/pdfext/lvrt_windfarm_full.txt` (2026-07-25). Teste de campo real em turbina
PMSG 850 kW, norma chinesa Q/GDW392-2009. Conteúdo: fórmula de corrente reativa
dinâmica, dados de teste simétrico vs. assimétrico (desequilíbrio de corrente
entre fases). Sintetizado em
`.claude/kb/standards/china_lvrt_windfarm_test.md`.
