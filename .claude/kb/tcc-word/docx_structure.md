# TCC Word — Estrutura OOXML

> **2026-09-02**: os Cap. 4 e 5 foram substituídos por inteiro (blocos 591–734
> → 117 parágrafos do fragmento). Faixas de ID novas em uso: `rId101`–`rId119`
> (imagens), `wp:docPr` a partir de `900000001`, `pic:cNvPr` a partir de
> `910000000`, mídia em `word/media/pll_imageN.png`. O documento passou de 759
> para 751 blocos, então **qualquer índice de bloco registrado abaixo para os
> Cap. 4/5 está obsoleto** — rodar `dump_headings.py` antes de usar. Receita da
> operação em [[tcc-mesclagem-cap45-canonico]]. e Estado do Documento

## Arquivo alvo

`TCC_Victor_Bruno_V9_novo_indice.docx` — na pasta OneDrive do TCC (path em
config.py da skill tcc-docx-editor, atualizado 2026-07-19).
Workflow: copiar para `C:\Temp\` → editar XML → reempacotar → devolver ao OneDrive.
Utilitários fixos de inspeção/repack (dump_headings, dump_blocks, find_text,
check_ids, repack): `.claude/skills/tcc-docx-editor/scripts/`. Divisão por
modelo em 3 níveis — Opus só para síntese; scripting no Sonnet (agente
**docx-scripter** quando a sessão roda em Opus); execução mecânica no
**docx-runner** (Haiku). Ver SKILL.md da skill.

> `TCC_Victor_Bruno_V9_novo_indice.docx` (2026-07-19) — esqueleto de títulos do novo
> índice do professor (`Indice.pdf`), gerado a partir do V9. Renumera Cap.2→3→4→5,
> insere Cap.2 novo (blecautes Ibéria/Chile/Brasil) e separa Trabalhos Futuros como
> Cap.7. Só títulos, sem parágrafo de corpo novo. Ver `project_new_toc_restructure.md`
> (memória) para o mapeamento completo antigo→novo. Numeração pura (renomeação de
> `<w:t>`) não foi marcada como tracked change — só os títulos 100% novos usam
> `<w:ins>`. Pendente: revisar em Word e decidir se vira o V9 oficial.

> **Passe de formatação (2026-07-19, mesmo arquivo)** — títulos de capítulo
> unificados para "Capítulo N – Título" (Cap.1 era "INTRODUÇÃO" sz=24, Cap.4
> era "4 CAPÍTULO – ..." sz=48; ambos agora sz=48 e mesmo padrão); subtítulos
> 4.1/4.2/4.3 de CAIXA ALTA para título normal; 2.5.1–2.5.3 e o bloco
> 3.1.1–3.1.4 (Clarke/Park/Controle Independente/Arquitetura, que estava sem
> numeração e com Ttulo3/Ttulo4 misturados, um deles com `w:numPr` de lista
> automática) corrigidos para Ttulo3 uniforme, sz=28, numeração manual e sem
> a cor legada `1B1C1D`. Mesmo tratamento aplicado a "Modulação por Largura
> de Pulso" → "3.3.1." (era o único filho sem número de 3.3). Edições diretas
> de texto/atributo, sem `<w:ins>` (mesmo trade-off da renumeração).

## Sumário (campo TOC)

O documento tem **um único índice**: o Sumário, um campo `TOC \o "1-3" \h \z \u`
(3 níveis — subseções de 4º nível como 4.2.2.1 ficam de fora, por decisão do
usuário em 2026-07-19). Não há Lista de Figuras nem Lista de Tabelas.

O texto das entradas e os números de página ficam **em cache no XML** — por isso
edições em títulos aparecem 2× num `replace` (o título real + a cópia no cache).
O cache não se atualiza sozinho e não dá para recalcular números de página sem
renderizar o documento.

**Solução:** marcar o campo como sujo — `<w:fldChar w:fldCharType="begin" w:dirty="true"/>`
— que faz o Word reconstruir o Sumário inteiro (entradas + páginas) ao abrir o
arquivo. Aplicado em 2026-07-19. Alternativa manual no Word: `Ctrl+A` → `F9`.

## Padrões XML (OOXML / Open XML)

### Tracked change — regra geral

Toda inserção usa `<w:ins>` com:
- `w:author="Claude"`
- `w:date="2026-06-14T00:00:00Z"`
- `w:id` = inteiro único e crescente no documento inteiro (ver contador abaixo)

Dois lugares por parágrafo: dentro do `<w:pPr><w:rPr>` (marca o parágrafo) e
envolvendo o(s) `<w:r>` com o conteúdo.

### Título de seção (Ttulo2 — ex.: "3.3. TÍTULO")

```xml
<w:p w14:paraId="1{bm_id:07X}" w14:textId="77777777"
     w:rsidR="00DB34AF" w:rsidRDefault="00DB34AF" w:rsidP="7211126C">
  <w:pPr>
    <w:pStyle w:val="Ttulo2"/>
    <w:autoSpaceDE w:val="0"/><w:autoSpaceDN w:val="0"/>
    <w:adjustRightInd w:val="0"/>
    <w:spacing w:before="299" w:after="299"/>
    <w:jc w:val="both"/>
    <w:rPr>
      <w:ins w:id="N" w:author="Claude" w:date="2026-06-14T00:00:00Z"/>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:sz w:val="36"/><w:szCs w:val="36"/>
      <w:lang w:val="pt-BR"/>
    </w:rPr>
  </w:pPr>
  <w:bookmarkStart w:id="{bm_id}" w:name="_Toc3_{bm_id}"/>
  <w:ins w:id="N+1" w:author="Claude" w:date="2026-06-14T00:00:00Z">
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
        <w:sz w:val="36"/><w:szCs w:val="36"/>
        <w:lang w:val="pt-BR"/>
      </w:rPr>
      <w:t>TEXTO DO TÍTULO</w:t>
    </w:r>
  </w:ins>
  <w:bookmarkEnd w:id="{bm_id}"/>
