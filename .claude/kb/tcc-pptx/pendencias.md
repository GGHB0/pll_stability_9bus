---
name: defesa-pendencias
description: Pendências do deck da defesa — divergências com o TCC, tempo de fala, decisões de conteúdo em aberto
aliases: [defesa-pendencias]
---

# Deck da defesa — pendências

> Levantadas na primeira leitura do esboço (2026-10-16). Mapa dos slides em
> [[defesa-deck-map]]; divergência de número se resolve pelo TCC canônico
> ([[tcc-pendencias]] guarda as do próprio TCC). Entregas em
> [[defesa-historico-entregas]].

## Em aberto

- **Exceção de método no slide 6 (2026-10-24, aprovada pelo Victor)**: o
  TCC só tem a Eq. (3.5); o slide ganhou dois desenhos conceituais sem número
  ao lado dela (eixos abc + dq girante com o vetor v projetado em v_d e v_q;
  senoides abc → Park → v_d e v_q constantes). Rótulos das senoides ficaram
  perto de 11 pt: conferir no projetor.
- **Slide 12 (inversor) dividido em três (2026-10-20; 12a e 12b entregues como slides 12 e 13, 12c pendente)**: 12a
  "Referência de corrente" (2ª prévia: diagrama de blocos da 1ª versão no
  PSIM, `assets/diagrams/referencia_corrente_psim.svg`, Pref 1 pu e Qref = 0
  ÷ vd do SRF-PLL, malha e PWM tracejados; embaixo a Eq. 3.9 invertida e
  "Por que o PLL importa aqui?". A 1ª prévia, só com a conta, foi recusada:
  o Victor quer mostrar como foi feito, não só a equação; 2ª prévia
  **aprovada** em 2026-10-20; **exceção aprovada** pelo Victor: "t = 35 ms" discreto sob o degrau
  do diagrama e na fala, único número fora do TCC no slide), 12b
  "Controle de corrente" (diagrama da malha dq, PWM 5 kHz, LCL, PI com
  ξ 0,707 e ωn = 4√2·fg → Kp = 8·fg·Lest, Ki = 32·fg²·Lest; sem Kp/Ki
  numéricos; Fig. 4.2 sai; 1ª prévia em 2026-10-20: Fig. 3.1 do TCC à
  esquerda, 3 cartões PWM/LCL/PI à direita, "Por que dois PIs?" embaixo;
  feito sobre o slide 12 antigo; entregue; **equações do PI a revisar**,
  o Victor não gostou da forma atual), 12c "Suporte de reativos do ONS" (Fig. 2.2 +
  como aplicamos: iq pela curva, saturado em Imax, id = min(id,nom,
  √(Imax² − iq²))). A fórmula do 12c é **exceção de método** (não está no
  TCC; inclinações do código fora). Ordem = trabalho real: PSIM com
  referência fixa ([[psim-netlists]]) → malha de corrente → ONS. Staging e
  script em `C:\Temp\defesa_inversor\gen_inversor.py` (um grupo `g_12a`,
  `g_12b`, `g_12c` por slide). Com o 12c, os slides seguintes descem mais 1.
  **TCC se contradiz**: §3.1.4 diz que não há desacoplamento, §3.5 diz que
  há; o 12b não afirma nenhum dos dois, e a explicação vai para o material
  de perguntas.
  **12c virou três slides (2026-10-21, staging `C:\Temp\defesa_ons\gen_ons.py`,
  entregue como slides 14-17, com o "Sistema completo" da Fig. 4.2 no fim)**: 12c "Referência pelo ONS" (`referencia_corrente_ons.svg`,
  bloco do Submódulo 2.10 no esqueleto do slide 12, encaixe da Fig. 4.2;
  aprovado), 12d "Dentro do Submódulo 2.10" (`ons_logica_defesa.svg`: rampa +
  círculo de raio I_max; **aprovado, "não tirar"**; a 1ª versão em caixas foi
  recusada por pouco clara) e 12e "Lógica em blocos" (`ons_fluxo_defesa.svg`,
  fluxograma do código, para o Victor explicar a lógica). Rampa
  (0,85 − V)/0,35 é do TCC (§5.2); a prioridade/círculo é exceção de método.
  Equações do 12c e do 13 a revisar juntas. Deck 26 → 30, fala 29,9 min:
  **rodada de tempo pendente** (slides 5, 6, 7, 9 sem fala; 10 com 384 palavras).

- **Passada de texto em 20-22 (pendente, 2026-10-21)**: layout e frase de
  abertura entregues sem mexer no corpo, a pedido do Victor. Ainda na tela:
  travessão nos 3 cartões do 20, "BAD_PLL" no cartão 2 do 20, a sigla de transitórios eletromagnéticos na
  legenda do 20 e nos limites do 22 (esta saiu em 2026-10-25). Só quando o Victor pedir.

