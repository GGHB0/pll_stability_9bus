# word_finalize.ps1 — passa o DOCX pelo proprio Word antes da entrega.
#
#   powershell -ExecutionPolicy Bypass -File word_finalize.ps1 `
#       -In C:\Temp\tcc_montado.docx -Out C:\Temp\tcc_final.docx [-Pdf C:\Temp\tcc.pdf]
#
# POR QUE (2026-09-02): um DOCX montado a mao abria, exportava PDF e passava na
# auditoria estrutural, mas o Word recusava o upload para o OneDrive
# ("CARREGAMENTO BLOQUEADO — nao e possivel salvar todas as novas alteracoes").
# Nao era corrupcao: o campo TOC marcado dirty deixava o documento modificado
# assim que abria. Passar pelo Word resolve isso e mais tres coisas de uma vez:
#
#   1. reconstroi o sumario, entao some o prompt de atualizacao de campos
#      E somem os PAGEREF apontando para bookmarks de secoes removidas
#      (que virariam "Erro! Indicador nao definido");
#   2. zera w:dirty;
#   3. descarta midia orfa de blocos apagados;
#   4. regrava o OOXML no formato canonico do Word, no lugar do zip montado a mao.
#
# Ao final PROVA que o Word consegue SALVAR (nao so abrir) — foi essa checagem
# que confirmou que a condicao de "nao e possivel salvar" tinha ido embora.
# Rodar audit_docx.py no -Out depois disso. Ver mesclagem_no_canonico.md.

#
# -Comments <arquivo.json> (opcional): lista [{"anchor": "...", "text": "..."}].
# O Word ancora um comentario no trecho exato "anchor" (<= 255 caracteres, uma
# ocorrencia so), com o texto prefixado por "[Claude] ". Usado para trecho que o usuario ainda vai
# aprovar no Word (ex.: espelho em ingles do Resumo). Feito pelo Word e nao a mao
# porque comentario mexe em 4 partes do pacote (comments, commentsIds,
# commentsExtended, commentsExtensible). O autor sai como a conta logada no
# Office (o Word ignora Application.UserName), dai o prefixo no texto.

param(
  [Parameter(Mandatory=$true)][string]$In,
  [Parameter(Mandatory=$true)][string]$Out,
  [string]$Pdf = "",
  [string]$Comments = ""
)

$ErrorActionPreference = "Stop"
$In  = (Resolve-Path $In).Path
if (Test-Path $Out) { Remove-Item $Out -Force }

# o Word aberto segura o arquivo e invalida a sessao do OneDrive
$viv = Get-Process winword -ErrorAction SilentlyContinue
if ($viv) { throw "Word esta aberto (PID $($viv.Id -join ',')). Fechar antes de finalizar." }

$w = New-Object -ComObject Word.Application
$w.Visible = $false
$w.DisplayAlerts = 0
try {
  $d = $w.Documents.Open($In, $false, $false)

  if ($Comments -ne "") {
    $lista = Get-Content $Comments -Raw -Encoding UTF8 | ConvertFrom-Json
    foreach ($c in $lista) {
      $r = $d.Content
      $r.Find.ClearFormatting()
      if (-not $r.Find.Execute($c.anchor, $true)) { throw "ancora nao encontrada: $($c.anchor)" }
      $d.Comments.Add($r, "[Claude] " + $c.text) | Out-Null
      "comentario   : +1 em '" + $c.anchor.Substring(0, [Math]::Min(50, $c.anchor.Length)) + "...'"
    }
  }

  $d.Fields.Update() | Out-Null
  # listas de figuras/quadros/graficos (TOC \c) e sumario, duas voltas: a lista
  # pode crescer uma folha e empurrar os numeros de pagina do sumario
  for ($k = 0; $k -lt 2; $k++) {
    foreach ($t in $d.TablesOfFigures)  { $t.Update() | Out-Null }
    foreach ($t in $d.TablesOfContents) { $t.Update() | Out-Null }
  }

  $d.SaveAs2($Out, 12)          # 12 = wdFormatXMLDocument
  if ($Pdf -ne "") { $d.ExportAsFixedFormat($Pdf, 17) }

  "paginas      : " + $d.ComputeStatistics(2)
  "palavras     : " + $d.ComputeStatistics(0)
  "campos       : " + $d.Fields.Count
  "figuras      : " + $d.InlineShapes.Count
  "comentarios  : " + $d.Comments.Count

  # campos que ficaram sem alvo aparecem como "Erro!" no resultado
  $err = 0
  foreach ($f in $d.Fields) { if ($f.Result.Text -match 'Erro!|Error!') { $err++ } }
  "campos c/ erro: $err"

  # prova de que o Word SALVA o arquivo, nao so abre
  $d.Saved = $false
  $d.Save()
  "SALVOU sem erro"

  $d.Close(0)
} finally {
  $w.Quit()
}

"saida        : $Out  ($((Get-Item $Out).Length) bytes)"
"proximo passo: python.exe audit_docx.py `"$Out`""
