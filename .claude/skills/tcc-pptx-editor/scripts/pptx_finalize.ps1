# pptx_finalize.ps1 - passa o deck montado pelo PowerPoint: prova que abre sem reparo e regrava.
#
#   powershell -ExecutionPolicy Bypass -File pptx_finalize.ps1 -In <montado.pptx> -Out <final.pptx> [-Pdf]
#
# Arquivo que o python-pptx gravou pode abrir no python e mesmo assim cair no
# "O PowerPoint encontrou um problema no conteudo... Reparar" (rel orfa, id de
# forma duplicado). Sem janela, esse caso vira excecao no Open: ABORTADO.
# -Pdf grava <final>.pdf ao lado (copia de seguranca para a defesa, sem depender de fonte).
# Mesma regra do render.ps1: so da Quit se nao havia PowerPoint rodando antes.

param(
  [Parameter(Mandatory=$true)][string]$In,
  [Parameter(Mandatory=$true)][string]$Out,
  [switch]$Pdf
)
$ErrorActionPreference = 'Stop'
$In = (Resolve-Path -LiteralPath $In).Path
if ($Out -match 'OneDrive') { Write-Output "ABORTADO: -Out vai para a pasta de trabalho; OneDrive so pelo entrega.ps1"; exit 1 }
$Out = [IO.Path]::GetFullPath($Out)

$jaRodava = [bool](Get-Process POWERPNT -ErrorAction SilentlyContinue)
$pp = New-Object -ComObject PowerPoint.Application
try {
  try { $pres = $pp.Presentations.Open($In, 0, 0, 0) }
  catch { Write-Output "ABORTADO: PowerPoint nao abriu o arquivo ($($_.Exception.Message))"; exit 1 }
  $n = $pres.Slides.Count
  $pres.SaveAs($Out, 24)          # ppSaveAsOpenXMLPresentation
  if ($Pdf) {
    $pdfPath = [IO.Path]::ChangeExtension($Out, '.pdf')
    $pres.SaveAs($pdfPath, 32)    # ppSaveAsPDF
    Write-Output "pdf: $pdfPath"
  }
  $pres.Close()
  Write-Output "final: $Out ($n slides, $((Get-Item -LiteralPath $Out).Length) bytes)"
  Write-Output "MD5 $((Get-FileHash -LiteralPath $Out -Algorithm MD5).Hash.ToLower())"
  Write-Output 'OK'
} finally {
  if (-not $jaRodava -and $pp.Presentations.Count -eq 0) { $pp.Quit() }
  [void][Runtime.InteropServices.Marshal]::ReleaseComObject($pp)
}