- **Reestruturação da MODELAGEM (decidida em 2026-10-18, Alternativa 1)**:
  5 slides na ordem do trabalho real (dq → 9 barras/Thévenin → bancada do
  PLL entre duas fontes ideais → ganhos → inversor em etapas PWM/LCL/100 MW),
  deck 25 → 26. Exceção à regra abaixo **só para o método** (bancada e
  sequência de montagem, de [[psim-modeling]]); nenhum número fora do TCC
  na tela (R_th, L_th, Vdc e m ficam para a arguição). **Tela entregue em
  2026-10-18.** Depois, no mesmo dia, o slide 5 foi dividido em dois (deck
  26 → 27): 5 = transformada de Park (equação 3.5, gancho "E o ângulo θ?"),
  6 = Fig. 4.3 com os blocos PD, PI e VCO. À noite entrou um slide 5 novo
  (deck 27 → 28): a usina fotovoltaica como inversor seguidor de rede
  (Fig. 3.2), que abre a MODELAGEM e resume o que vem; Park passou a 6.
  Pendente: **falas dos slides 5-12** (5, 6, 7 e 9 têm só o marcador
  "[Victor] Fala a escrever"; 8 e 12 ainda têm as antigas; 10 e 11 novas; no 5, o
  gancho para a substituição da máquina da Barra 2 no IEEE 9 barras, que
  aparece no 8). Itens que saíram da tela e devem ir para a fala:
  compromisso de banda do PI (slide 7), Rd1/Rd2/Rd3
  (slide 12), PI de corrente com ξ 0,707 e ωn = 4√2·fg (antiga fala do 6).

- **Exceções aprovadas no slide 13 (2026-10-19)**: (1) 0,1 s de
  inicialização (PLL trava, fora das métricas: `T_SETTLE` do pipeline), só
  no MÉTODO, nunca na MODELAGEM; (2) a matriz segue o simulado, não a
  Tabela 4.1 desatualizada (+ "I" na monofásica B7; bifásica L8-9 reprovada
  fica fora). Opcional do validador: o regime "N e I" da legenda se apoia no
  §5.1, não no Cap. 4.
- **Exceção aprovada no slide 2 (2026-10-21)**: Gráfico de barras da evolução de capacidade instalada de renováveis variáveis no SIN (2020 a 2025: 25,5 GW para 96,8 GW, +279% vs +24% da carga média nacional de 69,2 para 85,8 GWmed) da apresentação oficial do ONS ao Senado Federal (15/10/2025). Conecta a motivação da tese diretamente ao sistema elétrico brasileiro e aos desafios operacionais de conversores no SIN.

- **Sem a sigla de transitórios eletromagnéticos (Victor, 2026-10-19; ampliado em 2026-10-25)**: o Oscar não
  gostou da sigla. Saiu do deck (tela e notas), do TCC canônico (Resumo,
  Abstract, objetivo da §1, Cap. 6) e de todo o repositório em 2026-10-25. Na
  tela e na fala: "simulação" / "simulação computacional".
- **Slide 14 = fluxo da análise (Victor, 2026-10-20)**: Simulink → CSV →
  Python → painel HTML, não as ferramentas da modelagem (Python/PSIM/Simulink
  da §4.2; essa leitura foi entregue e revertida). Entregue no mesmo dia
  (tabela de métricas, rodapé-ponte B). Próximo passo do Victor: o **gancho
  para os resultados** (slides 15 em diante).
- **Regra (2026-10-17)**: o deck traz só o que está no TCC entregue
  (VFinal), com o mesmo valor; nada de ressalva na fala. A partida "até
  0,1 s" saiu do slide 10 por isso.
- **Inconsistências do próprio TCC entregue** (o deck evita os dois lados):
  Tabela 4.1 diz 28 cenários (21 + 7), mas a Tabela 5.3 já usa a
  monofásica na Barra 7 inadequada (29 = 21 + 8); a introdução traz
  22.547 MW (31%) e a §2.4.3, 23.368 MW (34,5%), que é o número do deck.
