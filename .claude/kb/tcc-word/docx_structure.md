# TCC Word — Estrutura OOXML e Estado do Documento

## Arquivo alvo

`TCCs Victor e Bruno_V8_revisado.docx` — na pasta OneDrive do TCC (path em config.py).
Workflow: copiar para `C:\Temp\` → editar XML → reempacotar → devolver ao OneDrive.

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

| Recurso | IDs usados | Próximo disponível |
|---|---|---|
| Bookmark IDs | 0–53 (originais) + 54, 55, 56 (Seção 3.3) | **57** |
| `w:ins` IDs | 1–20 (Seção 3.3, script gen_section33.py) | **21** |
| `pid` internos (paraId body) | 1–7 | **8** |

> Antes de inserir novos elementos, sempre buscar o maior ID existente no XML
> com grep para garantir que não há colisão com IDs do documento original.

## Estado atual — Implementado por Claude

- **Seção 3.3** — "PROTOCOLOS DE CONTINGÊNCIA E ANÁLISE DE CENÁRIOS" (tracked changes)
  - 3.3.1 Afundamento Simétrico (2 parágrafos + [TABELA 3.1])
  - 3.3.2 Afundamento Assimétrico (2 parágrafos + [TABELA 3.2])
  - ⚠️ Texto adicionado **sem acentuação** — corrigir em edição futura

> Mapa completo do documento seção a seção: `.claude/kb/tcc-word/content_map.md`

## Pendências Priorizadas

### P1 — Correções estruturais (rápidas, alto impacto)

1. **[FIGURA 3.1] sem placeholder** — referenciada 2× em 3.2.2 (§215 e §220)
   mas o placeholder não existe no texto. Inserir placeholder italic-centralizado:
   `[FIGURA 3.1 – Circuito do VSI trifásico de dois níveis com filtro LCL e blocos de controle PWM.]`
   após o parágrafo §220 (após "...é ilustrado na Figura 3.1").
2. **Estilo errado em 2.4.1/2.4.2/2.4.3** — usam `Ttulo4`, deveriam ser `Ttulo3`.
   Trocar `<w:pStyle w:val="Ttulo4"/>` → `Ttulo3` e ajustar sz/szCs=28, spacing=281.
3. **Seção sem número** — "A Necessidade das Transformadas de Referência" é `Ttulo2`
   antes de 2.1, sem numeração. Renumerar como "2.0" ou rebaixar a corpo.
   **NÃO alterar sem confirmação do Oscar/Victor.**

### P2 — Conteúdo pendente

4. **Cap. 4 quase vazio** — só títulos; 4.1.1 contém apenas ".". Prioridade do TCC.
   A redigir: 4.1.1, 4.1.2, 4.2.1, 4.3.1, 4.3.2.
   **4.2.2 (salto de fase) NÃO implementar** — instrução do Oscar.
5. **Referências MATLAB/PSIM** — Oscar comentário #9, Seção 3.1. Citar MathWorks
   (MATLAB) e Powersim Inc. ou artigo (PSIM).
6. **Acentuação da Seção 3.3** — corrigir em futura edição.

### P3 — Limpeza

7. **Figuras Cap. 2** — [FIGURA 2.1], [FIGURA 2.6] e 2 figuras ONS já têm placeholder
   de texto; substituir por imagens quando disponíveis.
8. **Lista de referências final** — mistura template UERJ + refs reais [1]–[9].
   Remover entradas do template.

### Fora de escopo (instrução do Oscar)

- Salto de fase (phase-angle jump) — não implementar
- Alto RoCoF — não implementar
- Métricas de desempenho (passo iv do Cap. 3) — pendente decisão do Oscar
