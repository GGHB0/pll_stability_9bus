---
name: tcc-revisao-fragmento-cap4
description: Revisão colaborativa do fragmento externo capitulos_4_5_revisados.docx — decisões de terminologia para a seção 4.3.3.3, ainda não mesclado no canônico
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

Rascunho em andamento (ainda **não aprovado** pelo usuário): parágrafo dos
cinco grupos de sinais monitorados + explicação das duas taxas de amostragem
(Ts = 5 µs / Tsc = 200 µs + interpolação). Nessa passada, removido "logsout"
(nome interno do objeto de registro do Simulink) do texto — mesmo tipo de
vazamento de artefato de código já corrigido no `app.py` (ver
`feedback_docx_no_code_artifacts` na memória); o bloco 643 do **canônico**
ainda cita "logsout" e deveria ser corrigido lá também — fora do escopo desta
revisão pontual, só sinalizado aqui.

## Verificação de conteúdo (não só vocabulário)

Confirmado contra `src/pipeline/loader.py:159-171`: os sinais de geradores
síncronos (`has_gen1`/`has_gen3`, ângulo do rotor + potência ativa de G1/G3)
existem de fato no pipeline, então a descrição do grupo "Geradores síncronos"
do canônico (bloco 648) é factualmente sólida — só precisava do mesmo
polimento de vocabulário, não de correção de conteúdo.

## Próximos passos

- Fechar o rascunho do restante do §4.3.3 (cinco grupos de sinais +
  amostragem) com o usuário.
- Só depois: revisar Cap. 5 do fragmento contra o canônico.
- Mesclagem no canônico é etapa posterior, ainda não decidida.
