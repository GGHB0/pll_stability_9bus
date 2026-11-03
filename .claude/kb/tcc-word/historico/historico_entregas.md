---
name: tcc-historico-entregas
description: Histórico de entregas do Claude ao TCC: subscritos, siglas, ABNT, Cap. 6-7, português, mais recente
aliases: [tcc-historico-entregas]
---

# TCC Word — Histórico de Entregas do Claude

> Extraído de `docx_structure.md` (2026-07-19) para respeitar o limite de
> 200 linhas. Padrões XML e registro de IDs continuam em `docx_structure.md`.
> Ordem: mais recente primeiro.

## 2026-11-03 (17h36) — Afiliação do Prof. Dr. Rafael Cavalcanti Neto na Folha de Aprovação (UFPE)

- Atualizada a afiliação institucional do examinador da banca Prof. Dr. Rafael Cavalcanti Neto na Folha de Aprovação (página 4) de `"Faculdade de Engenharia – UERJ"` para `"Universidade Federal de Pernambuco – UFPE"`.
- Atualizados também os scripts utilitários `gen_clean_folha.py`, `apply_folha_aprovacao_canonico.py` e `surgical_folha.py` em `scripts/tcc_banca/`.
- Processado via `word_finalize.ps1` (0 campos com erro, 92 páginas, 0 órfãs no `audit_pdf_whitespaces.py`, 0 erros no `audit_docx.py`).
- Entregue em `01_TCC_Monografia_Final` e `comentado` (DOCX MD5 `d0cd19421b41f0046ab4991655feb243`, PDF MD5 `5407addc52060791e330a571ef8d971d`, backup `_20261103_173615`).

## 2026-11-03 (14h25) — Revisão do Apêndice A (sem "módulos" / "alta definição") e itálico em *cycle slipping* / *notch*

- Reescritos os parágrafos e legendas do Apêndice A (`Figuras A.1` a `A.5`) descrevendo diretamente cada tela do painel interativo, sem chamar de "módulos", sem mencionar "alta definição (1920x1080)" e removendo o subtítulo órfão `"B. Sequência de Telas..."`.
- Aplicado itálico (`<w:i/>`) nas ocorrências restantes de *cycle slipping* (§4.3 `488D5DFE`, Apêndice A `69F1F49F` e legenda da `Figura A.4`) e *notch* (§2.5 `6158680C`), além de subscritos em $v_d$ e $i_q$ no Apêndice A.
- Entregue em `01_TCC_Monografia_Final` e `comentado` (DOCX MD5 `9933482ba0575d16034d9685c9f14f38`, PDF MD5 `31d4a084dd81fda430f44edb15600444`).

## 2026-11-03 (12h47) — Unificação canônica (Bruno + Victor) + Figura 2.2 sem /4 + §3.3.2.2 e Tabela 3.1

Partindo de `_backups\VF\TCC_Victor_Bruno_VFinal_backup_20261102_011844.docx` (`57ea8075`), que reúne todas as edições do Bruno (`01/11`) e do Victor (`02/11`, incluindo R3/Tabela 2.1 GFL × GFM):
- Limpeza de `"de transitórios eletromagnéticos"` no Resumo, Abstract e 2º objetivo específico.
- Figura 2.2 sem `/4` nos blocos PI (`current_control_dq_blocos.svg` / `.png` → `Kp + Ki/s`).
- §3.3.2.2 (vermelho `#FF0000`): texto explicativo do ajuste empírico por fator de 4 (Alves (2022); Yazdani e Iravani (2010)) e **Tabela 3.1** (parâmetros e ganhos já divididos por 4: Kp = 7,37 e Ki = 1768,9); tabela de cenários renumerada para **Tabela 3.2**.
- Entregue em `01_TCC_Monografia_Final` e `comentado` (DOCX MD5 `b46f89ae25dd39b0e88f3e822c78f6ae`, PDF MD5 `e8b843d93d798240be4e3ba8b8b7baf4`, backup `_20261103_124729`). Regra reforçada em `entrega.md`: sempre checar todos os backups mais recentes antes de editar ou entregar a versão final.

## 2026-11-02 (00h56) — Revisão depois das entregas do Bruno