</w:p>
```

### Subtítulo (Ttulo3 — ex.: "3.3.1. Subtítulo")

Igual ao Ttulo2, mas: `pStyle="Ttulo3"`, `sz/szCs=28`, `spacing before/after=281`,
`paraId` com prefixo `2` em vez de `1`.

### Parágrafo de corpo

```xml
<w:p w14:paraId="3{pid:07X}" ...>
  <w:pPr>
    <w:autoSpaceDE w:val="0"/><w:autoSpaceDN w:val="0"/>
    <w:adjustRightInd w:val="0"/>
    <w:spacing w:before="240" w:after="240"/>
    <w:jc w:val="both"/>
    <w:rPr>
      <w:ins w:id="N" .../>
      <w:szCs w:val="24"/>
    </w:rPr>
  </w:pPr>
  <w:ins w:id="N+1" ...>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
        <w:szCs w:val="24"/>
        <w:lang w:val="pt-BR"/>
      </w:rPr>
      <w:t xml:space="preserve">Texto do parágrafo.</w:t>
    </w:r>
  </w:ins>
</w:p>
```

### Placeholder (italic centralizado — figuras/tabelas)

Igual ao corpo, mas: `jc=center`, `<w:i/>` em ambos os `<w:rPr>`, `paraId` com prefixo `4`.

## Convenções de IDs

| Campo | Regra |
|---|---|
| `paraId` | Hex de 8 dígitos, DEVE ser < `0x80000000`. Usar prefixos `1`/`2`/`3`/`4` + 7 dígitos hex do contador interno |
| `bookmarkId` | Inteiro sequencial, único no documento. Não reusar. |
| `ins w:id` | Inteiro sequencial, único no documento inteiro. Não reusar. |

## Registro de IDs usados até agora

> Registro válido para `TCC_Victor_Bruno_V9_novo_indice_2.docx` (arquivo
> canônico), medido com `check_ids.py` em 04/08/2026 sobre o XML recém-extraído.
> O Word renumera IDs a cada save do usuário — **sempre rodar `check_ids.py` no
> XML recém-extraído** antes de inserir qualquer elemento novo; registros de
> sessões anteriores não valem.

| Recurso | Estado observado (04/08, pós-edições PLL) | Próximo disponível |
|---|---|---|
| Bookmark IDs | máximo em uso = 74 (68 bookmarks) | **75** |
| Bookmarks `_Toc235351NNN` | máximo NNN = 739 | **740** |
| `w:ins` IDs | só restam ids 25–26 (título 2.6 não aceito); sem `w:del` | **27** |
| `paraId` novos (prefixo `1FB.....`) | 0x1FB00000–0x1FB00200 de sessões anteriores; **0x1FB00201–0x1FB00214** usados nas edições PLL de 04/08 (§2.3, §3.4, §4.3.2, §4.3.3, referências) + `1FB3A4B3` do Word (sempre grepar antes) | **0x1FB00215** |
| `paraId` prefixo `16xxxxxx` | 16000001–16000003, 16100001–16100008, 16200001–16200009 (bloco 4.3.3; 1620000A–C liberados na reescrita do monitoramento — não reusar) | — |

> Antes de inserir novos elementos, sempre buscar o maior ID existente no XML
> com grep para garantir que não há colisão com IDs do documento original.

## Armadilhas de edição XML

Movidas para `armadilhas_xml.md` em 2026-08-04 (limite de 200 linhas).
Ler **antes** de escrever qualquer `gen_*.py`: corrupção por `ET.write`,
`w:proofErr` quebrando replaces, sectPr final, fusão de tabelas.

## Estado atual

Última entrega: **edições PLL** (2026-08-04, 01:41), 729 → 746 blocos.
Metodologia dos ganhos do PLL no §3.4 (equações 3.18–3.20), separação
`Kp,PLL`/`Ki,PLL` contra `Kp`/`Ki` do controlador de corrente, CIGRE e
mecanismo de cycle slipping no §2.3, dois cenários de sintonia no §4.3.3,
duas etapas de modelagem no §4.3.2, e 4 referências novas.

Estado do XML de trabalho: `C:\Temp\doc_tcc_pll.xml` (662 981 bytes);
template ZIP para repack: `C:\Temp\tcc_edit.docx`; script gerador:
`C:\Temp\gen_pll_edits.py`; spec: `C:\Temp\spec_pll_edits.md`.

> Histórico completo de entregas (ANEXOS, siglas, equações, Cap.4, Oscar):
> `historico_entregas.md`
> Mapa completo do documento seção a seção: `content_map.md`
> Pendências priorizadas P1/P2/P3: `pendencias.md`
> Inventário de siglas para a lista pré-textual: `siglas_inventory.md`
