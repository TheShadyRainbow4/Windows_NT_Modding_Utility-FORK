$ErrorActionPreference = "Stop"

$msbuildPath = "C:\Program Files\Microsoft Visual Studio\2022\Community\MSBuild\Current\Bin\MSBuild.exe"
if (-not (Test-Path $msbuildPath)) {
    Write-Error "MSBuild.exe not found at $msbuildPath"
}

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
git commit -m "Auto-commit: Version bump and latest changes"

Write-Host "Pushing to remote repo..."
git push origin HEAD

$verMajor = (Select-String -Path "src\Resource.h" -Pattern "#define VER_MAJOR\s+(\d+)").Matches.Groups[1].Value
$verMinor = (Select-String -Path "src\Resource.h" -Pattern "#define VER_MINOR\s+(\d+)").Matches.Groups[1].Value
$verRevision = (Select-String -Path "src\Resource.h" -Pattern "#define VER_REVISION\s+(\d+)").Matches.Groups[1].Value
$version = "$verMajor.$verMinor.$verRevision.0"

$commitMsg = git log -1 --pretty=%B

Write-Host "Publishing GitHub Release v$version..."
$ghPath = "C:\Program Files\GitHub CLI\gh.exe"
if (Test-Path $ghPath) {
    & $ghPath release create "v$version" "x64\Release\WinNTMU.exe" -t "Release v$version" -n $commitMsg
} else {
    Write-Host "GitHub CLI not found. Please install gh to automatically publish releases."
}

Write-Host "Done!"
