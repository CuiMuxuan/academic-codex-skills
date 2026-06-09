$ErrorActionPreference = 'Stop'

# Install the academic skills into a Claude Code home (~/.claude) so they can
# coexist with the primary Codex installation produced by install.ps1.
# The shared/ folder is installed one level above skills/ so that the
# ../../shared/ relative links inside each SKILL.md resolve correctly.

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$sourceSkills = Join-Path $repoRoot 'skills'
$sourceShared = Join-Path $repoRoot 'shared'
$claudeHome = Join-Path $env:USERPROFILE '.claude'
$targetSkills = Join-Path $claudeHome 'skills'
$targetShared = Join-Path $claudeHome 'shared'

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
