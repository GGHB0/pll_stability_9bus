# Skill: tcc-docx-editor

Edita o TCC DOCX (arquivo atual definido em `config.py` — hoje
`TCC_Victor_Bruno_V9_novo_indice.docx`) com tracked changes rastreáveis
no Word. Usa bash para copiar de/para o OneDrive (que tem lock), e `python.exe` para
manipular o XML (python não enxerga o VFS do Claude Desktop, só o Windows path real).

## Dependências

- `C:\projetos\pll_stability_9bus\.claude\skills\tcc-docx-editor\config.py` — paths pessoais (gitignored)
- `C:\projetos\pll_stability_9bus\.claude\skills\tcc-docx-editor\helpers.py` — funções XML
- A skill `slx-explorer` (ou equivalente) que provê `scripts/office/pack.py` e `scripts/office/unpack.py`

## Workflow padrão

```
1. Copiar DOCX para C:\Temp\          (bash — evita lock do OneDrive)
2. Desempacotar o ZIP/OOXML           (bash via python scripts/office/unpack.py)
3. Copiar document.xml para C:\Temp\  (bash — python.exe não acessa VFS)
4. Editar XML via Python              (python.exe C:\Temp\gen_*.py)
5. Copiar XML modificado de volta     (bash)
6. Reempacotar                        (bash via scripts/office/pack.py --validate false)
7. Copiar DOCX final ao OneDrive      (bash cp)
```

## Notas críticas

- **VFS isolation**: o `python.exe` do Windows NÃO consegue acessar o path
  `/c/Users/victo/AppData/Roaming/Claude/...` onde o bash desempacota o DOCX.
  Sempre copiar o XML para `C:\Temp\` antes de processar com python, e copiar de volta.
- **--validate false**: o `pack.py` usa `print()` com caracteres `→` que falham em
  cp1252. Sempre passar `--validate false` para evitar o crash do validador.
- **OneDrive lock**: não editar diretamente no path do OneDrive. Copiar para C:\Temp primeiro.
  A cópia de VOLTA também falha se o documento estiver aberto no Word do usuário
  ("Device or resource busy") — pedir para fechar antes do passo 7.
- **paraId**: máximo `0x7FFFFFFF`. Nunca usar prefixos A/B/C/D (overflow).
- **Word renumera IDs ao salvar**: se o usuário abriu e salvou o DOCX no Word,
  o registro de IDs do KB fica obsoleto — sempre grepar o XML atual antes de inserir.
- **PowerShell 5.1 + `python -c` inline quebra** com regex contendo `[...]`
  (parser do PS interpreta como tipo). Escrever scripts em `C:\Temp\*.py` e rodar o arquivo.

## Referência de IDs e armadilhas XML

Ver `.claude/kb/tcc-word/docx_structure.md` — tabela de IDs usados/próximos
disponíveis e seção "Armadilhas de edição XML" (sectPr final via `rindex`,
falso positivo `<w:p` vs `<w:pgSz`, cor azul de tracked change etc.).

## Comandos de exemplo

```bash
# 1. Copiar DOCX para temp
cp "/c/Users/victo/OneDrive/.../TCCs Victor e Bruno_V8_revisado.docx" /c/Temp/tcc_edit.docx

# 2. Desempacotar (dentro de uma sessão de skill com os scripts disponíveis)
python scripts/office/unpack.py /c/Temp/tcc_edit.docx /c/Temp/unpacked_tcc/

# 3. Copiar XML para edição
cp /c/Temp/unpacked_tcc/word/document.xml /c/Temp/doc_tcc_edit.xml

# 4. Rodar script de edição
python.exe C:\Temp\gen_minha_secao.py

# 5. Copiar XML modificado de volta
cp /c/Temp/doc_tcc_modified.xml /c/Temp/unpacked_tcc/word/document.xml

# 6. Reempacotar
python scripts/office/pack.py /c/Temp/unpacked_tcc/ /c/Temp/tcc_revisado.docx \
  --original /c/Temp/tcc_edit.docx --validate false

# 7. Devolver ao OneDrive
cp /c/Temp/tcc_revisado.docx "/c/Users/victo/OneDrive/.../TCCs Victor e Bruno_V8_revisado.docx"
```
