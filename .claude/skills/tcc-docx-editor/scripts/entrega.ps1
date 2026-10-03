# entrega.ps1 — entrega o DOCX finalizado ao OneDrive num passo so (referencia/entrega.md).
#
#   powershell -ExecutionPolicy Bypass -File entrega.ps1 `
#       -Final C:\Temp\tcc_<tema>\tcc_final.docx -Dest "<canonico no OneDrive>" `
#       -Md5Staging <md5 do canonico tirado no staging> [-Versao V10] [-NoReopen]
#
# POR QUE (2026-10-03): o checklist manual conferiu o MD5 com o Word aberto; ao
# fechar, o Word regravou o canonico (documento aberto pela nuvem, Saved=True)
# e o cp passou por cima sem nova checagem. Aqui a ordem e fixa:
#   1. fecha o Word pelo COM (Save() no que estiver Saved=False, depois Quit);
#      sem COM, CloseMainWindow. Nunca Stop-Process. Anota o que estava aberto;
#   2. confere que nao ha lock ~$ do canonico;
#   3. MD5 do canonico == -Md5Staging, DEPOIS do Word fechado. Divergiu ->
#      aborta (refazer a edicao sobre a versao nova, ver entrega.md);
#   4. backup datado em _backups\<Versao>\ ao lado do canonico, com MD5 conferido;
#   5. reconfere o MD5 do canonico imediatamente antes de copiar;
#   6. copia o final e confere MD5 destino == final;
#   7. reabre o canonico (e o que estava aberto), salvo -NoReopen.
# Codigo de saida 1 em qualquer aborto; nada e sobrescrito antes do passo 6.

param(
  [Parameter(Mandatory=$true)][string]$Final,
  [Parameter(Mandatory=$true)][string]$Dest,
  [Parameter(Mandatory=$true)][string]$Md5Staging,
  [string]$Versao = '',
  [switch]$NoReopen
)
$ErrorActionPreference = 'Stop'

function Md5($p) { (Get-FileHash -LiteralPath $p -Algorithm MD5).Hash.ToLower() }
function Aborta($msg) { Write-Output "ABORTADO: $msg"; exit 1 }

if (-not (Test-Path -LiteralPath $Final)) { Aborta "final nao existe: $Final" }
if (-not (Test-Path -LiteralPath $Dest))  { Aborta "canonico nao existe: $Dest" }
$Md5Staging = $Md5Staging.ToLower()

# 1. Word fechado
$abertos = @()
if (Get-Process WINWORD -ErrorAction SilentlyContinue) {
  try {
    $w = [Runtime.InteropServices.Marshal]::GetActiveObject('Word.Application')
    foreach ($d in @($w.Documents)) {
      $abertos += $d.FullName
      if (-not $d.Saved) { Write-Output "salvando antes de fechar: $($d.FullName)"; $d.Save() }
    }
    $w.Quit(0)
    [void][Runtime.InteropServices.Marshal]::ReleaseComObject($w)
  } catch {
    Write-Output "COM indisponivel ($($_.Exception.Message)); CloseMainWindow"
    Get-Process WINWORD -ErrorAction SilentlyContinue | ForEach-Object { [void]$_.CloseMainWindow() }
  }
  $t = 0
  while ((Get-Process WINWORD -ErrorAction SilentlyContinue) -and $t -lt 60) { Start-Sleep -Milliseconds 500; $t++ }
  if (Get-Process WINWORD -ErrorAction SilentlyContinue) { Aborta 'Word nao fechou em 30 s (dialogo aberto?)' }
  Write-Output "Word fechado; estavam abertos: $($abertos -join ' | ')"
  Start-Sleep -Seconds 2   # deixa o OneDrive registrar a regravacao do fechamento
}

# 2. lock
$pasta = Split-Path -LiteralPath $Dest
$nome = Split-Path -Leaf $Dest
$lock = Join-Path $pasta ('~$' + $nome.Substring(2))
if (Test-Path -LiteralPath $lock) { Aborta "lock presente: $lock" }

# 3. MD5 depois do Word fechado
$atual = Md5 $Dest
$mtime = (Get-Item -LiteralPath $Dest).LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss')
if ($atual -ne $Md5Staging) { Aborta "MD5 do canonico mudou desde o staging: $Md5Staging -> $atual (mtime $mtime)" }
Write-Output "MD5 do canonico confere com o staging: $atual"

# 4. backup
if (-not $Versao) {
  if ($nome -match '_(V\d+)') { $Versao = $Matches[1] } else { Aborta 'informe -Versao (nao achei V<n> no nome)' }
}
$dirBk = Join-Path $pasta (Join-Path '_backups' $Versao)
New-Item -ItemType Directory -Force -Path $dirBk | Out-Null
$base = [IO.Path]::GetFileNameWithoutExtension($nome)
$bk = Join-Path $dirBk ("{0}_backup_{1}.docx" -f $base, (Get-Date -Format 'yyyyMMdd_HHmmss'))
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
