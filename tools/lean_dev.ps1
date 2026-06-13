param(
  [Parameter(ValueFromRemainingArguments = $true)]
  [string[]] $LakeArgs
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$LeanDir = Join-Path $RepoRoot "09_LEAN_FORMALIZATION"

if (-not (Test-Path -LiteralPath $LeanDir -PathType Container)) {
  throw "Lean package directory not found: $LeanDir"
}

$DefaultCacheRoot = Join-Path $HOME ".d0_lean_cache\D0_v14\09_LEAN_FORMALIZATION"
$CacheRoot = if ($env:D0_LEAN_CACHE_ROOT) { $env:D0_LEAN_CACHE_ROOT } else { $DefaultCacheRoot }
$ExternalLake = Join-Path $CacheRoot ".lake"
$LocalLake = Join-Path $LeanDir ".lake"

New-Item -ItemType Directory -Force -Path $ExternalLake | Out-Null

if (Test-Path -LiteralPath $LocalLake) {
  $Item = Get-Item -LiteralPath $LocalLake -Force
  if (($Item.Attributes -band [IO.FileAttributes]::ReparsePoint) -eq 0) {
    throw "Refusing to use real in-project .lake: $LocalLake. Move/delete it, then rerun this script."
  }
} else {
  New-Item -ItemType Junction -Path $LocalLake -Target $ExternalLake | Out-Null
}

if (-not $LakeArgs -or $LakeArgs.Count -eq 0) {
  Write-Host "Lean package: $LeanDir"
  Write-Host "External Lake storage: $ExternalLake"
  Write-Host ""
  Write-Host "Usage:"
  Write-Host "  .\tools\lean_dev.ps1 --version"
  Write-Host "  .\tools\lean_dev.ps1 build D0.Core.Phi"
  Write-Host "  .\tools\lean_dev.ps1 build D0.TheoremLedger.ClosedVacuumFeedbackIndex"
  Write-Host ""
  Write-Host "No build was started. Pass explicit lake arguments to run Lean."
  exit 0
}

Write-Host "Lean package: $LeanDir"
Write-Host "External Lake storage: $ExternalLake"

# Native command stderr (lake/elan 'info:' progress) must NOT abort the script:
# PowerShell's Stop preference wraps native stderr as a terminating error. Switch to
# Continue for the native calls and rely on $LASTEXITCODE for success/failure.
$ErrorActionPreference = "Continue"

# One-time: fetch precompiled mathlib oleans so mathlib is never recompiled from
# source (~minutes vs ~1 hour). Idempotent: only runs when the cache is absent.
$MathlibLib = Join-Path $ExternalLake "packages\mathlib\.lake\build\lib"
$IsCacheCmd = ($LakeArgs -contains "cache")
if (-not $IsCacheCmd -and -not (Test-Path -LiteralPath $MathlibLib)) {
  Write-Host "Mathlib build cache missing -> 'lake exe cache get' (one-time, minutes)..."
  Push-Location $LeanDir
  try { & lake exe cache get } finally { Pop-Location }
}

Write-Host "lake $($LakeArgs -join ' ')"
Push-Location $LeanDir
try {
  & lake @LakeArgs
  $code = $LASTEXITCODE
} finally {
  Pop-Location
}
exit $code
