#Requires -Version 5.1
[CmdletBinding()]
param(
    [switch] $InstallCli,
    [switch] $SkipPull,
    [string] $TargetDir = (Join-Path $env:USERPROFILE ".codex\skills"),
    [string] $BinDir = (Join-Path $env:LOCALAPPDATA "Microsoft\WindowsApps"),
    [string] $PythonCommand = "python"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

if (-not $SkipPull) {
    if (-not (Test-Path -LiteralPath (Join-Path $RepoRoot ".git"))) {
        throw "This directory is not a git checkout. Clone https://github.com/indieark/indieark-skills.git first, or run with -SkipPull."
    }
    git -C $RepoRoot pull --ff-only
    if ($LASTEXITCODE -ne 0) {
        throw "git pull --ff-only failed"
    }
}

$installArgs = @(
    "-ExecutionPolicy", "Bypass",
    "-File", (Join-Path $RepoRoot "install.ps1"),
    "-TargetDir", $TargetDir,
    "-BinDir", $BinDir,
    "-PythonCommand", $PythonCommand
)
if ($InstallCli) {
    $installArgs += "-InstallCli"
}

powershell.exe @installArgs
if ($LASTEXITCODE -ne 0) {
    throw "install.ps1 failed"
}
