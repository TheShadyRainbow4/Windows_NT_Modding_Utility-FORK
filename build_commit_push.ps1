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

Write-Host "Signing WinNTMU.exe (Release)..."
& "C:\Users\Administrator\Desktop\Projects\Windows_NT_Modding_Utility\Elite-EasySigner\Elite-EasySigner_x64.exe" "x64\Release\WinNTMU.exe"

Write-Host "Building NTMU.sln (Debug|x64)..."
& $msbuildPath "NTMU.sln" /p:Configuration=Debug /p:Platform=x64
if ($LASTEXITCODE -ne 0) {
    Write-Error "Build failed!"
    exit $LASTEXITCODE
}

Write-Host "Signing WinNTMU.exe (Debug)..."
& "C:\Users\Administrator\Desktop\Projects\Windows_NT_Modding_Utility\Elite-EasySigner\Elite-EasySigner_x64.exe" "x64\Debug\WinNTMU.exe"

Write-Host "Builds and signing completed successfully. Adding changes to git..."
git add .
git commit -m "Update branding to EliteSoftware Edition, versions, and add custom packs link"

Write-Host "Pushing to remote repo..."
git push origin HEAD

Write-Host "Done!"
