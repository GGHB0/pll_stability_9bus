---
name: tcc-mesclagem-cap45-canonico
description: Mesclagem dos Capítulos 4 e 5 do fragmento revisado para dentro do TCC canônico em 2026-09-02, com a receita técnica e o inventário do que foi descartado
metadata:
  type: project
---

# Mesclagem dos Cap. 4 e 5 no Canônico (2026-09-02)

Os Capítulos 4 e 5 de `TCC_Victor_Bruno_V9_novo_indice_2.docx` foram
**substituídos por inteiro** pelo conteúdo de `capitulos_4_5_revisados.docx`.
Decisão do usuário depois de eu apresentar o inventário de perdas abaixo.
Complementa [[tcc-revisao-fragmento-cap5]] e [[tcc-docx-content-map]].

- Blocos substituídos: **591 a 734** (do `Ttulo1` "Capítulo 4" até o `Ttulo2`
  "5.4. Resumo ou Conclusões do Capítulo"). Documento passou de 759 para 751
  blocos; 75 páginas no PDF.
- Backup: `TCC_Victor_Bruno_V9_novo_indice_2_backup_20260902_004347.docx`.

## O que foi descartado (só existia no canônico)

Repescar daqui se o Victor quiser reintroduzir. O texto integral está no
backup acima.

| Conteúdo | Onde estava |
|---|---|
| Solver e taxas (ode23t, tolerância 10⁻³, Ts/Tsc/fsw, ω_res) | abertura de 4.3.3 |
| **4.3.3.1 Modelagem Dinâmica dos Geradores Síncronos** | H₁ = 9,478 s, H₃ = 2,351 s, AVR SM AC1C, PSS1A, Governor, justificativa da inércia reduzida, KUNDUR (1994) e ANDERSON; FOUAD (2003) |
| **4.3.3.2 Topologia da Falta** | bloco Fault (Three-Phase), chaves SPST, os quatro tipos 3LG/LLG/LL/LG |
| Lista dos cinco grupos de sinais monitorados | 4.3.3.3 |
| Descrição de 4.3.4.1 / 4.3.4.2 | afundamento simétrico e assimétrico |
| **Três tabelas** | duas em 4.3.2, uma de cenários em 4.3.4.1 |
| Quatro comentários do Bruno (ids 46, 49, 51, 52) | todos no Cap. 4 |

