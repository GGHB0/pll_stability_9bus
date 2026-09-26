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
    tcc_word["tcc-word/"]
    dashboard -->|3| pll
    dashboard -->|1| power_system
    dashboard -->|3| simulation
    dashboard -->|1| standards
    events -->|1| power_system
    events -->|1| standards
    inverter -->|6| pll
    inverter -->|1| power_system
    inverter -->|2| simulation
    inverter -->|1| standards
    pll -->|2| dashboard
    pll -->|1| events
    pll -->|2| inverter
    pll -->|3| power_system
    pll -->|1| psim
    pll -->|2| simulation
    pll -->|3| standards
    pll -->|4| tcc_word
    power_system -->|6| pll
    power_system -->|2| standards
    psim -->|3| pll
    psim -->|4| simulation
    python -->|1| dashboard
    simulation -->|6| dashboard
    simulation -->|3| pll
    simulation -->|1| power_system
    simulation -->|1| standards
    simulation -->|4| tcc_word
    standards -->|3| dashboard
    standards -->|2| events
    standards -->|3| inverter
    standards -->|5| pll
    standards -->|3| power_system
    standards -->|2| simulation
    tcc_word -->|1| dashboard
    tcc_word -->|1| events
    tcc_word -->|6| pll
    tcc_word -->|4| power_system
    tcc_word -->|4| simulation
    tcc_word -->|1| standards
```

Número na seta = quantos docs da origem apontam para docs do destino.
Grafo arquivo a arquivo: Graph View do Obsidian (vault = `.claude/`).
<!-- kb-links:end -->
