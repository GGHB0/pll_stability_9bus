"""
kb_links.py
Interliga os .md de .claude/ — aliases, índices por pasta, grafo e auditoria.

Convenção: `[[slug]]` aponta para o `name:` (ou `aliases:`) do frontmatter de
outro doc. O `aliases: [slug]` faz o Obsidian/Foam resolver o link, já que o
nome do arquivo (pll_contingencies.md) difere do slug (pll-contingencies).

Uso:
    python scripts/kb_links.py aliases   # insere aliases: [name] onde falta
    python scripts/kb_links.py index     # (re)gera index.md de cada pasta + raiz
    python scripts/kb_links.py graph     # (re)gera .claude/kb/grafo.md (Mermaid)
    python scripts/kb_links.py check     # links quebrados e órfãos (exit 1 se quebrado)
    python scripts/kb_links.py all       # aliases + index + graph + check
"""

import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ_ROOT = Path(__file__).resolve().parent.parent
CLAUDE = PROJ_ROOT / ".claude"
KB = CLAUDE / "kb"
MAX_LINES = 200
BEGIN, END = "<!-- kb-links:begin -->", "<!-- kb-links:end -->"
GENERATED = {"index.md", "grafo.md"}

FM_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.S)
WIKI_RE = re.compile(r"\[\[([^\]|#\n]+)(?:[#|][^\]\n]*)?\]\]")
MDLINK_RE = re.compile(r"\]\(([^)#\s]+\.md)(?:#[^)]*)?\)")
CODE_RE = re.compile(r"```.*?```|`[^`\n]*`", re.S)


@dataclass
class Doc:
    path: Path
    text: str
    name: str | None = None
    description: str = ""
    aliases: list[str] = field(default_factory=list)

    @property
    def rel(self) -> str:
        return self.path.relative_to(CLAUDE).as_posix()

    @property
    def slugs(self) -> set[str]:
        return {s for s in [self.name, *self.aliases] if s}

    def outlinks(self) -> tuple[set[str], set[Path]]:
        body = CODE_RE.sub("", self.text)
        wiki = {w.strip() for w in WIKI_RE.findall(body)}
        md = {(self.path.parent / l).resolve() for l in MDLINK_RE.findall(body)}
        return wiki, md


def parse(path: Path) -> Doc:
    text = path.read_text(encoding="utf-8", errors="replace")
    doc = Doc(path, text)
    m = FM_RE.match(text)
    if not m:
        return doc
    fm = m.group(1)
    if n := re.search(r"^name:\s*(.+?)\s*$", fm, re.M):
        doc.name = n.group(1).strip("\"'")
    if d := re.search(r"^description:\s*(.+?)\s*$", fm, re.M):
        doc.description = d.group(1).strip("\"'")
    if a := re.search(r"^aliases:\s*\[(.*?)\]", fm, re.M):
        doc.aliases = [s.strip(" \"'") for s in a.group(1).split(",") if s.strip()]
    return doc


def load_docs() -> list[Doc]:
    paths = [p for p in CLAUDE.rglob("*.md") if "worktrees" not in p.parts]
    return [parse(p) for p in sorted(paths)]


def slug_map(docs: list[Doc]) -> dict[str, Doc]:
    return {s: d for d in docs for s in d.slugs}


def short(text: str, n: int = 140) -> str:
    text = text.replace("|", "/")
    return text if len(text) <= n else text[: n - 1].rstrip() + "…"


# ── aliases ────────────────────────────────────────────────────────────────────
def cmd_aliases(docs: list[Doc]) -> None:
    added, skipped = 0, []
    for d in docs:
        if not d.name or d.aliases or not d.path.is_relative_to(KB):
            continue
        if len(d.text.splitlines()) + 1 > MAX_LINES:
            skipped.append(d.rel)
            continue
        nl = "\r\n" if "\r\n" in d.text else "\n"
        new = re.sub(r"^(name:.*?)(\r?\n)", rf"\1\2aliases: [{d.name}]{nl}",
                     d.text, count=1, flags=re.M)
        d.path.write_text(new, encoding="utf-8", newline="")
        added += 1
    print(f"aliases: {added} inseridos")
    for s in skipped:
        print(f"  pulado (passaria de {MAX_LINES} linhas): {s}")


