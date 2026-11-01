# Trocar o template visual do deck

Continuação de `SKILL.md`. Feito em 2026-10-16: deck passou para o visual
do "Project Portfolio" (SlidesCarnival), escolhido entre 9 candidatos.
Resultado em `referencia/design.md`; peças em `scripts/template_util.py`.

## 1. Achar e mostrar opções

- **SlidesCarnival** baixa direto, sem login: a página do template
  (`slidescarnival.com/template/<slug>/<id>`) tem links
  `slidescarnival.com/download/sc<NNNNN>/<slug>/pptx`. Achar com
  `curl -A "Mozilla/5.0" <página> | grep -oE '.../download/sc[0-9]+/[a-z0-9-]+/pptx'`.
  Conferir que o slug do link é o do template: a página também lista
  "relacionados", e o primeiro link pode ser de outro. Tags úteis:
  `/tag/minimalist`, `/tag/technology`, `/tag/thesis`.
- Slidesgo, Envato e Microsoft Create pedem clique, contagem ou login: passar
  o link ao Victor.
- `file -b` confirma "Microsoft PowerPoint 2007+"; `render.ps1 -Slides
  "1,2,...,8" -Folha` em cada um; juntar as folhas rotuladas numa imagem só
  (PIL, faixa escura com o nome) para o Victor comparar.
- Descartar logo: fundo escuro (projetor), dependente de foto de banco de
  imagem, cores berrantes, fontes que não renderizam.
- Licença CC BY 4.0: creditar o SlidesCarnival (linha discreta no fim).

## 2. Ler o template

- Export do Canva/Google: o master é o padrão do Office e todos os slides
  usam o layout `BLANK`; o visual (cabeçalho, linhas, textos fixos) mora no
  **slide master**. `dump_slides.py` não mostra isso: ler as formas de
  `prs.slide_master` (posição, rotação, `sz`, `srgbClr`, `typeface`).
- Tamanho da página do template pode ser outro (o "Project Portfolio" tem
  20 × 11,25 in): converter medidas e pontos pelo fator (aqui 1/1,5).

## 3. Aplicar: recriar a linguagem, não copiar slides

Copiar 25 slides para o arquivo do template quebraria nomes de forma,
notas, mídia e o pipeline inteiro. O que funciona:

1. **Layouts** `COVER`/`CONTENT`/`DIVIDER`: tirar o cabeçalho antigo e
   anexar as formas novas. `LayoutShapes` não cria formas: usar
   `Rascunho` (fabrica num slide temporário, copia o XML, `descarta()`
   antes de salvar).
2. **Elemento que muda por slide** (nome da seção): forma no slide
   (`rotulo_secao`), não no layout.
3. **Deslocar o conteúdo** se a área útil mudou (`desloca`; uma vez só).
   Tabela precisa de `gridCol` escalado, senão o PowerPoint ignora a nova
   largura.
4. **Estilo** (`estilo_chapado`): cores aparecem como `srgbClr` **e** como
   `schemeClr` (`accent1`, `accent4`, `accent6`...); tratar os dois. Trocar
   só o hex no zip pega metade das formas.
5. **Fundo**: hex do fundo no layout/master, por substituição no zip.
6. Capa: refazer à mão (posições e tamanhos explícitos nos placeholders).

## 4. Conferir

- `check_pptx.py` entende rotação desde 2026-10-16 (antes, rótulo girado
  dava falso "fora do slide").
- Render completo + `slide-validator`; `diff_slides.py` deve mostrar só
  posição, estilo e as formas novas, sem texto, tabela ou nota.
- Atualizar `referencia/design.md` (grade, cores, caixas) e a grade citada
  no agente `slide-validator`.
