#Requires -Version 5.1
[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string] $SourceRoot = (Join-Path (Split-Path -Parent $PSScriptRoot) "skills"),
    [switch] $SkipValidation
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = $PSScriptRoot
$ManifestPath = Join-Path $RepoRoot "manifest.json"
$manifest = Get-Content -LiteralPath $ManifestPath -Raw -Encoding UTF8 | ConvertFrom-Json

$excludedDirs = @(".git", "_work", "dist", "extensions", "__pycache__", ".pytest_cache")
$excludedExtensions = @(".pyc", ".pyo")
$excludedArchiveExtensions = @(".zip", ".tar", ".tgz", ".rar", ".7z", ".gz")

function Copy-RuntimeSkill([object] $Skill) {
    $source = Join-Path (Split-Path -Parent $RepoRoot) $Skill.source
    if (-not (Test-Path -LiteralPath $source)) {
        $source = Join-Path $SourceRoot ($Skill.source -replace "^skills[\\/]", "")
    }
    if (-not (Test-Path -LiteralPath $source)) {
        throw "Missing source for $($Skill.name): $source"
    }

    $target = Join-Path $RepoRoot $Skill.path
    if ($PSCmdlet.ShouldProcess($target, "Refresh $($Skill.name) from $source")) {
        if (Test-Path -LiteralPath $target) {
            Remove-Item -LiteralPath $target -Recurse -Force
        }
        Copy-Item -LiteralPath $source -Destination $target -Recurse -Force
    }
}

function Get-SkillRoots {
    foreach ($skill in @($manifest.skills)) {
        Join-Path $RepoRoot $skill.path
    }
}

function Remove-ExcludedFiles {
    foreach ($root in Get-SkillRoots) {
        if (-not (Test-Path -LiteralPath $root)) {
            continue
        }
        foreach ($dirName in $excludedDirs) {
            Get-ChildItem -LiteralPath $root -Directory -Recurse -Force |
            Where-Object { $_.Name -eq $dirName } |
            ForEach-Object { Remove-Item -LiteralPath $_.FullName -Recurse -Force }
        }

        Get-ChildItem -LiteralPath $root -File -Recurse -Force |
        Where-Object {
            $excludedExtensions -contains $_.Extension.ToLowerInvariant() -or
            $excludedArchiveExtensions -contains $_.Extension.ToLowerInvariant() -or
            $_.Name.EndsWith(".tar.gz", [StringComparison]::OrdinalIgnoreCase)
        } |
        ForEach-Object { Remove-Item -LiteralPath $_.FullName -Force }
    }
}

function Assert-Distribution {
    foreach ($skill in @($manifest.skills)) {
        $skillPath = Join-Path $RepoRoot $skill.path
        foreach ($required in @("SKILL.md", "skill.json")) {
            $path = Join-Path $skillPath $required
            if (-not (Test-Path -LiteralPath $path)) {
                throw "Missing $required for $($skill.name): $path"
            }
        }
        foreach ($cli in @($skill.cli)) {
            $entry = Join-Path $skillPath $cli.entrypoint
            if (-not (Test-Path -LiteralPath $entry)) {
                throw "Missing CLI entrypoint for $($skill.name): $entry"
            }
        }
    }

    foreach ($root in Get-SkillRoots) {
        $badDir = Get-ChildItem -LiteralPath $root -Directory -Recurse -Force |
            Where-Object { $excludedDirs -contains $_.Name } |
            Select-Object -First 1
        if ($badDir) {
            throw "Excluded directory remains: $($badDir.FullName)"
        }

        $badFile = Get-ChildItem -LiteralPath $root -File -Recurse -Force |
            Where-Object {
                $excludedExtensions -contains $_.Extension.ToLowerInvariant() -or
                $excludedArchiveExtensions -contains $_.Extension.ToLowerInvariant() -or
                $_.Name.EndsWith(".tar.gz", [StringComparison]::OrdinalIgnoreCase)
            } |
            Select-Object -First 1
        if ($badFile) {
            throw "Excluded file remains: $($badFile.FullName)"
        }
    }
}

foreach ($skill in @($manifest.skills)) {
    Copy-RuntimeSkill $skill
}

Remove-ExcludedFiles

if (-not $SkipValidation) {
    Assert-Distribution
}

Write-Host "Distribution refreshed: $RepoRoot"
