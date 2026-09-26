---
name: claude-index
description: Ponteiro para o índice geral do sistema .claude/ (kb/index.md, gerado por script)
aliases: [claude-index]
---

# Índice do Sistema .claude/

O índice agora é gerado automaticamente a partir do frontmatter de cada doc:

- **[kb/index.md](kb/index.md)**: pastas do KB, skills, agentes e regras
- **[kb/grafo.md](kb/grafo.md)**: grafo Mermaid das relações entre pastas
- Convenção de links: [rules/kb-links.md](rules/kb-links.md)

Para regenerar: `.venv\Scripts\python.exe scripts\kb_links.py all`