Remissões "Figuras 4.5 e 5.6" → 4.6 e o 4.13 do Bruno com o número em azul;
sigla FFT na lista (verde, A3); MPPT por extenso no Cap. 3, "O elo CC..." (uso único,
vermelho); §2.5 reescrito pelo Bruno pintado de azul a partir de "associados".
R4: sem "padrão dominante na indústria" (sem fonte), apoiado na frase anterior
do §2.4 (TEODORESCU; LISERRE; RODRIGUEZ, 2011), siglas por extenso completas e
em itálico, sem "grid-following"/"baseline". R6b: subscritos reais (v⁺ → v com
sobrescrito, ω0, vd, vq, ωPLL, θPLL) e a mesma citação. "droop" em itálico na
Tabela 2.1. Armadilha: `<w:t>` sem `xml:space` partido em dois runs perde o
espaço final no Word ("e4.6"). MD5 57ea80…, backup `..._20261102_005630`.

## 2026-11-02 (00h38) — R3 reaplicado sobre a versão do Bruno

O Bruno promoveu às 16h39 de 01/11 o backup `_042452`, que é a versão
**anterior** ao R3, e o parágrafo GFL × GFM e a Tabela 2.1 sumiram. Mesmo
`gen_r3.py` rodado sobre 732e2a… (versão das 18h53 dele): diff 2 trechos, só o
R3; 89 páginas, `audit_pdf_whitespaces` limpo. MD5 75b696…, backup
`..._20261102_003826`. Lição: backup `_HHMMSS` guarda a versão de **antes**
daquela entrega; promover sempre o canônico, nunca o backup mais recente.

## 2026-11-01 (04h24) — R3 do Rafael: GFL × GFM no §2.2 (azul)

Parágrafo novo depois do de Strauss-Mincu et al. (2026): GFM como fonte de
tensão que impõe ângulo e frequência e pode emular inércia (gerador síncrono
virtual), remissão à Tabela 2.1 e escopo só GFL. Tabela 2.1 (IBGE, 8 linhas,
larguras [2672, 3200, 3200]), fonte Gu e Green (2023) e Shadoul et al. (2022),
já nas Referências; sem linha "rede fraca" por falta de fonte citada.
Diff: 2 trechos; backup `..._20261101_042452`. Ver [[pll-reactive-inertia]].

## 2026-11-01 (04h04) — Ajustes pós-R6a

Figura 1.2 sem o "2025*" (asterisco do ONS sem nota; PNG via
`troca_imagem.py`); sigla EMT fora da Lista de Siglas (a forma por extenso
segue no Resumo e no objetivo específico); remissão do §2.5 "Seção 2.1.4"
(inexistente) → "Seção 2.3.2", número em azul. Referência ONS (2025) mantida
como entrou às 04h00. Diff: 2 trechos; backup `..._20261101_040433`.

## 2026-11-01 (04h00) — R2, R5 e R6a do Rafael: Introdução e Cap. 1 (azul)

Introdução: parágrafo com os números do 1.1, 2º parágrafo reescrito (R5, sem
"convencionais": comparação com usinas de geradores síncronos), dois
parágrafos na Motivação (classificação estendida; Chile e Ibéria) e apagão de
2023 igual ao RAP (23.368 MW, p. 15; 34,5%, p. 367; antes 22.547 MW / 31%).
1.1: Figuras 1.1 (IEA 2026) e 1.2 (capacidade no SIN, ONS 2025), de
`scripts/gen_matriz_renovaveis.py`; 1.4: Tabela 1.1 dos três blecautes;
figuras antigas do Cap. 1 viraram 1.3-1.5 (4 remissões em azul); sigla MMGD;
referência ONS (2025) sem título real ("Apresentação ao Senado Federal", a
confirmar), "2025*" do ONS sem nota. Base 58f7f0… (entrega das 03h12 em
[[tcc-historico-entregas-2026-11-01]]); backup `..._20261101_040046`. Ver
[[brasil-2023-overview]].

## 2026-11-01 (01h14) — A2 do André: "Mvar" na Figura 3.1 (verde)

Única ocorrência de VAr no TCC: cargas do unifilar. SVG com "Mvar" e vírgula
decimal (25 valores), PNG reexportado e recortado sem a faixa de título
(topo 285 px, 2760×1740) por `troca_imagem.py`; legenda da Figura 3.1 em
verde (imagem não tem cor de marca). Texto idêntico (`diff_texto` 0
trechos); backup `_backups\VF\..._20261101_011444`. Ver [[ieee9bus-topology]].

## 2026-11-01 (00h53) — A1 do André: "sintonia lenta" (verde)

52 trocas de "sintonia inadequada" por "sintonia lenta" (texto, legendas,
Lista de Ilustrações, células da Tabela 4.3, Resumo; "slow-tuning" no
Abstract), frase do compromisso de banda no §3.3.2.3 e 13 figuras
regeneradas com a legenda nova (Tabela 3.1 com a marca "L"). Script
`C:\Temp\tcc_banca_lenta\gen_banca_lenta.py` + `troca_figuras.py`; backup
`_backups\VF\..._20261101_005325`. Armadilhas: palavra partida em dois runs
("inadequad" | "a") e run com `lastRenderedPageBreak`, contar por `<w:t>`.
Entradas abaixo desta mantêm o nome antigo. Ver [[cenarios-simulados]].

