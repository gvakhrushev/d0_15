$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$LocalLake = Join-Path $RepoRoot "09_LEAN_FORMALIZATION\.lake"

if (-not (Test-Path -LiteralPath $LocalLake)) {
  Write-Host "PASS_LEAN_STORAGE_HYGIENE no .lake present"
  exit 0
}

$Item = Get-Item -LiteralPath $LocalLake -Force
if (($Item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
  Write-Host "PASS_LEAN_STORAGE_HYGIENE .lake is external junction/symlink"
  exit 0
}

Write-Host "FAIL_LEAN_STORAGE_HYGIENE real in-project .lake directory found: $LocalLake"
exit 1
