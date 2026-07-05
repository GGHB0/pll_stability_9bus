# Python Clean Code Knowledge Base

> **Purpose**: Clean code patterns for Python 3.11+ -- dataclasses, type hints, generators, testing
> **MCP Validated:** 2026-02-17

## Quick Navigation

### Concepts (< 150 lines each)

| File | Purpose |
|------|---------|
| [concepts/dataclasses.md](concepts/dataclasses.md) | @dataclass with slots, frozen, kw_only, field factories |
| [concepts/type-hints.md](concepts/type-hints.md) | Type annotations, generics, Self, TypeVar, 3.12+ syntax |
| [concepts/generators.md](concepts/generators.md) | Generator functions, yield, send, generator expressions |
| [concepts/context-managers.md](concepts/context-managers.md) | with statement, __enter__/__exit__, contextlib |

### Patterns (< 200 lines each)

| File | Purpose |
|------|---------|
| [patterns/file-parser.md](patterns/file-parser.md) | File parsing with generators and context managers |
| [patterns/clean-architecture.md](patterns/clean-architecture.md) | Clean code structure, naming, module organization |
| [patterns/error-handling.md](patterns/error-handling.md) | Exception hierarchy, custom errors, recovery patterns |
| [patterns/functional-patterns.md](patterns/functional-patterns.md) | Comprehensions, map, filter, reduce, functools |
| [patterns/numpy-pandas-plotly.md](patterns/numpy-pandas-plotly.md) | Pipeline de sinais temporais: NumPy/Pandas/Plotly — padrões do projeto |
| [patterns/bad-pll-dashboard-filter.md](patterns/bad-pll-dashboard-filter.md) | Toggle PLL nominal/mal dimensionado no dashboard HTML |
| [patterns/comparison-table.md](patterns/comparison-table.md) | Tabela comparativa de cenários, ordenável, filtrada por modo PLL |
| [patterns/dark-mode-theming.md](patterns/dark-mode-theming.md) | Gotcha do tema escuro — annotations/shapes com cor fixa em chart.py |
| [patterns/header-branding.md](patterns/header-branding.md) | Logo UERJ embutido (base64) + fix do label do toggle de mapa |

### Specs (Machine-Readable)

| File | Purpose |
|------|---------|
| [specs/python-standards.yaml](specs/python-standards.yaml) | Code standards, linting rules, project conventions |

---

## Quick Reference

- [quick-reference.md](quick-reference.md) - Fast lookup tables

---

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Dataclasses** | Declarative data containers with validation, immutability, and slots |
| **Type Hints** | Static typing with generics, unions, and Python 3.12+ syntax |
| **Generators** | Lazy evaluation for memory-efficient data processing |
| **Context Managers** | Resource lifecycle management with guaranteed cleanup |

---

## Learning Path

| Level | Files |
|-------|-------|
| **Beginner** | concepts/dataclasses.md, concepts/type-hints.md |
| **Intermediate** | concepts/generators.md, patterns/clean-architecture.md |
| **Advanced** | patterns/file-parser.md, patterns/functional-patterns.md |

---

## Agent Usage

| Agent | Primary Files | Use Case |
|-------|---------------|----------|
| ai-data-engineer | All files | Write clean, idiomatic Python 3.11+ code |