# ── índices ────────────────────────────────────────────────────────────────────
def write_managed(path: Path, header: str, body: str) -> bool:
    """Grava o bloco entre marcadores; preserva texto manual fora dele.
    Índice escrito à mão (sem marcadores) não é tocado."""
    block = f"{BEGIN}\n{body.rstrip()}\n{END}\n"
    if path.exists():
        old = path.read_text(encoding="utf-8")
        if BEGIN not in old:
            print(f"  mantido (índice manual): {path.relative_to(CLAUDE).as_posix()}")
            return False
        new = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n?",
                     lambda _: block, old, flags=re.S)
    else:
        new = header + "\n" + block
    lines = len(new.splitlines())
    if lines > MAX_LINES:
        print(f"  AVISO: {path.name} com {lines} linhas (> {MAX_LINES})")
    path.write_text(new, encoding="utf-8")
    return True


def folder_of(doc: Doc) -> str | None:
    if not doc.path.is_relative_to(KB):
        return None
    parts = doc.path.relative_to(KB).parts
    return parts[0] if len(parts) > 1 else None


def folder_edges(docs: list[Doc]) -> Counter:
    smap, by_path = slug_map(docs), {d.path.resolve(): d for d in docs}
    edges: Counter = Counter()
    for d in docs:
        src = folder_of(d)
        if not src or d.path.name in GENERATED:
            continue
        wiki, md = d.outlinks()
        targets = [smap[w] for w in wiki if w in smap] + [by_path[p] for p in md if p in by_path]
        for t in {t.path for t in targets}:
            dst = folder_of(by_path[t.resolve()])
            if dst and dst != src:
                edges[(src, dst)] += 1
    return edges


def cmd_index(docs: list[Doc]) -> None:
    folders = sorted(p.name for p in KB.iterdir() if p.is_dir())
    edges = folder_edges(docs)
    for folder in folders:
        items = [d for d in docs if folder_of(d) == folder and d.path.name not in GENERATED]
        groups: dict[str, list[Doc]] = defaultdict(list)
        for d in items:
            sub = d.path.parent.relative_to(KB / folder).as_posix()
            groups["" if sub == "." else sub].append(d)
        body = ["## Documentos"]
        for sub in sorted(groups):
            body += ["", f"### {sub}/", ""] if sub else [""]
            body += ["| Arquivo | Link | Cobre |", "|---|---|---|"]
            for d in groups[sub]:
                rel = d.path.relative_to(KB / folder).as_posix()
                slug = f"[[{d.name}]]" if d.name else "—"
                body.append(f"| [{d.path.name}]({rel}) | {slug} | {short(d.description)} |")
        related = sorted({b for (a, b) in edges if a == folder} | {a for (a, b) in edges if b == folder})
        body += ["", "## Pastas relacionadas", ""]
        body += [f"- [{r}/](../{r}/index.md) — saem {edges[(folder, r)]}, "
                 f"chegam {edges[(r, folder)]}" for r in related] or ["- (nenhuma)"]
        body += ["", "Voltar: [índice do KB](../index.md) · [grafo](../grafo.md)"]
        header = (f"---\nname: kb-index-{folder}\ndescription: Índice da pasta {folder}/ do KB "
                  f"(gerado por scripts/kb_links.py)\naliases: [kb-index-{folder}]\n---\n\n"
                  f"# KB — {folder}/\n\nGerado por `scripts/kb_links.py index`; texto fora dos "
                  f"marcadores é preservado.\n")
        write_managed(KB / folder / "index.md", header, "\n".join(body))
    write_root_index(docs, folders)
    print(f"index: {len(folders)} pastas + raiz")


def first_heading(doc: Doc) -> str:
    m = re.search(r"^#\s+(.+)$", FM_RE.sub("", doc.text), re.M)
    return m.group(1).strip() if m else ""


