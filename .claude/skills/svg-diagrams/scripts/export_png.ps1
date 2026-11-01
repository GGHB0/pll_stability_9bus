# Exporta SVG desenhado à mão para PNG pelo Edge headless.
#
# Uso (ferramenta PowerShell, não Git Bash: pelo Bash o Edge sai sem gravar):
#   .claude\skills\svg-diagrams\scripts\export_png.ps1 assets\diagrams\figura.svg [-Scale 3] [-Out caminho.png]
#
# Lê largura/altura do viewBox, copia o SVG para C:\Temp\svgexport (caminho do
# repo com espaço/acento quebra a URL file:///), rasteriza com o fator pedido e
# grava o PNG ao lado do SVG (ou em -Out). Conferir o PNG com Read depois.
param(
    [Parameter(Mandatory = $true)][string]$Svg,
    [double]$Scale = 3,
    [string]$Out
)
$ErrorActionPreference = 'Stop'

$svgPath = (Resolve-Path $Svg).Path
if (-not $Out) { $Out = [IO.Path]::ChangeExtension($svgPath, '.png') }

$text = [IO.File]::ReadAllText($svgPath)
$m = [regex]::Match($text, 'viewBox="\s*[-\d.]+[\s,]+[-\d.]+[\s,]+([\d.]+)[\s,]+([\d.]+)\s*"')
if (-not $m.Success) { throw "viewBox não encontrado em $svgPath" }
$w = [math]::Ceiling([double]$m.Groups[1].Value)
$h = [math]::Ceiling([double]$m.Groups[2].Value)

$edge = @(
    "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe",
    "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe"
) | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $edge) { throw 'msedge.exe não encontrado' }

$tmpDir = 'C:\Temp\svgexport'
New-Item -ItemType Directory -Force $tmpDir | Out-Null
$name = [IO.Path]::GetFileNameWithoutExtension($svgPath)
$tmpSvg = Join-Path $tmpDir "$name.svg"
$tmpPng = Join-Path $tmpDir "$name.png"
Copy-Item $svgPath $tmpSvg -Force
if (Test-Path $tmpPng) { Remove-Item $tmpPng -Force }

$url = 'file:///' + ($tmpSvg -replace '\\', '/')
# Start-Process: o Edge escreve avisos inofensivos no stderr, que com
# ErrorActionPreference=Stop virariam erro na chamada direta (&).
$edgeArgs = @('--headless=new', '--disable-gpu', '--hide-scrollbars',
    "--force-device-scale-factor=$Scale", '--default-background-color=ffffffff',
    "--window-size=$w,$h", "--screenshot=$tmpPng", $url)
Start-Process -FilePath $edge -ArgumentList $edgeArgs -Wait -WindowStyle Hidden

# O Edge pode devolver antes de terminar de gravar.
for ($i = 0; $i -lt 20 -and -not (Test-Path $tmpPng); $i++) { Start-Sleep -Milliseconds 250 }
if (-not (Test-Path $tmpPng)) { throw 'Edge não gerou o PNG' }

Copy-Item $tmpPng $Out -Force
$px = "{0}x{1}" -f [int]($w * $Scale), [int]($h * $Scale)
Write-Output "OK  $Out  ($px px, viewBox ${w}x${h}, escala $Scale)"
