---
name: defesa-historico-entregas
description: Histórico de entregas do Claude ao deck da defesa (Defesa_TCC_SRF-PLL.pptx), mais recente primeiro
aliases: [defesa-historico-entregas]
---

# Deck da defesa — histórico de entregas

> Uma entrada por entrega ao OneDrive: data, slides tocados, MD5 antes e
> depois, backup gravado, o que o `diff_slides.py` mostrou. Mesmo formato
> de [[tcc-historico-entregas]] (o do TCC DOCX). Mapa em [[defesa-deck-map]].

## 2026-10-16 (madrugada): visual do template "Project Portfolio" (entregue)

- Staging do canônico (MD5 `3231ecd2806662bb5130fd66685f8f32`); script
  `C:\Temp\defesa_tpl\gen_template.py` (grupos layouts, capa, desloca,
  secao, estilo); peças reaproveitáveis em `scripts/template_util.py`.
  Entregue MD5 `a3476f1764dae394ac691d54d7e1bbab`; backup
  `_backups\defesa\Defesa_TCC_SRF-PLL_backup_20261016_012452.pptx`; PDF em
  `C:\Temp\defesa_tpl\final.pdf`.
- Cabeçalho e linha de seção nos layouts, nome da seção girado nos slides
  2-25, conteúdo deslocado para x 1,10-12,95, blocos retos sem borda, tons
  de azul, capa com faixa de 3 figuras. Texto, tabelas e notas intactos
  (`diff_slides`).
- check_pptx 0 FALHA (após corrigir o script para rotação); slide-validator
  sem bloqueio, 2 avisos cosméticos em [[defesa-pendencias]].

## 2026-10-16 (noite) — demo ao vivo + paleta do HTML (entregue, leva junto as pendências 1-5)

- Staging = `final.pptx` da rodada de pendências (canônico intacto, MD5
  `c1a5457ba911ccbc6a1b3a702bc6837a`); script `C:\Temp\defesa_demo\gen_demo.py`
  (grupos novos, fusao, notas, nota, ordem, cor). Entregue MD5
  `3231ecd2806662bb5130fd66685f8f32`; backup
  `_backups\defesa\Defesa_TCC_SRF-PLL_backup_20261016_010232.pptx`; PDF de
  reserva em `C:\Temp\defesa_demo\final.pdf`.
- 24 → 25 slides: 7+8 fundidos; novos 10 (pipeline) e 12 (demonstração);
  notas de 9, 13 e 14 enxugadas; borda nas caixas "Nota"; paleta do HTML.
  Mapa em [[defesa-deck-map]].
- check_pptx 0 FALHA; tempo 25,2 min; slide-validator sem bloqueio (avisos
  visuais corrigidos; o de 0,1 s foi para [[defesa-pendencias]]).
  `diff_slides` backup × canônico: só o previsto (numeração desloca do 8 em diante).

## 2026-10-16 — pendências 1-5 (entregue na rodada da noite)

- Staging do canônico (MD5 `c1a5457ba911ccbc6a1b3a702bc6837a`), script
  `C:\Temp\defesa_pend\gen_pendencias.py` (grupos txt, tab, img, rot,
  notas), finalize com PDF: `final.pptx` MD5 `12a92b103870f424b9f91d90828f6840`.
- Slides tocados: 8, 10, 12, 13, 14, 18, 21, 22 + rótulo em 11 caixas +
  notas de 15 slides. Detalhe em [[defesa-pendencias]].
- check_pptx 0 FALHA / 3 avisos benignos; tempo 24,6 min; slide-validator
  sem bloqueio.
- Entrega abortada pelo PowerPoint aberto; canônico intacto. Lições
  (`a:pPr` solto, instância órfã) em `referencia/armadilhas.md` da skill.

## 2026-10-16 — montagem do pipeline (sem entrega)

- Esboço lido (24 slides, MD5 `c1a5457ba911ccbc6a1b3a702bc6837a`), nada
  gravado no OneDrive.
- Criados: skill `tcc-pptx-editor`, agentes `pptx-runner`, `pptx-scripter`,
  `slide-validator`, esta pasta do KB. `python-pptx 1.0.2` no `.venv`.
- Testados no deck real: dump, find, check (0 FALHA, 5 avisos), tempo de
  fala (30,9 min), troca de imagem, render, finalize com PDF.
- Achados viraram [[defesa-pendencias]] itens 1-6.
