---
name: tcc-armadilhas-xml
description: Armadilhas de edição direta do OOXML do TCC aprendidas na prática — corrupção por ET.write, proofErr, sectPr, falso positivo de w:p
---

# Armadilhas de Edição XML (aprendidas na prática)

> Fragmentado de `docx_structure.md` em 2026-08-04 (limite de 200 linhas).
> Padrões XML e registro de IDs continuam lá.

## Corrupção do arquivo

- **NUNCA usar `ET.parse` + `tree.write()` no `document.xml` inteiro.** Colapsa
  namespaces declarados mas usados só em `mc:Ignorable`/`AlternateContent`, e o
  Word passa a recusar o arquivo. Só `str.replace`/regex sobre o texto bruto,
  com `ET.fromstring` apenas para **validar** antes de gravar.
  - O script legado `C:\Temp\set_toc_dirty_true.py` faz exatamente isso e
    **não deve ser usado**. Substituto seguro: `C:\Temp\set_toc_dirty_pll.py`,
    que marca só o campo TOC (localiza o `instrText` contendo `TOC` e o
    `fldChar begin` imediatamente anterior) em vez de marcar todos os campos
    do documento, e valida com `ET.fromstring` antes de gravar.

## Replaces que não batem o count

- **`w:proofErr` do Word quebra replaces por substring** em parágrafos que ele
  reviu (típico onde há símbolos como `Kp`). Quando o count não bate, extrair a
  âncora **programaticamente pelo `paraId`** e reconstruir o parágrafo inteiro,
  em vez de transcrever o trecho como literal no script. Transcrição manual de
  âncoras longas é fonte recorrente de erro; extrair do XML sempre que possível.
- **Sumário (TOC)**: o texto das entradas fica em cache no XML. Um replace de
  título deve esperar **2 ocorrências** (título real + cache).

## Estrutura

- **Inserir parágrafo no fim do corpo**: localizar o sectPr final com
  `xml.rindex('<w:sectPr', 0, xml.rindex('</w:body>'))`. **Nunca** usar regex
  `<w:sectPr.*?</w:sectPr>\s*</w:body>` com `re.S`: o `.*?` faz o match começar
  no PRIMEIRO sectPr do documento (quebras de seção pré-textuais) e a inserção
  vai parar no começo do arquivo.
- **Sanity check de parágrafos num trecho**: usar `re.search(r'<w:p[ >]', trecho)`.
  O teste `'<w:p' in trecho` dá falso positivo com `<w:pgSz`/`<w:pgMar` do sectPr.
- **Duas tabelas adjacentes se fundem no Word** — sempre deixar um `<w:p>`
  entre tabelas consecutivas. Conferir com `xml.count('</w:tbl><w:tbl>') == 0`.

## Processo

- **Sempre regenerar a saída antes de verificar** — verificar um
  `doc_tcc_*.xml` de um run anterior bugado valida o bug, não o fix.
- **Títulos inseridos com `<w:ins>` aparecem azuis/sublinhados no Word**: é a
  cor de revisão do autor "Claude", não formatação; ficam pretos ao aceitar as
  alterações (Revisão → Aceitar). Já causou pergunta do usuário.
- **Arquivo aberto no Word bloqueia a cópia de volta ao OneDrive** ("Device or
  resource busy") — pedir para fechar; se o usuário salvou mudanças, refazer a
  edição sobre a versão salva (o Word também renumera IDs ao salvar).
