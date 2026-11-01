---
name: tcc-historico-entregas-2026-11-01
description: Entrega de 2026-11-01 (03h12): Figura 2.2 com a planta LCL da TeseAGP no lugar do RL, fonte com Alves (2022)
aliases: [tcc-historico-entregas-2026-11-01]
---

# TCC Word — Entrega de 2026-11-01 (03h12)

Continuação de [[tcc-historico-entregas]].

## Figura 2.2: planta LCL no lugar de 1/(Ls+R)

O bloco amarelo da malha de corrente dq era a planta RL de 1ª ordem
(L = L1+L2, R = R1+R2), que não é a do modelo: o filtro é LCL e a corrente
realimentada é iL2. Passou a ser 1/(s·L1·L2·C1) · 1/(s²+ωres²), eq. 3.49 da
TeseAGP (Alves, 2022), com o desenho em duas frações como na Fig. 3.23 da tese.
Rodapé da figura: ωres² = (L1+L2)/(L1·L2·C1) e "N(s): filtro notch". O resto
(PI Kp/4 + Ki/4s, notch, Vcc/2, eixos d e q, realimentação) ficou igual.

- `troca_imagem.py --rid rId16` (PNG 2340×1080, mesma largura de 6,30 in);
  fonte da figura: "Adaptado de Yazdani e Iravani (2010) e Alves (2022)"
  (Alves 2022 já estava nas referências). Cor vermelha da legenda e da fonte
  mantida como estava.
- `diff_texto` backup × canônico: 1 trecho (a linha da fonte); 0 comentários.
  Backup `_backups\VF\..._20261101_031249`; auditoria 0 falhas, 89 páginas.
- O OneDrive foi reorganizado: o canônico agora está em
  `Template Modelo TCC\01_TCC_Monografia_Final\` (config.py ajustado).

**Pendente, fora desta entrega:** o §3.3.2 (bloco 475) diz que há "termos de
desacoplamento" e que cada eixo vira "planta de primeira ordem". O modelo não
tem desacoplamento e a planta é LCL (ver [[agp-current-control-theory]],
[[simulink-model]]); a Seção 2.3.2 já diz isso certo. Decidir com o Victor.

## Promoção da versão do Victor e Equação (3.1) do ONS (16h39)

Promovido o backup mais recente do Victor (_20261101_042452, 897 parágrafos,
com todas as revisões de Rafael em azul, André em verde e Cleiton em vermelho)
para o arquivo canônico TCC_Victor_Bruno_VFinal.docx.

Formatação formal da restrição de corrente reativa do ONS (§3.3.2.1):
- A fórmula em pseudo-código id,ref = min(1.0, sqrt(Imax² - iq,ref²)) foi
  removida do texto corrido e convertida na Equação (3.1) em tabela sem
  bordas com OMML nativo: id,ref = min(1,0; sqrt(Imax² - iq,ref²)).
  Rótulo (3.1) e texto introdutório mantidos em vermelho (#FF0000, Prof. Cleiton).
- A teoria p-q de Akagi (§3.3.3) foi renumerada de (3.1) para (3.2)
  (menção no texto e rótulo na tabela), mantendo a cor azul (#0070C0, Prof. Rafael).
- audit_docx: 0 falhas, 0 avisos; diff_texto: 3 trechos (897 → 899 parágrafos).
  Backup datado em _backups\VF\TCC_Victor_Bruno_VFinal_backup_20261101_163920.docx.

## Aplicação dos Itens 1, 4 e 5 da Banca (16h54)

Atendendo às solicitações da banca e ajustes identificados:
- **Item 5 (Remissão cruzada no Cap. 4)**: Corrigida a remissão de 'Figuras 4.12 e 5.13' para 'Figuras 4.12 e 4.13'.
- **Item 4 (Harmonização da Seção 2.5 com Seção 2.3.2)**: Parágrafos 535 e 536 atualizados para refletir que os controladores PI possuem filtro notch e não desacoplamento ativo, tratando o acoplamento cruzado e a rede como perturbações e modelando a planta equivalente puramente indutiva para sintonia (em total alinhamento com a Figura 2.2 e [[agp-current-control-theory]]).
- **Item 1 (Escolha do SRF-PLL - Prof. Rafael, Comentário 4)**: Inserido parágrafo na Seção 2.4 justificando a opção pelo SRF-PLL sobre DSOGI-PLL e DDSRF-PLL (padrão comercial dominante em grid-following, menor demanda computacional e linha de base para contingências severas), formatado em azul (#0070C0), e incluída a sigla DSOGI-PLL na Lista de Siglas.
- **Validação**: audit_docx 0 falhas, 0 avisos; diff_texto com 4 trechos (899 -> 901 parágrafos). Backup em _backups\VF\TCC_Victor_Bruno_VFinal_backup_20261101_165411.docx.

## Registro do DOI Zenodo e Repositório GitHub (17h11)

- **DOI Oficial**: [10.5281/zenodo.23866787](https://doi.org/10.5281/zenodo.23866787).
- **Repositório Oficial**: https://github.com/GGHB0/pll_stability_9bus.
- **Seção 3.3.3**: Citação (OLIVEIRA; REZENDE, 2026) e remissão ao Apêndice A em azul (#0070C0).
- **Referências Bibliográficas**: Entrada formatada em ABNT com link oficial do GitHub e DOI permanente.
- **Apêndice A**: Atualizado o parágrafo final com o repositório e DOI.
- **CITATION.cff e README.md**: Metadados de citação atualizados e badge do DOI adicionado.
- **Auditoria**: audit_docx 0 falhas, 0 avisos; diff_texto com 3 trechos (901 parágrafos mantidos). Backup datado em _backups\VF\TCC_Victor_Bruno_VFinal_backup_20261101_171104.docx.

## Inserção de Componentes Simétricas (Figura 2.4) e Trabalhos Futuros (17h40)

- **Item 2 (Componentes Simétricas de Fortescue e Figura 2.4)**:
  - Inserido na Seção 2.4 texto formal definindo as componentes de Fortescue (sequência positiva girando a +ω0, sequência negativa girando a -ω0) e o mecanismo físico da velocidade relativa Δω = 2ω0 (120 Hz) sobre o referencial síncrono dq, que contamina a malha do SRF-PLL.
  - Inserida a **Figura 2.4 – Decomposição em componentes simétricas e projeção da oscilação de 120 Hz no referencial dq** (arte vetorial de 3 painéis: sequência positiva, negativa e projeção em dq; 3000x1260 px) com legenda e fonte, e registrada na Lista de Ilustrações.
  - Na Seção 4.3 (§4.3), amarrada a raia de 120 Hz da FFT da Figura 4.10 diretamente à Figura 2.4 e à fundamentação da Seção 2.4.
- **Item 3 (Trabalhos Futuros e Técnicas Avançadas)**:
  - Acrescentado ao §6.1 (Trabalhos Futuros) o compromisso operacional da injeção de correntes puramente simétricas diante de tensão desbalanceada, resultando em potências ativa e reativa oscilantes a 120 Hz que estressam o barramento CC.
- **Destaques**: Todas as adições destacadas em azul (#0070C0) para o Prof. Rafael.
- **Auditoria**: audit_docx 0 falhas, 0 avisos; diff_texto com 4 trechos (901 -> 906 parágrafos). Backup datado em _backups\VF\TCC_Victor_Bruno_VFinal_backup_20261101_174017.docx.
