# Armadilhas do pipeline PPTX

Continuação de `SKILL.md`. Ordem: ambiente, python-pptx, PowerPoint, conteúdo.

## Ambiente

- `python-pptx` está **só no `.venv`** (`requirements.txt`). O `python` do
  sistema não tem: sempre `C:\projetos\pll_stability_9bus\.venv\Scripts\python.exe`.
- Script por caminho de arquivo, nunca `python -c` com regex (PowerShell
  quebra `[...]`). `sys.stdout.reconfigure(encoding="utf-8")` (ou
  `pptx_util.utf8()`): o console é cp1252 e morre em `→`, `ξ`, `ω`.
- `python -I` ignora `PYTHONIOENCODING`: o reconfigure é o que resolve.

## python-pptx

- **Nome de forma não é único**: o deck tem vários "Text 2" no mesmo slide
  e "Cartão de destaque" ×3. Localizar por nome **e** índice do
  `dump_slides.py`, e conferir o texto antigo antes de trocar.
- `shape.text = ...` / `text_frame.text = ...` **apaga a formatação** dos
  runs (tamanho, cor, negrito). Para trocar texto mantendo o estilo:
  escrever no primeiro run (`p.runs[0].text = novo`) e esvaziar os demais,
  ou copiar o `rPr` do run antigo para o novo.
- Texto com dois estilos na mesma linha ("**Justificativa de ouro:** Por
  que...") são runs distintos: trocar run a run.
- Tabela: `cell.text = x` também perde a formatação; usar
  `cell.text_frame.paragraphs[0].runs[0].text`. Linha nova = deepcopy de
  `tbl.tr` existente + ajustar a altura da forma (a tabela não cresce sozinha
  no arquivo; o PowerPoint recalcula só ao abrir).
- Notas: `slide.notes_slide.notes_text_frame`. Acessar `notes_slide` **cria**
  as notas se não existirem: checar `slide.has_notes_slide` antes de ler.
- Duplicar slide não existe na API: deepcopy do `spTree` num slide novo do
  mesmo layout + copiar as relações de imagem (`get_or_add_image_part`).
  Mover slide: reordenar `prs.slides._sldIdLst`.
- Remover slide: tirar do `_sldIdLst` **e** `drop_rel` na presentation part,
  senão o slide fica órfão no pacote e o PowerPoint pode pedir reparo.
- `add_picture` com só `width` mantém a proporção; com width e height
  deforma. Para trocar figura, usar `troca_imagem.py`.

## PowerPoint (COM)

- **Instância única**: `New-Object -ComObject PowerPoint.Application` se
  pendura no PowerPoint que o Victor tiver aberto. `Quit()` fecharia a
  apresentação dele: `render.ps1` e `pptx_finalize.ps1` só dão Quit se não
  havia PowerPoint rodando antes. O processo some alguns segundos depois do
  Quit; não matar.
- `Presentations.Open(path, ReadOnly, Untitled, WithWindow)`: sem janela,
  arquivo corrompido vira exceção em vez de diálogo de reparo travado.
- Export de slide em PNG usa as fontes instaladas na máquina: o render
  daqui vale para o notebook da defesa só se as fontes forem as mesmas
  (Arial/Calibri, sem risco). Levar também o PDF (`-Pdf`).

## Conteúdo

- O deck veio de um gerador (nomes "Text N", mídia `image-<slide>-<n>.png`):
  as notas terminam às vezes com o número do slide solto ("... 22"). O
  `pptx_util.falas` ignora esse resto; ao reescrever notas, não repetir.
- Legenda "Figura X.Y do TCC" é texto fixo, não campo: renumeração no TCC
  não chega aqui sozinha. `check_pptx.py --tcc` pega número inexistente,
  **não** pega número que existe mas aponta para outra figura: conferir o
  título da legenda do TCC contra a imagem.
- Número de simulação: o TCC canônico manda. P e Q do UFV de rodada antiga
  estão em escala errada (CLAUDE.md); número de P/Q que não esteja no TCC
  passa por `src/pipeline/pq.py`, nunca por leitura direta do CSV.
