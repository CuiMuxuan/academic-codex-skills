param(
  [Parameter(Mandatory=$true)]
  [string]$InputPath,

  [Parameter(Mandatory=$true)]
  [string]$OutputPath,

  [switch]$Visible,
  [switch]$AllowOverwrite
)

$ErrorActionPreference = "Stop"

function Resolve-StrictPath([string]$PathValue) {
  $resolved = Resolve-Path -LiteralPath $PathValue -ErrorAction Stop
  return $resolved.Path
}

$inputFull = Resolve-StrictPath $InputPath
$outputFull = [System.IO.Path]::GetFullPath($OutputPath)

if ([System.IO.Path]::GetExtension($inputFull).ToLowerInvariant() -ne ".docx") {
  throw "Input must be a .docx file: $inputFull"
}

if ((Test-Path -LiteralPath $outputFull) -and -not $AllowOverwrite) {
  throw "Output already exists. Pass -AllowOverwrite only after explicit user confirmation: $outputFull"
}

$outputDir = [System.IO.Path]::GetDirectoryName($outputFull)
if ($outputDir -and -not (Test-Path -LiteralPath $outputDir)) {
  New-Item -ItemType Directory -Force -Path $outputDir | Out-Null
}

$word = $null
$document = $null
$report = [ordered]@{
  input = $inputFull
  output = $outputFull
  fields_updated = 0
  toc_updated = 0
  tables_of_figures_updated = 0
  tables_of_authorities_updated = 0
  indexes_updated = 0
  repaginated = $false
  warnings = @()
}

try {
  $word = New-Object -ComObject Word.Application
  $word.Visible = [bool]$Visible
  $word.DisplayAlerts = 0
  $document = $word.Documents.Open($inputFull, $false, $false)

  foreach ($story in @($document.StoryRanges)) {
    $current = $story
    while ($null -ne $current) {
      try {
        $report.fields_updated += [int]$current.Fields.Update()
      } catch {
        $report.warnings += "field_update_failed:$($_.Exception.Message)"
      }
      $current = $current.NextStoryRange
    }
  }

  foreach ($toc in @($document.TablesOfContents)) {
    try {
      $toc.Update()
      $report.toc_updated += 1
    } catch {
      $report.warnings += "toc_update_failed:$($_.Exception.Message)"
    }
  }

  foreach ($tof in @($document.TablesOfFigures)) {
    try {
      $tof.Update()
      $report.tables_of_figures_updated += 1
    } catch {
      $report.warnings += "table_of_figures_update_failed:$($_.Exception.Message)"
    }
  }

  foreach ($toa in @($document.TablesOfAuthorities)) {
    try {
      $toa.Update()
      $report.tables_of_authorities_updated += 1
    } catch {
      $report.warnings += "table_of_authorities_update_failed:$($_.Exception.Message)"
    }
  }

  foreach ($index in @($document.Indexes)) {
    try {
      $index.Update()
      $report.indexes_updated += 1
    } catch {
      $report.warnings += "index_update_failed:$($_.Exception.Message)"
    }
  }

  try {
    $document.Repaginate()
    $report.repaginated = $true
  } catch {
    $report.warnings += "repaginate_failed:$($_.Exception.Message)"
  }

  $document.SaveAs2($outputFull)
  $reportPath = [System.IO.Path]::ChangeExtension($outputFull, ".word-refresh.json")
  ($report | ConvertTo-Json -Depth 4) | Set-Content -LiteralPath $reportPath -Encoding UTF8
  Write-Output "saved=$outputFull"
  Write-Output "report=$reportPath"
} finally {
  if ($null -ne $document) {
    $document.Close($false) | Out-Null
  }
  if ($null -ne $word) {
    $word.Quit() | Out-Null
  }
  [System.GC]::Collect()
  [System.GC]::WaitForPendingFinalizers()
}
