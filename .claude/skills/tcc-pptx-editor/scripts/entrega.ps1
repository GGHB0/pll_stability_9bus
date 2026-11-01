# entrega.ps1 - entrega o deck finalizado ao OneDrive num passo so (referencia/entrega.md).
#
#   powershell -ExecutionPolicy Bypass -File entrega.ps1 `
#       -Final C:\Temp\defesa_<tema>\final.pptx -Dest "<canonico no OneDrive>" `
#       -Md5Staging <md5 do canonico tirado no staging> [-NoReopen]
#
# Mesma ordem do entrega.ps1 do Word (licao de 2026-10-03: conferir o MD5 so
# DEPOIS de fechar o app, que pode regravar o arquivo ao sair):
#   1. fecha o PowerPoint pelo COM (Save() no que estiver Saved=False, depois Quit);
#      sem COM, CloseMainWindow. Nunca Stop-Process. Anota o que estava aberto;
#   2. confere que nao ha lock ~$ do canonico;
#   3. MD5 do canonico == -Md5Staging. Divergiu -> aborta (o Victor ou o Bruno
#      salvaram; refazer a edicao sobre a versao nova);
#   4. backup datado em _backups\defesa\ ao lado do canonico, MD5 conferido;
#   5. reconfere o MD5 imediatamente antes de copiar;
#   6. copia o final e confere MD5 destino == final;
#   7. reabre o canonico (e o que estava aberto), salvo -NoReopen.
# Codigo de saida 1 em qualquer aborto; nada e sobrescrito antes do passo 6.

param(
  [Parameter(Mandatory=$true)][string]$Final,
  [Parameter(Mandatory=$true)][string]$Dest,
  [Parameter(Mandatory=$true)][string]$Md5Staging,
  [switch]$NoReopen
)
$ErrorActionPreference = 'Stop'

function Md5($p) { (Get-FileHash -LiteralPath $p -Algorithm MD5).Hash.ToLower() }
function Aborta($msg) { Write-Output "ABORTADO: $msg"; exit 1 }

if (-not (Test-Path -LiteralPath $Final)) { Aborta "final nao existe: $Final" }
if (-not (Test-Path -LiteralPath $Dest))  { Aborta "canonico nao existe: $Dest" }
$Md5Staging = $Md5Staging.ToLower()

# 1. PowerPoint fechado
$abertos = @()
if (Get-Process POWERPNT -ErrorAction SilentlyContinue) {
  try {
    $pp = [Runtime.InteropServices.Marshal]::GetActiveObject('PowerPoint.Application')
    foreach ($p in @($pp.Presentations)) {
      $abertos += $p.FullName
      if (-not $p.Saved) { Write-Output "salvando antes de fechar: $($p.FullName)"; $p.Save() }
    }
    $pp.Quit()
    [void][Runtime.InteropServices.Marshal]::ReleaseComObject($pp)
  } catch {
    Write-Output "COM indisponivel ($($_.Exception.Message)); CloseMainWindow"
    Get-Process POWERPNT -ErrorAction SilentlyContinue | ForEach-Object { [void]$_.CloseMainWindow() }
  }
  # logo depois do pptx_finalize -Pdf a instancia dele ainda esta saindo e leva
  # mais de 30 s (2026-10-19, duas vezes): 90 s antes de abortar
  $t = 0
  while ((Get-Process POWERPNT -ErrorAction SilentlyContinue) -and $t -lt 180) { Start-Sleep -Milliseconds 500; $t++ }
  if (Get-Process POWERPNT -ErrorAction SilentlyContinue) { Aborta 'PowerPoint nao fechou em 90 s (dialogo aberto?)' }
  Write-Output "PowerPoint fechado; estavam abertos: $($abertos -join ' | ')"
  Start-Sleep -Seconds 2
}

# 2. lock (PowerPoint usa ~$ + nome inteiro; o Word corta 2 letras: testa os dois)
$pasta = Split-Path -LiteralPath $Dest
$nome = Split-Path -Leaf $Dest
foreach ($lk in @(('~$' + $nome), ('~$' + $nome.Substring(2)))) {
  if (Test-Path -LiteralPath (Join-Path $pasta $lk)) { Aborta "lock presente: $lk" }
}

# 3. MD5 depois do PowerPoint fechado
$atual = Md5 $Dest
$mtime = (Get-Item -LiteralPath $Dest).LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss')
if ($atual -ne $Md5Staging) { Aborta "MD5 do canonico mudou desde o staging: $Md5Staging -> $atual (mtime $mtime)" }
Write-Output "MD5 do canonico confere com o staging: $atual"

# 4. backup
$dirBk = Join-Path $pasta (Join-Path '_backups' 'defesa')
New-Item -ItemType Directory -Force -Path $dirBk | Out-Null
$base = [IO.Path]::GetFileNameWithoutExtension($nome)
$bk = Join-Path $dirBk ("{0}_backup_{1}.pptx" -f $base, (Get-Date -Format 'yyyyMMdd_HHmmss'))
Copy-Item -LiteralPath $Dest -Destination $bk
if ((Md5 $bk) -ne $atual) { Aborta "backup com MD5 diferente: $bk" }
Write-Output "backup: $bk"

# 5-6. reconfere e copia
if ((Md5 $Dest) -ne $Md5Staging) { Aborta 'canonico mudou entre o backup e a copia' }
$md5Final = Md5 $Final
try { Copy-Item -LiteralPath $Final -Destination $Dest -Force }
catch { Aborta "copia falhou ($($_.Exception.Message)); backup intacto em $bk" }
$novo = Md5 $Dest
if ($novo -ne $md5Final) { Aborta "MD5 do destino ($novo) != final ($md5Final)" }
Write-Output "entregue: $Dest  MD5 $novo"

# 7. reabre
if (-not $NoReopen) {
  $reabrir = @($Dest) + @($abertos | Where-Object { $_ -ne $Dest -and (Test-Path -LiteralPath $_) })
  foreach ($p in $reabrir) { Start-Process -FilePath $p }
  Write-Output "reaberto: $($reabrir -join ' | ')"
}
Write-Output 'OK'
