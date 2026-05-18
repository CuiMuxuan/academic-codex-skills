$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$source = Join-Path $repoRoot 'skills'
$target = Join-Path $env:USERPROFILE '.codex\skills'

if (-not (Test-Path -LiteralPath $source)) {
    throw "Source skills folder not found: $source"
}

New-Item -ItemType Directory -Force -Path $target | Out-Null
Copy-Item -Path (Join-Path $source '*') -Destination $target -Recurse -Force

Write-Host "Installed skills to $target"
