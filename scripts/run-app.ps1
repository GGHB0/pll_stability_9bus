Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $ProjectRoot '.venv\Scripts\python.exe'

if (-not (Test-Path $Python)) {
    throw "Python not found at $Python. Create the virtual environment first."
}

Set-Location $ProjectRoot
& $Python (Join-Path $ProjectRoot 'app.py') @args
