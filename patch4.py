import os
mw_path = r'C:\Users\Administrator\Desktop\Projects\Windows_NT_Modding_Utility\Windows_NT_Modding_Utility-FORK\src\MainWindow.cpp'
with open(mw_path, 'r', encoding='utf-8') as f:
    mw = f.read()

if 'PlaySoundW(MAKEINTRESOURCEW(110)' not in mw: # 110 is IDR_WAV_COMPLETE
    mw = mw.replace('MainWndMsgBox(_pTranslations->pack_apply_successful, MB_ICONINFORMATION);', 'PlaySoundW(MAKEINTRESOURCEW(110), g_hinst, SND_RESOURCE | SND_ASYNC);\n\t\tMainWndMsgBox(_pTranslations->pack_apply_successful, MB_ICONINFORMATION);')
    with open(mw_path, 'w', encoding='utf-8') as f:
        f.write(mw)
