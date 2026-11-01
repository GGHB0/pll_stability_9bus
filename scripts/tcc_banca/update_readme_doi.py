# -*- coding: utf-8 -*-
with open("README.md", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Badge
needle1 = 'src="https://img.shields.io/badge/IEEE-9%20Barras-0F766E?style=for-the-badge">'
badge = '\n  <a href="https://doi.org/10.5281/zenodo.23866787"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.23866787.svg" alt="DOI"></a>'

if needle1 in text and "zenodo.23866787" not in text:
    pos = text.find(needle1) + len(needle1)
    text = text[:pos] + badge + text[pos:]
    print("Badge adicionado ao README.md")

# 2. Citação
needle2 = "Disponível em:\n> <https://github.com/GGHB0/pll_stability_9bus>."
replacement2 = "Disponível em:\n> <https://github.com/GGHB0/pll_stability_9bus>. DOI: 10.5281/zenodo.23866787."
if needle2 in text:
    text = text.replace(needle2, replacement2)
    print("DOI adicionado à citação do README.md")
else:
    needle2_crlf = "Disponível em:\r\n> <https://github.com/GGHB0/pll_stability_9bus>."
    replacement2_crlf = "Disponível em:\r\n> <https://github.com/GGHB0/pll_stability_9bus>. DOI: 10.5281/zenodo.23866787."
    if needle2_crlf in text:
        text = text.replace(needle2_crlf, replacement2_crlf)
        print("DOI adicionado à citação do README.md (CRLF)")

with open("README.md", "w", encoding="utf-8") as f:
    f.write(text)

