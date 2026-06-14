---
name: tcc-full-cap4
description: Conteúdo completo do Capítulo 4 — Análise e Discussão de Resultados (quase vazio — só títulos), Conclusão (placeholder) e Referências finais do documento
metadata:
  type: project
---

# TCC — Capítulo 4: Análise e Discussão de Resultados (texto completo)

> ⬜ **PRIORIDADE:** Este capítulo está quase vazio. Só os títulos e um parágrafo introdutório existem.
> Subseções a redigir: 4.1.1, 4.1.2, 4.2.1, 4.3.1, 4.3.2.
> **4.2.2 NÃO implementar** — instrução do orientador Oscar.

## Introdução do Capítulo 4 *(✅ redigida)*

Este capítulo apresenta a análise e a discussão dos resultados obtidos a partir das simulações de transitórios eletromagnéticos (EMT) realizadas nos ambientes PSIM e MATLAB/Simulink, conforme a metodologia descrita no Capítulo 3. O objetivo central desta etapa consiste em avaliar, de forma quantitativa e crítica, o desempenho dinâmico do algoritmo de sincronismo SRF-PLL, bem como identificar seus limites de robustez quando aplicado a um Inversor Conectado à Rede (ICR) submetido a diferentes contingências do sistema elétrico.

A análise concentra-se tanto na resposta interna do PLL, quanto nos impactos sistêmicos observados na injeção de potência ativa e reativa pelo inversor. Dessa forma, busca-se estabelecer uma relação direta entre a estabilidade do sincronismo e a qualidade da energia fornecida à rede, aspecto fundamental para o atendimento aos requisitos dos códigos de rede modernos.

## 4.1. Desempenho do SRF-PLL sob Afundamentos de Tensão Simétricos

A análise inicia-se pela avaliação do desempenho do SRF-PLL sob afundamentos de tensão simétricos, tipicamente associados a faltas trifásicas distantes. Esse cenário representa a condição de menor complexidade para o algoritmo, uma vez que a tensão da rede sofre apenas redução de magnitude, sem a introdução de componentes de sequência negativa ou desequilíbrios angulares entre fases.

### 4.1.1. Resposta Dinâmica e Tempo de Acomodação *(✏️ contém apenas ".")*

.

### 4.1.2. Impacto na Injeção de Potência Ativa e Reativa *(⬜ vazio)*

## 4.2. Limites de Robustez sob Contingências Assimétricas e Saltos de Fase

### 4.2.1. Instabilidade sob Faltas Assimétricas *(⬜ vazio)*

### 4.2.2. Impacto do Salto de Fase (Phase-Angle Jump) *(⬜ vazio — NÃO implementar)*

## 4.3. Análise de Sensibilidade e Diretrizes de Projeto

Esta seção discute a influência dos parâmetros de projeto do PLL na sua robustez, validando a análise de sensibilidade proposta na metodologia.

### 4.3.1. Influência dos Ganhos do Controlador PI do PLL *(⬜ vazio)*

### 4.3.2. Conformidade com o Código de Rede (LVRT) *(⬜ vazio)*

---

# Conclusão *(⬜ placeholder — não redigida)*

A facilidade de disseminação do conhecimento, potencializada pelas redes de comunicação, é um fator que tem impulsionado diferentes instituições governamentais.... *(texto do template UERJ — substituir)*

---

# Referências Finais do Documento

> ⚠️ Esta seção mistura referências reais do TCC com o template de exemplo da UERJ.
> As referências reais (citadas no texto) são as listadas em `full_intro.md` [1]–[9].
> O restante abaixo é template da UERJ e deve ser removido.

## Referências reais usadas no TCC

BOLLEN, M. H. J. Understanding Power Quality Problems: Voltage Sags and Interruptions. IEEE Press, 2000.

YAZDANI, A.; IRAVANI, R. Voltage-Sourced Converters in Power Systems: Modeling, Control, and Applications. John Wiley & Sons, 2010.

TEODORESCU, R.; LISERRE, M.; RODRIGUEZ, P. Grid Converters for Photovoltaic and Wind Power Systems. John Wiley & Sons, 2011.

IEEE Standard for Interconnection and Interoperability of Distributed Energy Resources with Associated Electric Power Systems Interfaces (2018). IEEE Std 1547-2018.

*(Nota no documento: "Referências a serem usados nos textos até o momento")*

## Template UERJ (a remover — P3 em docx_structure.md)

As entradas abaixo pertencem ao template de formatação da UERJ e não são referências do TCC:

- GOMES, L. G. F. F. Novela e sociedade no Brasil. Niterói: EdUFF, 1998.
- ROMANO, Giovanni. Imagens da juventude na era moderna. In: LEVI, G.; SCHMIDT, J. (Org.). História dos jovens 2. São Paulo: Companhia das Letras, 1996. p. 7-16.
- REVISTA BRASILEIRA DE GEOGRAFIA. Rio de Janeiro: IBGE, 1939-
- NAVES, P. Lagos andinos dão banho de beleza. Folha de S. Paulo, São Paulo, 28 jun. 1999.
- KOBAYASHI, K. Doença dos xavantes. 1980. 1 fotografia, color., 16 cm x 56 cm.
- *(e demais entradas do template — todas a remover)*

---

# Achados da Revisão (2026-06) para o Cap. 4

Com base em simulações realizadas:

- **H > 0,1 s** nas máquinas síncronas G1/G3 evitou colapso total do sistema; abaixo/próximo desse valor, o sistema entra em região crítica
- O colapso observado ocorre na **recuperação pós-contingência**: o PLL tenta retornar, acumula erro, oscila em loop e deixa de fornecer uma referência angular útil
- `Id` e `Iq` deixam de seguir trajetória coerente quando `theta_hat` se perde
- Tentativas de notch/filtro para remover componentes de 120 Hz não resolveram os casos severos; seguem relevantes para curtos assimétricos moderados, mas não substituem uma solução estrutural para baixa inércia e lock-loss
- Varredura com H das máquinas e reatância de curto entre 2% e 20% de 529 ohms
