# Mesclar um Fragmento no TCC Canônico

Extraído de `fragmento_externo.md` em 2026-09-02 pelo limite de 200 linhas.
Primeira aplicação: Cap. 4 e 5 em 2026-09-02, registrada em
`kb/tcc-word/mesclagem_cap45_canonico.md`.

Feito pela primeira vez em 2026-09-02 (ver [[tcc-mesclagem-cap45-canonico]]).
**Não é copiar e colar**, e nenhuma das três incompatibilidades avisa quando
está errada:

- **Antes de qualquer coisa, compare as duas árvores de seção.** O fragmento
  pode ser mais **raso** que o capítulo que ele substitui. Em 2026-09-02 o
  Cap. 4 do fragmento tinha 43 parágrafos contra ~144 blocos do canônico, e a
  troca apagou modelagem de gerador, topologia de falta, três tabelas e quatro
  comentários do Bruno. Levantar o inventário de perdas e **apresentar antes de
  editar** — a decisão é do usuário, e ele escolheu perder mesmo assim.
- **Título sem `pStyle` não entra no sumário.** O fragmento é plain-Normal:
  os títulos são parágrafos em negrito `w:sz` 36, sem estilo. Mapear por
  padrão de texto: `Capítulo N:` → `Ttulo1` (sz 48), e a contagem de pontos do
  número → `Ttulo2` (36) / `Ttulo3` (28) / `Ttulo4` (24). Normalizar também a
  pontuação (`Capítulo 5:` → `Capítulo 5 – `, `5.1` → `5.1.`).
- **A convenção de figura pode estar invertida.** No fragmento a legenda fica
  **abaixo** da imagem, em itálico 11 pt, com hífen; no canônico fica **acima**,
  12 pt, com travessão curto, e há um parágrafo "Fonte: Os autores (2026)."
  depois da imagem. Reordenar `[IMG][legenda]` → `[legenda][IMG][Fonte]`.
- **⚠️ Tamanho de página: o fragmento é Carta e o TCC é A4.** Área útil de
  6,50 in contra **6,30 in**. As figuras montadas em largura cheia estouram a
  margem direita, e nada denuncia isso a não ser medir. Derivar a largura do
  `sectPr` **de destino**, nunca assumir:

  ```python
  UTIL_TW  = pgSz_w - pgMar_right - pgMar_left   # twips
  UTIL_EMU = UTIL_TW * 635                       # 1 twip = 635 EMU
  ```

  e reescalar preservando a proporção em `wp:extent` **E** em `a:ext` (mesma
  armadilha do clone de figura, acima). Fechar com um `assert` de que nenhuma
  imagem do documento final passa de `UTIL_EMU`.
- **Comentário órfão tem três partes, não uma.** Apagar de `comments.xml` deixa
  `commentsExtended.xml` e `commentsIds.xml` apontando para `paraId` inexistente.
  Comparar os `paraId` dessas duas partes contra os de **`comments.xml`**, não
  contra os de `document.xml` — o `paraId` de um comentário vivo não está no
  corpo, e a comparação errada acusa falso positivo.
- **Remover `w14:paraId`/`w14:textId`** dos parágrafos importados: os dois
  arquivos têm faixas próprias e podem colidir. O Word regenera ao salvar.
- **Renomear a mídia importada.** Os dois DOCX começam em `image1.png`; entrar
  como `pll_imageN.png` evita sobrescrita silenciosa. `rId` e `docPr`/`cNvPr`
  em faixas altas e distintas, com `assert` de unicidade no fim.
- Marcar o campo TOC com `w:dirty="true"` e confirmar, no PDF exportado, que o
  sumário reconstruído lista as seções novas.

