import os
import re

ph_path = r'C:\Users\Administrator\Desktop\Projects\Windows_NT_Modding_Utility\Windows_NT_Modding_Utility-FORK\src\Pack.h'
with open(ph_path, 'r', encoding='utf-8') as f:
    ph = f.read()
if 'bool CreateReversePack(LPCWSTR outPath);' not in ph:
    ph = ph.replace('bool Apply(void *lpParam, PackApplyProgressCallback pfnProgressCalback);', 'bool Apply(void *lpParam, PackApplyProgressCallback pfnProgressCalback);\n\tbool CreateReversePack(LPCWSTR outPath);')
    with open(ph_path, 'w', encoding='utf-8') as f:
        f.write(ph)

pc_path = r'C:\Users\Administrator\Desktop\Projects\Windows_NT_Modding_Utility\Windows_NT_Modding_Utility-FORK\src\Pack.cpp'
with open(pc_path, 'r', encoding='utf-8') as f:
    pc = f.read()

impl = '''
bool CPack::CreateReversePack(LPCWSTR outPath)
{
    WCHAR szIniPath[MAX_PATH];
    wcscpy_s(szIniPath, outPath);
    PathCchAppend(szIniPath, MAX_PATH, L"pack.ini");

    FILE* fIni = _wfsopen(szIniPath, L"w, ccs=UTF-8", _SH_DENYNO);
    if (!fIni) return false;

    fwprintf(fIni, L"[Pack]\\nName=Reverse Backup\\nAuthor=WinNTMU\\nVersion=1.0\\n\\n");
    fwprintf(fIni, L"[Section.Backup]\\nType=Files\\n");

    int secIndex = 1;
    for (const auto& sec : _sections)
    {
        if (sec.type == PackSectionType::Files || sec.type == PackSectionType::Resources)
        {
            fwprintf(fIni, L"[Section.Files.%d]\\nType=Files\\n", secIndex);
            for (const auto& item : sec.items)
            {
                if (GetFileAttributesW(item.destFile.c_str()) != INVALID_FILE_ATTRIBUTES)
                {
                    WCHAR fname[MAX_PATH];
                    wcscpy_s(fname, PathFindFileNameW(item.destFile.c_str()));
                    
                    WCHAR backupDest[MAX_PATH];
                    wcscpy_s(backupDest, outPath);
                    PathCchAppend(backupDest, MAX_PATH, fname);
                    
                    _CopyFileWithOldStack(item.destFile.c_str(), backupDest);
                    fwprintf(fIni, L"\\"%s\\"=\\"%s\\"\\n", fname, item.destFile.c_str());
                }
            }
            secIndex++;
        }
    }
    fclose(fIni);
    return true;
}
'''
if 'bool CPack::CreateReversePack' not in pc:
    pc += impl
    with open(pc_path, 'w', encoding='utf-8') as f:
        f.write(pc)

mw_path = r'C:\Users\Administrator\Desktop\Projects\Windows_NT_Modding_Utility\Windows_NT_Modding_Utility-FORK\src\MainWindow.cpp'
with open(mw_path, 'r', encoding='utf-8') as f:
    mw = f.read()

if 'IDM_TOOLSCREATEREVERSEPACK' not in mw:
    mw = mw.replace('#define IDM_TOOLSSYSRESTORE', '#define IDM_TOOLSCREATEREVERSEPACK 220\n#define IDM_TOOLSSYSRESTORE')
    mw = mw.replace('MENU_ITEM(IDM_TOOLSSYSRESTORE,          tools_system_restore)', 'MENU_ITEM(IDM_TOOLSSYSRESTORE,          tools_system_restore)\n\t\tAppendMenuW(hmenuSub, 0, IDM_TOOLSCREATEREVERSEPACK, L"Create Reverse Pack...")')
    
    cmd_block = '''
				case IDM_TOOLSCREATEREVERSEPACK:
				{
					wil::com_ptr<IFileOpenDialog> pDialog;
					if (SUCCEEDED(CoCreateInstance(CLSID_FileOpenDialog, nullptr, CLSCTX_INPROC_SERVER, IID_PPV_ARGS(&pDialog))))
					{
						pDialog->SetOptions(FOS_PICKFOLDERS | FOS_FORCEFILESYSTEM);
						if (SUCCEEDED(pDialog->Show(hWnd)))
						{
							wil::com_ptr<IShellItem> pItem;
							if (SUCCEEDED(pDialog->GetResult(&pItem)))
							{
								PWSTR pszPath;
								if (SUCCEEDED(pItem->GetDisplayName(SIGDN_FILESYSPATH, &pszPath)))
								{
									_pack.CreateReversePack(pszPath);
									CoTaskMemFree(pszPath);
								}
							}
						}
					}
					break;
				}
				case IDM_TOOLSSYSRESTORE:
'''
    mw = mw.replace('case IDM_TOOLSSYSRESTORE:', cmd_block)
    
    auto_backup = '''
	WCHAR szBackupDir[MAX_PATH];
	GetTempPathW(MAX_PATH, szBackupDir);
	PathCchAppend(szBackupDir, MAX_PATH, L"WinNTMU_Backup");
	CreateDirectoryW(szBackupDir, NULL);
	_pack.CreateReversePack(szBackupDir);

	if (_pack.Apply(this, s_ApplyProgressCallback))'''
    mw = mw.replace('if (_pack.Apply(this, s_ApplyProgressCallback))', auto_backup)
    
    with open(mw_path, 'w', encoding='utf-8') as f:
        f.write(mw)
