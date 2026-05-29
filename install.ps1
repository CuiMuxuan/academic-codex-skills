$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$sourceSkills = Join-Path $repoRoot 'skills'
$sourceShared = Join-Path $repoRoot 'shared'
$targetSkills = Join-Path $env:USERPROFILE '.codex\skills'
$targetShared = Join-Path $env:USERPROFILE '.codex\shared'

if (-not (Test-Path -LiteralPath $sourceSkills)) {
    throw "Source skills folder not found: $sourceSkills"
}

New-Item -ItemType Directory -Force -Path $targetSkills | Out-Null

$skillDirs = Get-ChildItem -LiteralPath $sourceSkills -Directory
foreach ($skill in $skillDirs) {
    $destination = Join-Path $targetSkills $skill.Name
    if (Test-Path -LiteralPath $destination) {
        Remove-Item -LiteralPath $destination -Recurse -Force
    }
    Copy-Item -LiteralPath $skill.FullName -Destination $destination -Recurse -Force
    Write-Host "Installed skill: $($skill.Name)"
}

if (Test-Path -LiteralPath $sourceShared) {
    New-Item -ItemType Directory -Force -Path $targetShared | Out-Null
    Get-ChildItem -LiteralPath $sourceShared -File | ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $targetShared $_.Name) -Force
        Write-Host "Installed shared file: $($_.Name)"
    }
}

Write-Host "Installed skills to $targetSkills"
Write-Host "Installed shared protocols to $targetShared"
