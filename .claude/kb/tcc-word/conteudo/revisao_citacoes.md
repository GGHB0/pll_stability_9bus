---
name: tcc-revisao-citacoes
description: Revisão de fidelidade das citações do TCC V10 (item 26): cada trecho × página da fonte × veredito
aliases: [tcc-revisao-citacoes]
source: Wu e Wang 2020 p.1-3; Xiong et al. 2025 p.1; Strauss-Mincu et al. 2026 p.95, 97, 101, 106; Teodorescu et al. 2011 §8.3 p.182-186; Mohan 2003 §17-4 p.475-477; IEA GER2026 p.12
references:
  - "WU, H.; WANG, X. Design-Oriented Transient Stability Analysis of PLL-Synchronized Voltage-Source Converters. IEEE Transactions on Power Electronics, v. 35, n. 4, p. 3573-3589, abr. 2020. DOI 10.1109/TPEL.2019.2937942."
  - "XIONG, Y. et al. Comparison of Power Swing Characteristics and Efficacy Analysis of Impedance-based Detections in Synchronous Generators and Grid-following Systems. IEEE Transactions on Power Systems, v. 40, n. 3, p. 2545-2556, maio 2025. DOI 10.1109/TPWRS.2024.3469235."
  - "STRAUSS-MINCU, D. et al. Inverter-Dominated Future Power Systems: A Roadmap for System Stability. IEEE Power and Energy Magazine, v. 24, p. 93-107, 2026. DOI 10.1109/MPE.2025.3617895."
  - "TEODORESCU, R.; LISERRE, M.; RODRIGUEZ, P. Grid Converters for Photovoltaic and Wind Power Systems. Chichester: John Wiley & Sons, 2011."
  - "MOHAN, N. Power Electronics: Converters, Applications, and Design. 3. ed. Hoboken: John Wiley & Sons, 2003."
  - "INTERNATIONAL ENERGY AGENCY (IEA). Global Energy Review 2026. Paris: IEA, 2026."
---

# Revisão das citações do TCC (V10)

Item 26 de [[tcc-pendencias]]. Pergunta de cada linha: **a página citada
sustenta o que a frase afirma?** Levantamento feito em 2026-09-27 sobre o V10
entregue (MD5 `66a817de…`): 65 citações no corpo, 20 entradas na lista.
Blocos = índice de parágrafo do `document.xml` naquela versão (mudam a cada
edição; localizar pelo trecho).

Vereditos: **OK** · **FRASE** (ajustar o texto à fonte) · **FONTE** (trocar a
fonte) · **SEM PDF** (não dá para conferir).

## Consistência texto × lista (mecânico)

- Citadas sem entrada na lista: IEA (2026), KUNDUR et al. (2004), GU; GREEN
  (2023), COORDINADOR ELÉCTRICO NACIONAL (2025) — é o item 15 de
  [[tcc-pendencias]].
- Na lista sem citação: ANDERSON; FOUAD (2003), IEEE 1547-2018.
- Entrada incompleta: ESCOBAR et al. (2021), sem volume, páginas nem DOI.
- MATLAB/Simulink e PSIM sem referência no §4.2 (item 7).

## Alto risco (conferido em 2026-09-27)

| Bloco | Trecho (resumo) | Fonte citada | O que a fonte diz | Veredito |
|---|---|---|---|---|
| 250 | flutuação da geração e falta de armazenamento comprometem a confiabilidade | MOHAN (2003) | §17-4 (p. 475-477) só descreve a interface eletrônica de PV, eólica e armazenamento; nada sobre intermitência ou confiabilidade | FONTE: IEA (2026) p. 12 fala da necessidade de flexibilidade e capacidade despachável com mais renováveis variáveis |
| 251 | máquinas síncronas conferem estabilidade pela inércia física | XIONG et al. (2025) | p. 1: oscilação do SG é regida pelo ângulo físico; a do GFL, pelo controle. Não fala em inércia. Wu e Wang p. 1 (abstract e intro): ao contrário do SG, falta ao VSC lei física que governe o sincronismo; a dinâmica depende do controle | FRASE: trocar "inércia física" por "leis físicas"; citar os dois |
| 256 | IBRs carecem de inércia, menor resposta inercial | WU; WANG (2020) | nenhuma ocorrência de "inertia" no artigo | FONTE: STRAUSS-MINCU et al. (2026) p. 95 ("As system inertia decreases…") e p. 97 (inércia vem das máquinas síncronas) |
| 258 | sequência negativa gera 2ω em vq e impede a convergência, levando à perda de sincronismo | WU; WANG (2020) | §V-D: falta assimétrica só para dizer que se usa pré-filtro. Teodorescu §8.3 (p. 182-186): sequência negativa gera oscilação em 2ω no dq e na fase detectada. Wu e Wang: perda de sincronismo em faltas severas (abstract) | FRASE + FONTE: 2ω → Teodorescu; perda de sincronismo → Wu e Wang |
| 392 | inércia menor faz os síncronos remanescentes terem desvios angulares mais rápidos | WU; WANG (2020); XIONG et al. (2025) | nenhum dos dois trata disso. Strauss-Mincu p. 106: inércia menor → RoCoF maior; p. 101: requisitos de estabilidade transitória precisam ser reavaliados com a dominância de inversores | FRASE + FONTE: reescrever para o que o Roadmap diz |

Já conferidos antes: bloco 259, "redes fracas" (WU; WANG, 2020), OK (p. 1 e
3); bloco 260, Motivação (XIONG et al., 2025), OK (p. 1, evento de 2023).

Consequência: sem o bloco 250, o MOHAN fica sem nenhuma citação no corpo
(sair da lista ou citar em outro ponto).

## Sem PDF na pasta Bibliografia

BOLLEN (2000) bl. 325 · KUNDUR (1994) bl. 326 · OGATA (2009) bl. 443, 462 ·
RODRIGUEZ et al. (2007) bl. 408, 610 · SHADOUL et al. (2022) bl. 249 ·
ESCOBAR et al. (2021) bl. 410 · KUNDUR et al. (2004) bl. 276-285 (o KB
descreve a classificação pelo Gu e Green). Decisão pendente com o Victor.

## Médio risco (a conferir)

Livros de uso amplo: YAZDANI; IRAVANI (10 usos), TEODORESCU et al. (11),
ALVES (2022) ×3, ALVES; DIAS; ROLIM (2020). Mais sensível: bloco 447, números
da sintonia do PLL (ts = 20 ms → KpPLL = 460) citando ALVES; DIAS; ROLIM e
Teodorescu; conferir contra [[pll-loop-filter-gains]].

## Baixo risco (a conferir contra o `source:` do KB)

Cap. 2 redigido em 2026-07-19 a partir de extrações com página: IEA, Gu e
Green, Strauss-Mincu, CIGRE, ENTSO-E, Coordinador, ONS (2022, 2023).

## Relacionados

- [[tcc-pendencias]] — itens 7, 12, 15 e 26
- [[tcc-historico-entregas]] — troca de "redes fracas" e comentário 16
