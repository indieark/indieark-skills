#Requires -Version 5.1
[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string] $TargetDir = (Join-Path $env:USERPROFILE ".codex\skills"),
    [switch] $InstallCli,
    [string] $BinDir = (Join-Path $env:LOCALAPPDATA "Microsoft\WindowsApps"),
    [string] $PythonCommand = "python"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$ManifestPath = Join-Path $RepoRoot "manifest.json"

function Read-JsonFile([string] $Path) {
    if (-not (Test-Path -LiteralPath $Path)) {
        throw "Missing manifest: $Path"
    }
    return Get-Content -LiteralPath $Path -Raw -Encoding UTF8 | ConvertFrom-Json
}

function Assert-Skill([object] $Skill) {
    $skillPath = Join-Path $RepoRoot $Skill.path
    foreach ($required in @("SKILL.md", "skill.json")) {
        $path = Join-Path $skillPath $required
        if (-not (Test-Path -LiteralPath $path)) {
            throw "Missing $required for $($Skill.name): $path"
        }
    }
    foreach ($cli in @($Skill.cli)) {
        $entry = Join-Path $skillPath $cli.entrypoint
        if (-not (Test-Path -LiteralPath $entry)) {
            throw "Missing CLI entrypoint for $($Skill.name): $entry"
        }
    }
}

function Install-Skill([object] $Skill) {
    $source = Join-Path $RepoRoot $Skill.path
    $target = Join-Path $TargetDir $Skill.name
    Assert-Skill $Skill
    if ($PSCmdlet.ShouldProcess($target, "Install $($Skill.name)")) {
        New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null
        if (Test-Path -LiteralPath $target) {
            Remove-Item -LiteralPath $target -Recurse -Force
        }
        Copy-Item -LiteralPath $source -Destination $target -Recurse -Force
    }
}

function Install-CliWrapper([object] $Skill, [object] $Cli) {
    $entry = Join-Path (Join-Path $TargetDir $Skill.name) $Cli.entrypoint
    $wrapper = Join-Path $BinDir $Cli.wrapper
    if (-not (Test-Path -LiteralPath $entry)) {
        throw "Cannot create CLI wrapper; installed entrypoint is missing: $entry"
    }
    if ($PSCmdlet.ShouldProcess($wrapper, "Install CLI wrapper $($Cli.name)")) {
        New-Item -ItemType Directory -Force -Path $BinDir | Out-Null
        $content = "@echo off`r`n$PythonCommand `"$entry`" %*`r`n"
        Set-Content -LiteralPath $wrapper -Value $content -Encoding ASCII
    }
}

$manifest = Read-JsonFile $ManifestPath

foreach ($skill in @($manifest.skills)) {
    Install-Skill $skill
}

if ($InstallCli) {
    foreach ($skill in @($manifest.skills)) {
        foreach ($cli in @($skill.cli)) {
            Install-CliWrapper $skill $cli
        }
    }
}

Write-Host "Installed $(@($manifest.skills).Count) skills to $TargetDir"
if ($InstallCli) {
    Write-Host "CLI wrappers installed to $BinDir"
}