Os comentários do Bruno pediam justamente o que o fragmento entrega ("Mudar
valores para os corretos", "Vai virar a parte do csv e do dashboard", "dar um
enfoque na parte onde fizemos os primeiros modelos no psim"). O comentário 2
(Cap. 1) sobreviveu; os quatro do Cap. 4 saíram junto com o texto que
ancoravam.

**Fica valendo:** o Cap. 4 do fragmento é mais raso que o do canônico. Se
algum dia a banca cobrar modelagem de gerador ou topologia de falta, o texto
está no backup, não perdido.

## Receita da mesclagem

O fragmento é *plain Normal* e o canônico é estilizado. Três incompatibilidades
tiveram que ser resolvidas, e nenhuma é óbvia:

### 1. Títulos sem estilo não entram no sumário

Os 117 parágrafos do fragmento têm **zero** `pStyle`: os títulos são parágrafos
comuns em negrito `w:sz` 36. Inseridos como estão, o sumário do canônico
ignora todos. O mapeamento aplicado:

| Padrão no fragmento | Estilo | `w:sz` |
|---|---|---|
| `Capítulo N: Título` | `Ttulo1` | 48 |
| `N.N Título` (1 ponto) | `Ttulo2` | 36 |
| `N.N.N` (2 pontos) | `Ttulo3` | 28 |
| `N.N.N.N` (3 pontos) | `Ttulo4` | 24 |

Também normalizado ao padrão do canônico: `Capítulo 5:` → `Capítulo 5 – ` e
ponto depois do número (`5.1` → `5.1.`). Total: 19 títulos.

### 2. A convenção de figura é invertida

| | Fragmento | Canônico |
|---|---|---|
| Legenda | **abaixo** da imagem, itálico 11 pt, "Figura 5.1 **-**" | **acima**, 12 pt normal, "Figura 4.1 **–**" |
| Fonte | não existe | "Fonte: Os autores (2026)." depois da imagem |

Cada `[IMG][legenda]` do fragmento virou `[legenda][IMG][Fonte]`, com hífen
trocado por travessão curto. São 19 figuras.

### 3. O fragmento é Carta e o TCC é A4

**Esta é a que morde em silêncio.** O fragmento foi montado em Carta com
margens de 1", área útil **6,50 in**, e as figuras didáticas usam essa largura
cheia (regra em `assets/charts/figuras_didaticas.md`). O canônico é **A4**
(`pgSz` 11907 twips, margens 1701/1134), área útil **6,30 in**. Quatro figuras
entravam estourando a margem direita em 0,20 in: as Figuras 4.1 (unifilar),
4.2 (circuito LCL), 5.11 (retenção didática) e 5.14 (potência didática).

Reescaladas para 6,30 in preservando a proporção, **mexendo em `wp:extent` E
em `a:ext`** (a armadilha já registrada em `fragmento_externo.md`: mexer só no
primeiro entrega a figura esticada). Perda de 3% na escala, sem prejuízo de
legibilidade — conferido no PDF renderizado.

Derivar a largura do próprio `sectPr` de destino, nunca assumir:

```python
UTIL_TW  = pgSz_w - pgMar_right - pgMar_left      # twips
UTIL_EMU = UTIL_TW * 635                          # 1 twip = 635 EMU
```

### 4. IDs e partes auxiliares

- **rId das imagens**: `rId101`–`rId119` (o canônico ia até `rId30`).
- **Mídia**: renomeada para `word/media/pll_imageN.png` — os dois arquivos
  tinham `image1.png`…`image11.png` e colidiriam.
- **`wp:docPr`**: `900000001`+; **`pic:cNvPr`**: `910000000`+. Conferido que os
  28 `docPr` do documento final são únicos.
- **`w14:paraId`/`textId`** dos parágrafos do fragmento foram **removidos** na
  inserção, para não colidir com os do canônico. O Word regenera ao salvar.
- **Comentários órfãos**: apagar de `comments.xml` não basta. `commentsExtended.xml`
  e `commentsIds.xml` referenciam o `paraId` do *conteúdo do comentário*, e
  ficam apontando para o vazio. Limpar as três partes. Conferir comparando os
  `paraId` dessas partes contra os de `comments.xml`, **não** contra os de
  `document.xml` (dá falso positivo: o paraId do comentário vivo não está no
  corpo).
- **Sumário**: `<w:fldChar w:fldCharType="begin" w:dirty="true"/>` no campo TOC.
  O Word reconstruiu na abertura, com as seis subseções novas de 5.1 a 5.6.

## Realces amarelos que foram junto

Os dois realces amarelos do fragmento (parágrafos 91 e 96 do fragmento, hoje
no §5.4 do TCC) são anotação do usuário marcando texto dele próprio, e
**entraram no canônico**. Decidido manter: o canônico já usa amarelo na seção
de Referências para marcar entradas "A CONFIRMAR", então a marcação não é
estranha ao documento. Ficam visíveis no corpo do Cap. 5 até alguém limpar.

## Verificação feita

XML bem-formado, 30→30 partes preservadas, 19 mídias novas, todos os `r:embed`
com relationship correspondente e alvo presente no zip, `docPr` únicos, nenhuma
imagem acima da área útil, sem em-dash. Word abriu sem prompt de reparo,
exportou 75 páginas e reconstruiu o sumário. Páginas 43, 55, 57 e 61
rasterizadas e conferidas visualmente.

## Efeito no restante do KB

`content_map.md` foi reescrito nos Cap. 4 e 5: o mapa antigo descrevia texto
que não existe mais. `revisao_fragmento_cap4.md` e os `revisao_fragmento_cap5*`
continuam válidos — descrevem o fragmento, que segue sendo a fonte.
