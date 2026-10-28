---
name: kb-grafo
description: Grafo Mermaid das relações entre pastas do KB (gerado por scripts/kb_links.py)
aliases: [kb-grafo]
---

# KB — grafo de relações entre pastas

Voltar: [índice do KB](index.md)

<!-- kb-links:begin -->
```mermaid
graph LR
    dashboard["dashboard/"]
    events["events/"]
    inverter["inverter/"]
    pll["pll/"]
    power_system["power-system/"]
    psim["psim/"]
    python["python/"]
    simulation["simulation/"]
    standards["standards/"]
    tcc_pptx["tcc-pptx/"]
    tcc_word["tcc-word/"]
    dashboard -->|4| pll
    dashboard -->|2| power_system
    dashboard -->|5| simulation
    dashboard -->|4| standards
    dashboard -->|3| tcc_pptx
    dashboard -->|2| tcc_word
    events -->|2| power_system
    events -->|1| standards
    inverter -->|6| pll
    inverter -->|1| power_system
    inverter -->|2| simulation
    inverter -->|1| standards
    pll -->|2| dashboard
    pll -->|1| events
    pll -->|5| inverter
    pll -->|3| power_system
    pll -->|1| psim
    pll -->|2| simulation
    pll -->|3| standards
    pll -->|7| tcc_word
    power_system -->|1| dashboard
    power_system -->|6| pll
    power_system -->|2| standards
    power_system -->|1| tcc_word
    psim -->|4| inverter
    psim -->|4| pll
    psim -->|1| power_system
    psim -->|4| simulation
    psim -->|1| standards
    python -->|1| dashboard
    simulation -->|6| dashboard
    simulation -->|1| inverter
    simulation -->|3| pll
    simulation -->|1| power_system
    simulation -->|1| psim
    simulation -->|1| standards
    simulation -->|5| tcc_word
    standards -->|4| dashboard
    standards -->|2| events
    standards -->|3| inverter
    standards -->|5| pll
    standards -->|3| power_system
    standards -->|2| simulation
    standards -->|1| tcc_pptx
    standards -->|2| tcc_word
    tcc_pptx -->|3| dashboard
    tcc_pptx -->|1| events
    tcc_pptx -->|2| inverter
    tcc_pptx -->|1| pll
    tcc_pptx -->|4| psim
    tcc_pptx -->|2| simulation
    tcc_pptx -->|3| tcc_word
    tcc_word -->|2| dashboard
    tcc_word -->|2| events
    tcc_word -->|12| pll
    tcc_word -->|9| power_system
    tcc_word -->|11| simulation
    tcc_word -->|4| standards
```

Número na seta = quantos docs da origem apontam para docs do destino.
Grafo arquivo a arquivo: Graph View do Obsidian (vault = `.claude/`).
<!-- kb-links:end -->
