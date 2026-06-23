Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

$ActivateScript = Join-Path $ProjectRoot '.venv\Scripts\Activate.ps1'
if (-not (Test-Path $ActivateScript)) {
    throw "Virtual environment not found at $ActivateScript. Create it with: python -m venv .venv"
}

. $ActivateScript

Write-Host "Project root: $ProjectRoot" -ForegroundColor Cyan
Write-Host "Python: $(Get-Command python).Source" -ForegroundColor Cyan
Write-Host "Use 'python app.py' from here." -ForegroundColor Green
