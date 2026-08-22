---
name: tcc-revisao-fragmento-cap4
description: Revisão colaborativa do fragmento externo capitulos_4_5_revisados.docx — Cap.4 fechado (terminologia do dashboard, ganhos do PLL, filtro LCL, tempos de falta), ainda não mesclado no canônico
metadata:
  type: project
---

# Revisão do Fragmento Externo (Cap. 4 e 5)

## Contexto

O usuário compartilhou `capitulos_4_5_revisados.docx` (Downloads), uma versão
revisada dos capítulos 4 e 5, distinta do canônico
(`TCC_Victor_Bruno_V9_novo_indice_2.docx`, ver `docx_structure.md`/
`content_map.md`). Esse fragmento vai eventualmente substituir/atualizar o
conteúdo desses capítulos no arquivo canônico, mas por ora a edição fica
isolada nele — nada foi mesclado no canônico ainda.

Ordem de trabalho definida pelo usuário: fechar o Cap. 4 primeiro; o Cap. 5
(que tem divergências estruturais maiores em relação ao canônico — ver
abaixo) fica para depois.

## Divergências estruturais observadas (fragmento vs. canônico)

- Cap. 4: perde as subseções de modelagem de geradores e topologia de falta
  como itens dedicados (presentes no canônico como 4.3.3.1/4.3.3.2, ver
  `content_map.md`).
- Cap. 5: adiciona uma seção nova de validação em regime permanente (nominal
  vs. sintonia inadequada, sem falta) e perde a seção dedicada de impacto dos
  ganhos do PLL (5.3 no canônico) — a reconciliar quando chegarmos no Cap. 5.

## Decisões de terminologia — §4.3.3 (equivalente ao 4.3.3.3 canônico)

Parágrafo original do fragmento descrevia a visualização de resultados como
"interface interativa desenvolvida em ambiente web"/"plataforma" — impreciso:
o artefato real é um relatório HTML único gerado localmente (Plotly via CDN,
não uma aplicação web hospedada). Ver `src/report/renderer.py:155`.

Termos fixados após 3 rodadas de calibração de registro:

- "ambiente web"/"plataforma" → **"painel interativo (*dashboard*)"**
  (convenção do projeto: termo estrangeiro em itálico na primeira ocorrência,
  como já feito com *cycle slipping*, *grid-following*)
- "arquivos de dados tabulares" (formal demais) → **"arquivos CSV"**
- "responsável por homogeneizar as bases temporais" → **"compatibiliza as
  bases de tempo"**
- "Trata-se de um arquivo único, aberto diretamente no navegador" → cortado;
  substituído pela ideia de **dashboard consolidado**
- "comparação lado a lado" (dos gráficos) → **"visualização lado a lado"** (a
  comparação quantitativa é da tabela; o gráfico só permite leitura visual)

**Decisão final (2026-08-22): manter compacto.** O fragmento usa um único
parágrafo para as grandezas monitoradas (diferente da granularidade do
canônico, que separa em 5 grupos + parágrafo de amostragem/interpolação).
O usuário optou por só polir esse parágrafo único em vez de expandir para a
estrutura do canônico. Texto final aplicado (parágrafo do fragmento
equivalente ao 26): troca "componente em quadratura da tensão" por "erro de
fase em relação à referência da rede" (é essa grandeza, não Vq isolado, que
alimenta as métricas IAE/ISE/ts) e especifica "do inversor" nas
tensões/correntes trifásicas (o original era ambíguo sobre o lado medido).

Removido "logsout" (nome interno do objeto de registro do Simulink) da
reescrita — mesmo tipo de vazamento de artefato de código já corrigido no
`app.py` (ver `feedback_docx_no_code_artifacts` na memória); o bloco 643 do
**canônico** ainda cita "logsout" e deveria ser corrigido lá também — fora do
escopo desta revisão pontual, só sinalizado aqui.

## Verificação de conteúdo (não só vocabulário)

