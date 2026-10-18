# Sincronia do deck com o TCC

Continuação de `SKILL.md`. O deck resume o TCC **entregue à banca** (`DOCX_TCC`
em `config.py`, hoje o VFinal de 15/10/2026; pode diferir do `DOCX_SOURCE`
de edição da `tcc-docx-editor`). A banca leu o
TCC: número, figura ou afirmação diferente no slide vira pergunta.

## Fontes de verdade, nesta ordem

1. **Texto do TCC canônico**: o que a banca tem na mão. Extrair o
   `document.xml` para o staging e buscar com os scripts da `tcc-docx-editor`:
   ```text
   python.exe ..\tcc-docx-editor\scripts\find_text.py <document.xml> "58,4"
   python.exe ..\tcc-docx-editor\scripts\dump_blocks.py <document.xml> <ini> <fim>
   ```
   Tabelas 5.1-5.3 e legendas: `dump_headings.py` acha o capítulo, depois
   `dump_blocks.py` no intervalo.
2. **KB**: ganhos e sintonia (`kb/pll/sintonia/`), cenários
   (`kb/simulation/cenarios_simulados.md`), estado do TCC
   (`kb/tcc-word/content_map.md`, `historico/historico_entregas*.md`).
3. **KB e simulação não autorizam número no deck.** Servem para conferir
   e para responder perguntas da banca (`output/defesa_qa.pdf`), nunca para
   pôr no slide o que o TCC não diz.

## O que conferir em toda edição de conteúdo

- **Números**: cada valor do slide e das notas contra o TCC, com o mesmo
  arredondamento e a mesma unidade (ms × s, % × pu, rad/s × Hz). Refazer as
  contas que forem refazíveis (ωn = √Ki, ξ = Kp/2ωn, 4,6/(ξ·ωn)) com o
  python, sem confiar no texto.
- **Contagens de cenários**: "N cenários, X nominais e Y inadequados" e
  "falta F na barra B só com a sintonia nominal" mudam a cada rodada nova.
  Conferir na Tabela 4.1 do TCC e em `cenarios_simulados.md`.
- **Legendas**: `check_pptx.py --tcc "<DOCX_TCC>"` confere se o número
  existe e se o tipo (Figura/Tabela) bate. Depois, a olho: o título da
  legenda do TCC (o script imprime as legendas lidas) descreve a imagem
  que está na moldura?
- **Figura em si**: a imagem do slide é a mesma do TCC? Figura regenerada
  no TCC (ex.: P/Q corrigidos em 03/10) precisa ser trocada aqui também
  (`casos/troca_figura.md`). O esboço de 2026-10-16 tinha 4 de 10 figuras
  velhas: comparar cada mídia com o PNG de mesmo papel em `assets/charts/`
  (`git log` do PNG depois da data do deck = suspeita). Não extrair a
  figura do DOCX pela legenda: a Lista de Ilustrações casa primeiro.
- **Notas de fala**: os mesmos números aparecem por extenso nas notas.
  `find_text.py <deck> "<valor>" --notas` em cada valor alterado.

## Número ou afirmação que o TCC não tem

Sai do deck, na tela e nas notas (ex.: em 2026-10-17 saíram Vcc 136,36 kV,
L1/L2/Cf, "partida até 0,1 s", a janela da retenção, a coluna "Vd mínima e
máxima" e o cartão "grid-forming"). Se a banca pode perguntar, a resposta
vai para o PDF de perguntas e respostas, não para o slide.

## TCC com inconsistência interna

O TCC entregue pode dizer duas coisas (ex.: Tabela 4.1 com 28 cenários e
Tabela 5.3 já com o 29º; 22.547 MW na introdução e 23.368 MW na §2.4.3). O
deck não cita a contagem em conflito, ou usa a seção dedicada ao assunto;
registrar em `kb/tcc-pptx/pendencias.md` e avisar o Victor.

## Ao terminar

Divergência encontrada e não corrigida nesta entrega vai para
`kb/tcc-pptx/pendencias.md` com slide, valor do deck, valor do TCC e fonte.
