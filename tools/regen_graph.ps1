<#
.SYNOPSIS
  Regenerate the D0 theory view + graph from the canonical CLAIM_TO_LEAN_MAP.csv,
  with claim-count delta sanity. The theory_status_map.csv / theory_graph.* /
  index markdowns are GENERATED artifacts - never hand-edit them.

.PARAMETER CheckOnly
  Regenerate, assert the committed generated files are already up to date
  (idempotence), then restore the working tree. Used by CI. Fails if stale.

.PARAMETER AllowShrink
  Max permitted drop in summary.claims vs the committed graph (default 0).
#>
param(
  [switch]$CheckOnly,
  [int]$AllowShrink = 0
)
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$graphPath = "03_THEORY_MAP/theory_graph.json"
$generated = @(
  "03_THEORY_MAP/theory_status_map.csv",
  "03_THEORY_MAP/theory_graph.json",
  "03_THEORY_MAP/theory_graph.dot",
  "03_THEORY_MAP/theory_graph.html",
  "03_THEORY_MAP/theory_semantic_index.md",
  "09_LEAN_FORMALIZATION/docs/LEAN_CORE_THEOREM_INDEX.md"
)

function Get-Claims($jsonText) {
  try { return ([int]((ConvertFrom-Json $jsonText).summary.claims)) } catch { return -1 }
}

# Previous (committed) claim count, if the graph is tracked.
$prevClaims = -1
$prevText = (git show "HEAD:$graphPath" 2>$null) | Out-String
if ($prevText.Trim().Length -gt 0) { $prevClaims = Get-Claims $prevText }

Write-Host "Regenerating theory view + graph from canonical CLAIM_TO_LEAN_MAP.csv ..."
python tools/sync_theory_status_map.py
if ($LASTEXITCODE -ne 0) { Write-Host "sync_theory_status_map.py FAILED"; exit 2 }

# Best-effort code-knowledge graph refresh (graphify-out/ is gitignored).
if (Test-Path "tools/graphify_d0.ps1") {
  try { & "tools/graphify_d0.ps1" update . | Out-Null } catch { Write-Host "graphify refresh skipped: $_" }
}

$newClaims = Get-Claims ((Get-Content $graphPath -Raw))
Write-Host "claims: previous=$prevClaims  new=$newClaims  (allow-shrink=$AllowShrink)"
if ($prevClaims -ge 0 -and $newClaims -lt ($prevClaims - $AllowShrink)) {
  Write-Host "DELTA SANITY FAIL: claims dropped $prevClaims -> $newClaims beyond tolerance"
  if ($CheckOnly) { git checkout -- $generated 2>$null }
  exit 1
}

if ($CheckOnly) {
  $dirty = (git status --porcelain -- $generated) | Where-Object { $_.Trim().Length -gt 0 }
  git checkout -- $generated 2>$null
  if ($dirty) {
    Write-Host "IDEMPOTENCE FAIL: generated artifacts were stale/hand-edited:"
    $dirty | ForEach-Object { Write-Host "  $_" }
    exit 1
  }
  Write-Host "RESULT: PASS (generated artifacts up to date)"
  exit 0
}

Write-Host "RESULT: regenerated. Review and commit the generated artifacts."
exit 0