def write_root_index(docs: list[Doc], folders: list[str]) -> None:
    body = ["## Pastas do KB", "", "| Pasta | Docs | Índice |", "|---|---|---|"]
    for f in folders:
        n = sum(1 for d in docs if folder_of(d) == f and d.path.name not in GENERATED)
        body.append(f"| {f}/ | {n} | [{f}/index.md]({f}/index.md) |")
    loose = [d for d in docs if d.path.parent == KB and d.path.name not in GENERATED]
    body += ["", "Soltos na raiz: " + ", ".join(f"[{d.path.name}]({d.path.name})" for d in loose)]
    body += ["", "Mapa de relações entre pastas: [grafo.md](grafo.md)", "", "## Skills", ""]
    for skill in sorted((CLAUDE / "skills").glob("*/SKILL.md")):
        aux = [d for d in docs if d.path.parent == skill.parent and d.path.name != "SKILL.md"]
        extra = " · ".join(f"[{d.path.stem}](../skills/{skill.parent.name}/{d.path.name})" for d in aux)
        body.append(f"- [{skill.parent.name}](../skills/{skill.parent.name}/SKILL.md)"
                    + (f" — {extra}" if extra else ""))
    body += ["", "## Agentes", ""]
    for d in docs:
        if d.path.parent == CLAUDE / "agents":
            body.append(f"- [{d.path.stem}](../agents/{d.path.name}) — {short(d.description, 110)}")
    body += ["", "## Regras", ""]
    for d in docs:
        if d.path.parent == CLAUDE / "rules":
            body.append(f"- [{d.path.stem}](../rules/{d.path.name}) — {short(first_heading(d), 110)}")
    header = ("---\nname: kb-index\ndescription: Porta de entrada do KB — pastas, skills, agentes "
              "e regras (gerado por scripts/kb_links.py)\naliases: [kb-index]\n---\n\n"
              "# Knowledge Base — índice geral\n\nGerado por `scripts/kb_links.py index`. "
              "Links `[[slug]]` abrem no Obsidian (vault = `.claude/`) ou no VS Code com Foam. "
              "Convenção em [rules/kb-links.md](../rules/kb-links.md); ponteiro legado em "
              "[INDEX.md](../INDEX.md).\n")
    write_managed(KB / "index.md", header, "\n".join(body))


# ── grafo ──────────────────────────────────────────────────────────────────────
def cmd_graph(docs: list[Doc]) -> None:
    edges = folder_edges(docs)
    nid = lambda f: re.sub(r"\W", "_", f)
    body = ["```mermaid", "graph LR"]
    folders = sorted({f for e in edges for f in e})
    body += [f'    {nid(f)}["{f}/"]' for f in folders]
    body += [f"    {nid(a)} -->|{n}| {nid(b)}" for (a, b), n in sorted(edges.items())]
    body += ["```", "", "Número na seta = quantos docs da origem apontam para docs do destino.",
             "Grafo arquivo a arquivo: Graph View do Obsidian (vault = `.claude/`)."]
    header = ("---\nname: kb-grafo\ndescription: Grafo Mermaid das relações entre pastas do KB "
              "(gerado por scripts/kb_links.py)\naliases: [kb-grafo]\n---\n\n"
              "# KB — grafo de relações entre pastas\n\nVoltar: [índice do KB](index.md)\n")
    write_managed(KB / "grafo.md", header, "\n".join(body))
    print(f"graph: {len(edges)} arestas entre {len(folders)} pastas")


# ── auditoria ──────────────────────────────────────────────────────────────────
def cmd_check(docs: list[Doc]) -> int:
    smap, paths = slug_map(docs), {d.path.resolve() for d in docs}
    inbound: Counter = Counter()
    broken = []
    for d in docs:
        wiki, md = d.outlinks()
        for w in wiki:
            if w in smap:
                inbound[smap[w].path.resolve()] += 1
            else:
                broken.append((d.rel, f"[[{w}]]"))
        for p in md:
            if p in paths:
                inbound[p] += 1
            elif not p.exists():
                broken.append((d.rel, p.name))
    dup = [s for s, n in Counter(s for d in docs for s in {d.name} if s).items() if n > 1]
    orphans = [d.rel for d in docs if inbound[d.path.resolve()] == 0
               and d.path != KB / "index.md" and "worktrees" not in d.path.parts]
    unlinked = [d.rel for d in docs if folder_of(d) and d.path.name not in GENERATED
                and not any(d.outlinks())]
    print(f"check: {len(docs)} docs · {len(broken)} links quebrados · {len(orphans)} órfãos"
          f" · {len(unlinked)} sem referência")
    for src, link in broken:
        print(f"  QUEBRADO {src} → {link}")
    for s in dup:
        print(f"  SLUG DUPLICADO {s}")
    for o in orphans:
        print(f"  órfão {o}")
    for u in unlinked:
        print(f"  sem referência (não aponta para nenhum tema) {u}")
    return 1 if broken or dup else 0


def main() -> int:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    steps = ["aliases", "index", "graph", "check"] if cmd == "all" else [cmd]
    rc = 0
    for step in steps:
        docs = load_docs()  # recarrega: passos anteriores mudam os arquivos
        fn = {"aliases": cmd_aliases, "index": cmd_index, "graph": cmd_graph, "check": cmd_check}[step]
        rc = fn(docs) or rc
    return rc


if __name__ == "__main__":
    sys.exit(main())