- **Demo (slide 16)**: ~~cartão mostra "V residual médio B2", não a
  retenção~~ resolvido em 2026-10-20: o painel ganhou os indicadores do Cap. 5
  com as receitas do TCC (retenção 9,2% / 8,2%, retorno 98 ms / "não
  retorna", 66,8%, 0,72 pu), ver [[indicadores-tcc-dashboard]]. Os cards
  podem ser lidos. Conferir se as notas do slide 16 querem citar o card.
- **Notas do slide 16 × aba "Análise TCC" (2026-10-20)**: desde 2026-10-25
  a aba não existe mais; o painel abre no **Resumo** e os 8 capítulos ficam
  só no botão "Modo apresentação" (passador avança)
  ([[roteiro-demonstracao-dashboard]]). As notas do slide da demo têm de
  dizer isso. Falta reescrever as notas pelos
  capítulos e decidir o tempo: a aba pede 3 a 4 min, então ou os slides
  17-18 viram síntese rápida, ou capítulos saem (`CAPITULOS` em
  `src/report/roteiro.py`).
- **Ensaiar a demo (slide 16) no notebook da defesa, sem internet**: abrir
  `output/pll_metrics.html` antes, no cenário Barra 7 trifásica nominal;
  conferir os nomes dos botões citados nas notas (Zoom na falta, aba
  Espectro FFT em dq; agora o botão "Modo apresentação"). O cabeçalho já
  diz "UERJ 2026" (corrigido em 2026-10-20).
- **Crédito do template (CC BY 4.0)**: o visual vem do "Project
  Portfolio" do SlidesCarnival; falta a linha de crédito (sugestão: discreta
  no último slide do apêndice). Decisão do Victor.
- **Cosmético (slide-validator)**: ~1 in vazio no pé da capa; faixa de ~0,8 in
  vazia no pé do slide 11 (duas sintonias).
- A capa troca de figuras do TCC para fotos de usinas (2026-10-16); o
  crédito CC BY acima vale só para o template, não para as fotos (Pexels).
- **6. Fontes**: Arial (título) + Calibri (corpo) do tema, sem mudança no
  deck. Conferir no notebook da defesa e levar o PDF de reserva.
- **Figuras dedicadas do apêndice** (caso `figura_dedicada.md` da skill):
  5.14 (slide 23), 5.5/5.6 (slide 24), 5.20/5.21 (slide 27). Corpo (15, 17,
  18) entregue em 2026-10-18.
- **Opcionais do slide-validator (figuras dedicadas, 2026-10-18)**: slide 18
  com moldura direita até x 12,30 (não 12,95) e ticks ~10,5 pt nas 5.10/5.18;
  faixa cinza do 1º ciclo sem legenda nas 5.7/5.18 (explicar na fala, está
  no texto da Fig. 5.7); rótulo "falta" encosta na curva no painel Barra 7;
  cartão "250×" do slide 18, onde o TCC diz "mais de 250 vezes"; título do
  cartão "Sintonia nominal" do slide 15 em roxo (design: azul = nominal).
- **Opcional (slide 5, slide-validator)**: o redesenho da Fig. 3.2 usa
  rótulos em minúscula ("Fonte primária"), o TCC em maiúscula ("Fonte
  Primária"); o cartão "Seguidor de rede" é paráfrase do §4.1, sem número novo.
- Resolvido em 2026-10-19: título do slide 5 encurtado ("Fonte renovável")
  com a frase de abertura (opção C de 4, a pedido do Victor); mesmo padrão
  nos slides 6 a 11 (o 10 virou dois: sintonia e duas sintonias, deck 28 → 29);
  revisão slide a slide segue no 12 (inversor). Opcional (slide-validator,
  slide 9): rótulos v_abc, v_q e ω_PLL da figura da bancada pequenos no projetor.
- Resolvido em 2026-10-18 (noite): Fig. 4.3 redesenhada para o slide 6 a pedido do Victor (exceção à regra de diagrama idêntico ao TCC), equações num cartão à direita.
- Resolvido em 2026-10-18 (fim de tarde): equação do slide 5 na largura toda
  com cartões embaixo; Fig. 4.3 de 5,5 para 6,2 in; subscritos reais
  (baseline -25000) em v_q, v_d, ω_PLL, ω_0, θ_PLL nos cartões do slide 6.

## Resolvidas em 2026-10-16 (entregues na rodada da noite)

1. Monofásica na Barra 7 com sintonia inadequada: slide 10 "com as duas
   sintonias"; linha nova nas tabelas dos slides 18 e 21 (Tabela 5.3 do TCC:
   0,64 / 0,55 / 70,6° / 95 ms; ver [[cenarios-simulados]]); notas 10, 18, 21.
2. Contagem: 29 cenários, 21 nominais e 8 inadequados.
3. Roteiro: 30,9 → 24,6 min (3.195 palavras), Bruno 47% / Victor 53%; só
   repetição cortada, explicações úteis à banca devolvidas pelo validador.
4. "BAD_PLL" fora da tela (slide 8) e da fala.
5. Rótulo "Justificativa de ouro:" removido das 11 caixas; a pergunta
   ficou em `accent1`.

Achados extras, também resolvidos:

- 4 figuras velhas trocadas pelas de `assets/charts/` (slides 12, 13 e 18:
  legenda "salto de fase" e par da monofásica; slide 22: escala antiga de
  P/Q, 0,87 pu antes da falta).
- Slide 14: Q 0,14 pu (escala legada ×1,5) → 0,09 pu, como no TCC.
