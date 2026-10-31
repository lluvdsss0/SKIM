$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$skimPython = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python313\python.exe'
Write-Host 'SKIM: http://127.0.0.1:8000 — Ctrl+C to stop'
if (Test-Path -LiteralPath $skimPython) {
    & $skimPython -m http.server 8000 --bind 127.0.0.1
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    py -3 -m http.server 8000 --bind 127.0.0.1
} else {
    python -m http.server 8000 --bind 127.0.0.1
}
