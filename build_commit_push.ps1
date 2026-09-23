$ErrorActionPreference = "Stop"

$msbuildPath = "C:\Program Files\Microsoft Visual Studio\2022\Community\MSBuild\Current\Bin\MSBuild.exe"
if (-not (Test-Path $msbuildPath)) {
    Write-Error "MSBuild.exe not found at $msbuildPath"
}

Write-Host "Bumping version number..."
$resPath = "src\Resource.h"
$resContent = Get-Content $resPath -Raw
$verMajor = [regex]::Match($resContent, "#define VER_MAJOR\s+(\d+)").Groups[1].Value
$verMinor = [regex]::Match($resContent, "#define VER_MINOR\s+(\d+)").Groups[1].Value
$verBuild = [regex]::Match($resContent, "#define VER_BUILD\s+(\d+)").Groups[1].Value
$verRevision = [regex]::Match($resContent, "#define VER_REVISION\s+(\d+)").Groups[1].Value

$newMinor = [int]$verMinor + 1
$newBuild = [int]$verBuild + 1
$newRevision = [int]$verRevision + 1

$resContent = $resContent -replace '(#define VER_MINOR\s+)\d+', ('${1}' + $newMinor)
$resContent = $resContent -replace '(#define VER_BUILD\s+)\d+', ('${1}' + $newBuild)
$resContent = $resContent -replace '(#define VER_REVISION\s+)\d+', ('${1}' + $newRevision)

Set-Content -Path $resPath -Value $resContent -NoNewline
$version = "$verMajor.$newMinor.$newBuild.$newRevision"
Write-Host "Bumped version to $version"

Write-Host "Building NTMU.sln (Release|x64)..."
& $msbuildPath "NTMU.sln" /p:Configuration=Release /p:Platform=x64
if ($LASTEXITCODE -ne 0) {
    Write-Error "Build failed!"
    exit $LASTEXITCODE
}

Write-Host "Building NTMU.sln (Debug|x64)..."
& $msbuildPath "NTMU.sln" /p:Configuration=Debug /p:Platform=x64
if ($LASTEXITCODE -ne 0) {
    Write-Error "Build failed!"
    exit $LASTEXITCODE
}

Write-Host "Signing Executables..."
$pw = ConvertTo-SecureString -String "Minecraft145!!" -Force -AsPlainText
$cert = Get-PfxCertificate -FilePath "C:\Users\Administrator\Desktop\Projects\Windows_NT_Modding_Utility\Elite-EasySigner\EliteSoftware_Special.pfx" -Password $pw
Set-AuthenticodeSignature -FilePath "x64\Release\WinNTMU.exe" -Certificate $cert -TimestampServer "http://timestamp.digicert.com"
Set-AuthenticodeSignature -FilePath "x64\Debug\WinNTMU.exe" -Certificate $cert -TimestampServer "http://timestamp.digicert.com"

Write-Host "Builds completed successfully. Adding changes to git..."
git add .
# We use SilentlyContinue in case there are no changes to commit
git commit -m "Auto-commit: Version bump and latest changes" | Out-Null

Write-Host "Pushing to remote repo..."
git push origin HEAD

$verMajor = (Select-String -Path "src\Resource.h" -Pattern "#define VER_MAJOR\s+(\d+)").Matches.Groups[1].Value
$verMinor = (Select-String -Path "src\Resource.h" -Pattern "#define VER_MINOR\s+(\d+)").Matches.Groups[1].Value
$verBuild = (Select-String -Path "src\Resource.h" -Pattern "#define VER_BUILD\s+(\d+)").Matches.Groups[1].Value
$verRevision = (Select-String -Path "src\Resource.h" -Pattern "#define VER_REVISION\s+(\d+)").Matches.Groups[1].Value
$version = "$verMajor.$verMinor.$verBuild.$verRevision"

$commitMsg = git log -1 --pretty=%B

Write-Host "Publishing GitHub Release v$version..."
$ghPath = "C:\Program Files\GitHub CLI\gh.exe"
if (Test-Path $ghPath) {
    & $ghPath release create "v$version" "x64\Release\WinNTMU.exe" -t "Release v$version" -n $commitMsg -R "TheShadyRainbow4/Windows_NT_Modding_Utility-FORK"
} else {
    Write-Host "GitHub CLI not found. Please install gh to automatically publish releases."
}

Write-Host "Done!"
