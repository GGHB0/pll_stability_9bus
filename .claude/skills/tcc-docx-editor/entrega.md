# Entrega ao OneDrive (passo 8 do workflow)

Continuação de `SKILL.md`. Aprendido em 2026-09-02, na marra, e ampliado
desde então.

## Checklist

1. Word fechado (`tasklist | grep -i winword`) e sem lock `~$*` na pasta.
   Se estiver aberto: fechar pelo COM, salvando (`padroes_revisao.md` §3).
2. **MD5 do OneDrive igual ao do staging.** Timestamp e bytes não bastam (o
   MD5 pegou um save do Victor 8 min depois da cópia).
3. Backup datado: `<nome>_backup_YYYYMMDD_HHMMSS.docx` em `_backups/<versão>/`
   ao lado do arquivo (`comentado/_backups/V10/`).
4. `cp` do final → `md5sum` do destino igual ao do final.
5. Reabrir o canônico no Word (`Start-Process "<path>"`).

## MD5 mudou

- **Antes da entrega**: refazer o staging e reaplicar o `gen_*.py` (ele só lê
  o XML do staging). Sync de outro aparelho (Bruno) chega em rajadas, até com
  mtime voltando: esperar parar de mudar antes de refazer (2026-10-01).
- **Depois da entrega** (o Victor salvou por cima, ou outra sessão entregou):
  não refazer nada às cegas. Conferir no arquivo atual se as edições
  entregues sobreviveram (grep de uma frase-assinatura de cada edição, contagem
  de `Feito.` no `comments.xml`). Sobreviveram → a próxima rodada parte do
  arquivo atual. Sumiram → restaurar por paraId, como em 2026-10-02 00h17
  (`historico_entregas.md`).

## Sessões em paralelo (achado em 2026-10-02)

Duas sessões do Claude editaram o V10 no mesmo dia, as duas com o staging
padrão de `config.py` (`C:\Temp\tcc_edit.docx`, `C:\Temp\doc_tcc_edit.xml`).
Uma refez o staging entre o gen e a conferência da outra. Não houve perda
porque o pré-check por MD5 segura a entrega, mas a conferência leu o XML
errado.

- **Staging por tema**: `C:\Temp\tcc_<tema>\tcc_edit.docx` e
  `doc_tcc_edit.xml` dentro da pasta, com o `gen_<tema>.py` lendo dali. Os
  paths de `config.py` ficam como padrão, para quando só houver uma sessão.
- Antes de reler o XML de staging numa rodada longa, conferir o mtime: se
  for mais novo que o seu staging, alguém mexeu.

## Por que cada regra existe

- **Word fechado**: trocar os bytes por baixo de uma sessão viva quebra o
  sincronismo do OneDrive ("CARREGAMENTO BLOQUEADO", upload recusado).
- **Nunca entregar zip montado à mão**: rodar `word_finalize.ps1` antes. O zip
  à mão abre e até exporta PDF, mas o `w:dirty` do sumário deixa o documento
  modificado ao abrir, disparando o mesmo bloqueio, e os `PAGEREF` de seções
  removidas ficam "Erro! Indicador não definido".
- **`audit_docx.py` distingue arquivo corrompido de problema de
  sincronismo**: 0 falhas quando o Word reclamar = conteúdo são, o problema é
  de upload.