Confirmado contra `src/pipeline/loader.py:159-171`: os sinais de geradores
síncronos (`has_gen1`/`has_gen3`, ângulo do rotor + potência ativa de G1/G3)
existem de fato no pipeline, então a descrição do grupo "Geradores síncronos"
do canônico (bloco 648) é factualmente sólida — só precisava do mesmo
polimento de vocabulário, não de correção de conteúdo. (Não relevante para o
fragmento, que decidiu não tratar geradores no Cap.4 — ver abaixo.)

## Revisão do restante do Cap. 4 (2026-08-22)

Após fechar o §4.3.3, revisão do resto do capítulo (§4.1, 4.2, 4.3.1, 4.3.2,
4.3.4, 4.4) identificou dois tipos de problema:

**Grupo A — linguagem de certeza absoluta** (mesma regra já aplicada ao
canônico no passe de estilo de 2026-08-05, ver `historico_entregas.md`):
"garantindo"/"garantiu"/"assegurar" neutralizados em 3 parágrafos (§4.1,
§4.3.2, §4.3.2.2). Também adicionado itálico em "cycle slipping" (§4.3.3),
que tinha ficado sem a marcação de estrangeirismo.

**Grupo B — lacunas de conteúdo vs. canônico**, decididas item a item pelo
usuário:

1. **Geradores síncronos G1/G3 (H1, H3)** — **descartado**: "não é o foco do
   trabalho". O fragmento não vai tratar dinâmica de geradores no Cap.4,
   diferente do canônico (4.3.3.1). Divergência estrutural aceita
   definitivamente, não é mais pendência.
2. **Ganhos numéricos do PLL** — **incluído** em §4.3.2.2: `Kp,PLL = 460` /
   `Ki,PLL = 105 820` (ωn = 325,3 rad/s, ξ = 0,707, ts = 20 ms) no nominal;
   redução de 80% (`Kp,PLL = 92` / `Ki,PLL = 21 164`, ωn = 145,5 rad/s,
   ξ = 0,316) na sintonia inadequada. Valores conferem com
   `content_map.md` (Cap.4/§4.3.3 canônico) e a memória `project_bad_pll`.
3. **Tempos de falta** — **incluído** em §4.3.4: duração 0,1 s (6 ciclos) em
   ambos os cenários; nominal aplicada 0,3-0,4 s com janela até 0,6 s;
   sintonia inadequada aplicada 0,6-0,7 s com janela até 1,0 s. Confere com
   `pendencias.md` item 17 e `kb/simulation/cenarios_simulados.md`.
4. **Parâmetros do filtro LCL** — **incluído** em §4.3.2.1: ωres =
   9068,99 rad/s, ξ = 0,707, Lest (L1+L2) = 30,71 mH, resistências de
   amortecimento Rd1 = 0,5734 Ω / Rd2 = 0,0054 Ω / Rd3 = 3,1228 Ω. Valores
   vêm de `kb/inverter/lcl_filter.md` e do bloco 624 do canônico (extraído em
   `canon_4_3_3.txt`) — não usados os valores de referência da TeseAGP
   (220V/5kVA, sistema de escala diferente).
5. **Separar §4.3.2.2 em corrente e PLL** (como o canônico faz em 4.3.2.2 /
   4.3.2.3) — **feito**, após comparativo aprovado pelo usuário. Novo título
   "4.3.2.2 Sintonia do Controle de Corrente" (renomeado, tirado "e do
   SRF-PLL") seguido de "4.3.2.3 Modelagem do Sistema de Sincronismo
   (SRF-PLL)" (título novo, inserido antes do parágrafo com Kp,PLL/Ki,PLL).
   Texto dos dois parágrafos não mudou, só a quebra de seção. Documento
   passou de 76 para 77 parágrafos.

## Próximos passos

- Cap. 4 do fragmento está fechado (grupos A e B completos).
- Próximo: revisar Cap. 5 do fragmento contra o canônico.
- Mesclagem no canônico é etapa posterior, ainda não decidida.