## Entregas de 2026-10-25 a 2026-10-31

Ver [[tcc-historico-entregas-2026-10-25]]: sigla pedida pelo Oscar fora do TCC, revisão do Cleiton em vermelho e 1ª rodada
Rafael (azul) / André (verde): R7, A3 e renumeração (3.N) → (2.N).

## Entregas de 2026-10-15

Ver [[tcc-historico-entregas-2026-10-15]]: referências de delimitação de
escopo (ALI et al., 2025; IEEE 2800.2) e Figura 3.2 só em diagrama de blocos.

## Entregas de 2026-10-12 a 2026-10-14

Ver [[tcc-historico-entregas-2026-10-12]]: comentários do Oscar de 11/10,
P e Q de 03/10 reaplicados, 180° = oposição de fase, ANEXOS removido e
primeiro ciclo = salto de fase; restauração de 13/10 e monofásica na Barra 7 (14/10).

## Entregas de 2026-10-03

Ver [[tcc-historico-entregas-2026-10-03]]: comentários do Oscar após a
Figura 5.8 (3 tabelas e 2 figuras), "Referência" no §5.1, Figura 4.2 com
letras maiores e escala de P e Q corrigida com potências médias.

## Entregas de 2026-10-02

Ver [[tcc-historico-entregas-2026-10-02]]: Figura 3.1 do controle de corrente
dq, fontes "Adaptado de" nas figuras conceituais, Figura 4.1 redesenhada com
a potência da UFV, Cap. 5 restaurado após save por cima.

## Entregas de 2026-10-01

Ver [[tcc-historico-entregas-2026-10-01]]: gráficos e texto do Cap. 5 da
safra de 01/10, texto antes das figuras, "reaquisitar" fora, citações de
alto risco e referências pedidas pelo Oscar.

## Entregas de 2026-09-27 a 2026-09-29

Ver [[tcc-historico-entregas-2026-09-fim]]: citação de "redes fracas" para Wu
e Wang, Xiong na Motivação (comentário 16) e 38 comentários novos do Oscar
mesclados no Cap. 5.

## Entregas de 2026-09-26

Ver [[tcc-historico-entregas-2026-09-26]]: comentários do Oscar no V10
(notação do PLL, Resumo/Abstract, figuras ONS), comentário 16 com o Xiong
(duas tentativas revertidas) e siglas definidas uma vez só.

## Entregas de 2026-09-13

Ver [[tcc-historico-entregas-2026-09-13]]: passagem ABNT completa, lista de
siglas revisada contra o texto, subscrito nos símbolos do texto corrido.

## Entregas de 2026-09-12

Ver `historico_entregas_2026_09_12.md`: referências em amarelo fechadas,
revisão de português do documento inteiro, Cap. 7 e Cap. 6 redigidos.

## Entregas de setembro/2026 até o dia 09

Ver `historico_entregas_2026_09_inicio.md` — troca de terminologia
PAC → PCC (2026-09-09), mesclagem dos Cap. 4 e 5 do fragmento no
canônico e enxugamento analítico do Cap. 5 (ambas de 2026-09-02).

## Entregas de agosto/2026

Ver `historico_entregas_2026_08.md` — nova §3.5 (controlador de corrente) +
referências cruzadas Cap.3↔Cap.4, passe de estilo Fase 2, e os ganhos do PLL
(§3.4) / CIGRE (§2.3) / dois cenários (§4.3.3) / duas etapas (§4.3.2).

## Entregas de julho/2026 (2026-07-22 e anteriores)

Ver `historico_entregas_2026_07.md` — inclui a remoção retroativa de
travessão, a remoção de linguagem de código/merge de 4.3.2.1–4.3.3.2, e o
incidente de corrupção que motivou a troca para `TCC_Victor_Bruno_V9_novo_indice_2.docx`.

## Entregas anteriores (V8)

Ver `historico_entregas_v8.md` (fragmentado em 2026-07-22 por limite de linhas).

## Relacionados

- [[tcc-historico-entregas-2026-11-01]] — Figura 2.2 com a planta LCL (2026-11-01 03h12)
- [[tcc-historico-entregas-2026-08]] — histórico detalhado de agosto
- [[tcc-historico-entregas-2026-09-26]] — entregas de 2026-09-26 (V10)
