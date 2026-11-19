$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$sourceRoot = Join-Path $repoRoot 'source'
$outRoot = Join-Path $repoRoot 'build\out'
$mutex = [Threading.Mutex]::new($false, 'Global\InterlanguageTeXSlotV1')
$acquired = $false
try {
  $acquired = $mutex.WaitOne(300000)
  if (-not $acquired) { throw 'Timed out waiting for Global\InterlanguageTeXSlotV1.' }
  New-Item -ItemType Directory -Force -Path $outRoot | Out-Null
  Push-Location $sourceRoot
  try {
    $env:SOURCE_DATE_EPOCH = '1788825600'
    $env:TZ = 'UTC'
    foreach ($pass in 1..4) {
      & xelatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=$outRoot main.tex
      if ($LASTEXITCODE -ne 0) { throw "XeLaTeX failed on pass $pass." }
      Copy-Item -LiteralPath (Join-Path $outRoot 'main.pdf') -Destination (Join-Path $outRoot "main.pass$pass.pdf")
    }
    $p3 = (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $outRoot 'main.pass3.pdf')).Hash
    $p4 = (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $outRoot 'main.pass4.pdf')).Hash
    if ($p3 -cne $p4) { throw 'Passes 3 and 4 are not byte-identical.' }
  } finally { Pop-Location }
} finally {
  if ($acquired) { $mutex.ReleaseMutex() }
  $mutex.Dispose()
}
