---
name: defesa-historico-entregas
description: Histórico de entregas do Claude ao deck da defesa (Defesa_TCC_SRF-PLL.pptx), mais recente primeiro
aliases: [defesa-historico-entregas]
---

# Deck da defesa — histórico de entregas

> Uma entrada por entrega ao OneDrive: data, slides tocados, MD5 antes e
> depois, backup gravado, o que o `diff_slides.py` mostrou. Mesmo formato
> de [[tcc-historico-entregas]] (o do TCC DOCX). Mapa em [[defesa-deck-map]].

## 2026-10-16 — montagem do pipeline (sem entrega)

- Esboço lido (24 slides, MD5 `c1a5457ba911ccbc6a1b3a702bc6837a`), nada
  gravado no OneDrive.
- Criados: skill `tcc-pptx-editor`, agentes `pptx-runner`, `pptx-scripter`,
  `slide-validator`, esta pasta do KB. `python-pptx 1.0.2` no `.venv`.
- Testados no deck real: dump, find, check (0 FALHA, 5 avisos), tempo de
  fala (30,9 min), troca de imagem, render, finalize com PDF.
- Achados viraram [[defesa-pendencias]] itens 1-6.
