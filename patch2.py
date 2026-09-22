import os
path = r'C:\Users\Administrator\Desktop\Projects\Windows_NT_Modding_Utility\Windows_NT_Modding_Utility-FORK\build_commit_push.ps1'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
if 'Elite-EasySigner' not in content:
    content += '\nWrite-Host "Signing EXE..."\n& "C:\\Users\\Administrator\\Desktop\\Projects\\Windows_NT_Modding_Utility\\Elite-EasySigner\\Elite-EasySigner_x64.exe" "\\x64\\Release\\WinNTMU.exe"\n'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
