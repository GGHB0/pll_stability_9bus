# Referências Bibliográficas Completas

Qualquer arquivo `.md` de `.claude/kb/` que cite **literatura externa**
(livro, tese/dissertação, artigo de periódico, norma/standard, relatório
institucional) precisa, além do `source:` compacto já usado (citação rápida
por página/seção), de um campo `references:` no frontmatter com a(s)
citação(ões) bibliográfica(s) completa(s) — pronta(s) para colar direto na
lista de referências do TCC.

**Why:** o `source:` (`TeseAGP p.58-60`, `IEEE 519-2014 §5`) serve para achar
a seção rápido, mas não bastam para montar a bibliografia final do TCC —
falta autor completo, título por extenso, editora/comitê, edição, ano, DOI.
Reconstituir isso depois, arquivo por arquivo, é trabalho perdido.

**How to apply:** ao criar ou editar um arquivo de KB que cite literatura
externa, adicionar/atualizar `references:` como lista YAML no frontmatter:

```yaml
---
name: exemplo
description: ...
source: Autor p.10-15
references:
  - "SOBRENOME, Nome. Título completo da obra. Editora/Comitê, edição, ano."
---
```

- Uma entrada por fonte externa distinta citada no arquivo (pode haver mais
  de uma).
- Formato livre (ABNT-like), mas sempre com: autor(es), título completo,
  veículo (editora, periódico + volume/número, ou comitê normativo), ano.
  DOI/edição quando disponível.
- **O que conta como "literatura externa":** livros, teses/dissertações,
  artigos de periódico/conferência, normas/standards (IEEE, ONS, PRODIST),
  relatórios institucionais (ENTSO-E, ONS RAP, IEA, Coordinador Eléctrico
  Nacional). **Não conta:** arquivos internos do projeto (`.slx`, notebooks,
  `params.m`), versões anteriores do próprio TCC (TCCs V8), atas de reunião,
  netlists PSIM — esses continuam só em `source:`.
- **Nunca fabricar dado que não foi confirmado** (autor, DOI, edição, ISBN).
  Se a extração do PDF não trouxe essa informação, deixar o campo incompleto
  e anotar `(a confirmar)` no próprio texto da entrada — não inventar.
- Aplica-se retroativamente: ao editar um arquivo de KB antigo que já cite
  literatura sem `references:`, aproveitar e adicionar.
- O fluxo de extração de PDFs (metadados/TOC no Passo 1 da skill
  `pdf-kb-updater`) normalmente já traz autor/título/ano suficientes para
  montar a entrada — conferir ali antes de deixar campo incompleto.
