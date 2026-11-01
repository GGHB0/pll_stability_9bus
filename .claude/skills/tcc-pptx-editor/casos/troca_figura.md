# Troca de figura

Continuação de `SKILL.md`. Figuras do deck vêm do TCC (PNG exportado do
DOCX ou gerado pelos scripts de figura do projeto) e ficam numa "Moldura da
figura" com legenda "Figura X.Y do TCC: ...".

## De onde tirar o PNG

- **Figura do TCC**: a mídia do DOCX canônico (`word/media/`), achada pelo
  `rId` da legenda. É a mesma que a banca viu. Preferir à regeneração.
- **Gráfico regenerado** (`scripts/` do projeto, dashboard): só se o TCC
  também recebeu o novo; senão o deck passa a mostrar outra coisa.
- **Versão para projeção** (mesmos dados, desenho no tamanho do slide):
  `casos/figura_dedicada.md`.
- **Diagrama** (`assets/diagrams/*.svg`): PNG via skill `svg-diagrams`
  (`export_png.ps1`).
- Resolução: ≥ 150 px por polegada **exibida** (moldura de 6 in → ≥ 900 px
  de largura). O `check_pptx.py` avisa abaixo disso.

## Trocar

```text
python.exe scripts\troca_imagem.py deck.pptx <slide> "<forma>" novo.png montado.pptx
```

- `<forma>`: nome ("Image 0") ou o índice `[i]` do `dump_slides.py`.
- O PNG cabe na caixa antiga pela proporção dele, centrado. Proporção
  muito diferente deixa faixa vazia na moldura: aí ajustar a moldura (e a
  legenda) junto, no `gen_*.py`, seguindo `referencia/design.md` (imagem
  0,15 in para dentro da moldura, legenda logo abaixo).
- `--esticar` só para PNG gerado na mesma proporção da caixa.
- Legenda: conferir se o número e a descrição continuam valendo; trocar no
  mesmo script.

## Conferir

Render do slide (`render.ps1 -Slides "<n>"`) e ler o PNG: texto da figura
legível de longe (eixos, legenda do gráfico), sem corte na borda, moldura
alinhada com as caixas ao lado.
