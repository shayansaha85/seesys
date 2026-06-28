$ErrorActionPreference = "Stop"

# TODO: Replace with your actual GitHub username/repo
$Repo = "shayansaha85/seesys"
$AppName = "seesys"
$ExeName = "$AppName.exe"

Write-Host "Installing $AppName..."

$ApiUrl = "https://api.github.com/repos/$Repo/releases/latest"
try {
    $Release = Invoke-RestMethod -Uri $ApiUrl
    $Asset = $Release.assets | Where-Object { $_.name -eq "$AppName-windows.exe" }
} catch {
    Write-Error "Could not fetch release info from $Repo. Have you created a GitHub Release?"
    exit 1
}

if (-not $Asset) {
    Write-Error "Could not find Windows release asset."
    exit 1
}

$InstallDir = "$env:LOCALAPPDATA\Programs\$AppName"
if (-not (Test-Path $InstallDir)) {
    New-Item -ItemType Directory -Path $InstallDir | Out-Null
}

$DestPath = Join-Path $InstallDir $ExeName

Write-Host "Downloading $AppName..."
Invoke-WebRequest -Uri $Asset.browser_download_url -OutFile $DestPath

$UserPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($UserPath -notmatch [regex]::Escape($InstallDir)) {
    Write-Host "Adding $InstallDir to PATH..."
    $NewPath = $UserPath + ";$InstallDir"
    [Environment]::SetEnvironmentVariable("Path", $NewPath, "User")
    Write-Host "Please restart your PowerShell terminal for the PATH changes to take effect."
}

Write-Host "$AppName successfully installed! You can now run it by typing '$AppName'."
