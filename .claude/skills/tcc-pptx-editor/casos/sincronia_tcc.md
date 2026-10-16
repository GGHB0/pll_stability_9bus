# Sincronia do deck com o TCC

Continuação de `SKILL.md`. O deck resume o TCC canônico (`DOCX_TCC` em
`config.py`, o mesmo `DOCX_SOURCE` da `tcc-docx-editor`). A banca leu o
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
3. **Simulação** (`output/results/`, via `src/pipeline/`): só para número
   que não está no TCC. Número novo no deck que não está no TCC é decisão
   do Victor: perguntar antes.

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
  (`casos/troca_figura.md`).
- **Notas de fala**: os mesmos números aparecem por extenso nas notas.
  `find_text.py <deck> "<valor>" --notas` em cada valor alterado.

## Ao terminar

Divergência encontrada e não corrigida nesta entrega vai para
`kb/tcc-pptx/pendencias.md` com slide, valor do deck, valor do TCC e fonte.
