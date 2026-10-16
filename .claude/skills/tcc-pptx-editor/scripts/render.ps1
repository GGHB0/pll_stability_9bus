# render.ps1 - exporta slides em PNG pelo PowerPoint (o que a banca vai ver) e monta a folha-resumo.
#
#   powershell -ExecutionPolicy Bypass -File render.ps1 -In <deck.pptx> -Out <pasta> `
#       [-Slides "3,5,12"] [-Largura 1600] [-Folha]
#
# -In      SEMPRE uma copia de trabalho (C:\Temp\defesa_<tema>\...), nunca o canonico do OneDrive
# -Slides  lista separada por virgula; padrao: todos
# -Folha   grava folha.png (4 colunas, 400x225 por slide) para ver o deck inteiro numa leitura
#
# O PowerPoint e instancia unica: o COM se pendura na sessao que o Victor tiver aberta.
# Por isso so fecha (Quit) se nao havia PowerPoint rodando antes, e abre o deck
# ReadOnly e sem janela. Nunca Stop-Process.

param(
  [Parameter(Mandatory=$true)][string]$In,
  [Parameter(Mandatory=$true)][string]$Out,
  [string]$Slides = '',
  [int]$Largura = 1600,
  [switch]$Folha
)
$ErrorActionPreference = 'Stop'
$In = (Resolve-Path -LiteralPath $In).Path
if ($In -match 'OneDrive') { Write-Output "ABORTADO: renderizar a copia de trabalho, nao o OneDrive"; exit 1 }
New-Item -ItemType Directory -Force -Path $Out | Out-Null
$Out = (Resolve-Path -LiteralPath $Out).Path

$jaRodava = [bool](Get-Process POWERPNT -ErrorAction SilentlyContinue)
$pp = New-Object -ComObject PowerPoint.Application
# Open(FileName, ReadOnly, Untitled, WithWindow)
$pres = $pp.Presentations.Open($In, -1, 0, 0)
try {
  $alto = [int]($Largura * $pres.PageSetup.SlideHeight / $pres.PageSetup.SlideWidth)
  $lista = if ($Slides) { $Slides.Split(',') | ForEach-Object { [int]$_ } } else { 1..$pres.Slides.Count }
  foreach ($n in $lista) {
    $pres.Slides.Item($n).Export((Join-Path $Out ('s{0:D2}.png' -f $n)), 'PNG', $Largura, $alto)
  }
  Write-Output "exportados $($lista.Count) slides em $Out (${Largura}x$alto)"
} finally {
  $pres.Close()
  if (-not $jaRodava -and $pp.Presentations.Count -eq 0) { $pp.Quit() }
  [void][Runtime.InteropServices.Marshal]::ReleaseComObject($pp)
}

if ($Folha) {
  Add-Type -AssemblyName System.Drawing
  $pngs = Get-ChildItem -LiteralPath $Out -Filter 's*.png' | Sort-Object Name
  $w = 400; $h = 225; $col = 4; $lin = [math]::Ceiling($pngs.Count / $col)
  $bmp = New-Object System.Drawing.Bitmap ($col * $w), ($lin * $h)
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $g.Clear([System.Drawing.Color]::White)
  $fonte = New-Object System.Drawing.Font 'Arial', 14, ([System.Drawing.FontStyle]::Bold)
  $i = 0
  foreach ($p in $pngs) {
    $img = [System.Drawing.Image]::FromFile($p.FullName)
    $x = ($i % $col) * $w; $y = [math]::Floor($i / $col) * $h
    $g.DrawImage($img, $x, $y, $w, $h); $img.Dispose()
    $g.DrawString(($p.BaseName.Substring(1)), $fonte, [System.Drawing.Brushes]::Red, ($x + 4), ($y + 4))
    $i++
  }
  $bmp.Save((Join-Path $Out 'folha.png')); $g.Dispose(); $bmp.Dispose()
  Write-Output "folha: $(Join-Path $Out 'folha.png')"
}
