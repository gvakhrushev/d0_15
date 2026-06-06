param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $GraphifyArgs
)

$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot '..')
$GraphifyRoot = Join-Path $ProjectRoot 'tools\graphify'
$OldPythonPath = $env:PYTHONPATH
$OldPythonIoEncoding = $env:PYTHONIOENCODING
$OldPythonUtf8 = $env:PYTHONUTF8

if ($OldPythonPath) {
    $env:PYTHONPATH = "$GraphifyRoot;$OldPythonPath"
} else {
    $env:PYTHONPATH = $GraphifyRoot
}
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONUTF8 = '1'

try {
    Push-Location $ProjectRoot
    python -m graphify @GraphifyArgs
    exit $LASTEXITCODE
}
finally {
    Pop-Location
    $env:PYTHONPATH = $OldPythonPath
    $env:PYTHONIOENCODING = $OldPythonIoEncoding
    $env:PYTHONUTF8 = $OldPythonUtf8
}
