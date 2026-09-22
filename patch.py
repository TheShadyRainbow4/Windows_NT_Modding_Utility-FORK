import os
import re

def main():
    mw_path = r'C:\Users\Administrator\Desktop\Projects\Windows_NT_Modding_Utility\Windows_NT_Modding_Utility-FORK\src\MainWindow.cpp'
    with open(mw_path, 'r', encoding='utf-8') as f:
        mw = f.read()

    # Task 1: UAC Shield
    shield_code = '''	EnableWindow(_hwndApply, FALSE);
	SendMessageW(_hwndApply, BCM_SETSHIELD, 0, TRUE);'''
    mw = mw.replace('	EnableWindow(_hwndApply, FALSE);', shield_code, 1)

    # Task 2: _HandleLoadPath method
    handle_load_path = '''
void CMainWindow::_HandleLoadPath(LPCWSTR szPath, LoadSource loadSource)
{
	DWORD attrs = GetFileAttributesW(szPath);
	if (attrs == INVALID_FILE_ATTRIBUTES) return;

	if (attrs & FILE_ATTRIBUTE_DIRECTORY) {
		WCHAR szIni[MAX_PATH];
		wcscpy_s(szIni, szPath);
		PathCchAppend(szIni, MAX_PATH, L"pack.ini");
		_LoadPack(szIni, loadSource);
	} else {
		LPCWSTR ext = PathFindExtensionW(szPath);
		if (ext && _wcsicmp(ext, L".zip") == 0) {
			WCHAR cmd[MAX_PATH * 3];
			swprintf_s(cmd, MAX_PATH * 3, L"tar.exe -xf \\"%s\\" -C \\"%s\\"", szPath, g_szTempDir);
			
			STARTUPINFOW si = { sizeof(si) };
			PROCESS_INFORMATION pi;
			if (CreateProcessW(NULL, cmd, NULL, NULL, FALSE, CREATE_NO_WINDOW, NULL, NULL, &si, &pi)) {
				WaitForSingleObject(pi.hProcess, INFINITE);
				CloseHandle(pi.hProcess);
				CloseHandle(pi.hThread);
			}
			
			WCHAR szIni[MAX_PATH];
			wcscpy_s(szIni, g_szTempDir);
			PathCchAppend(szIni, MAX_PATH, L"pack.ini");
			_LoadPack(szIni, loadSource);
		} else {
			_LoadPack(szPath, loadSource);
		}
	}
}
'''
    mw = mw.replace('void CMainWindow::_LoadPack(LPCWSTR pszPath, LoadSource loadSource)', handle_load_path + '\nvoid CMainWindow::_LoadPack(LPCWSTR pszPath, LoadSource loadSource)')

    # replace _LoadPack with _HandleLoadPath in WM_DROPFILES and IDM_FILEOPEN and _OnCreate
    mw = mw.replace('_LoadPack(szFilePath, LoadSource::Default);', '_HandleLoadPath(szFilePath, LoadSource::Default);')
    mw = mw.replace('_LoadPack(szFile, LoadSource::Default);', '_HandleLoadPath(szFile, LoadSource::Default);')
    mw = mw.replace('_LoadPack(g_szInitialPack, LoadSource::CommandLine);', '_HandleLoadPath(g_szInitialPack, LoadSource::CommandLine);')

    # Add Shlwapi.h
    mw = mw.replace('#include "Util.h"', '#include "Util.h"\n#include <shlwapi.h>\n#pragma comment(lib, "shlwapi.lib")')

    # Task 4: StatusBar click & parts
    status_parts = '''	int parts[] = { 100, 200, -1 };
	SendMessageW(_hwndStatusBar, SB_SETPARTS, 3, (LPARAM)parts);
	
	WCHAR szVer[64];
	swprintf_s(szVer, L"Version %d.%d.%d.0", VER_MAJOR, VER_MINOR, VER_REVISION);
	SendMessageW(_hwndStatusBar, SB_SETTEXTW, 0, (LPARAM)L"Ready");
	SendMessageW(_hwndStatusBar, SB_SETTEXTW, 1, (LPARAM)szVer);
	SendMessageW(_hwndStatusBar, SB_SETTEXTW, 2, (LPARAM)L"View WinNTMU Logs");'''
    
    mw = re.sub(r'	int parts\[\] = { 100, -1 };\n	SendMessageW\(_hwndStatusBar, SB_SETPARTS, 2, \(LPARAM\)parts\);\n	\n	WCHAR szVer\[64\];\n	swprintf_s\(szVer, L"Version %d.%d.%d.0", VER_MAJOR, VER_MINOR, VER_REVISION\);\n	SendMessageW\(_hwndStatusBar, SB_SETTEXTW, 0, \(LPARAM\)L"Ready"\);\n	SendMessageW\(_hwndStatusBar, SB_SETTEXTW, 1, \(LPARAM\)szVer\);', status_parts, mw)

    layout_parts = '''		int parts[] = { RECTWIDTH(rcClient) - 250, RECTWIDTH(rcClient) - 150, -1 };
		SendMessageW(_hwndStatusBar, SB_SETPARTS, 3, (LPARAM)parts);'''
    mw = re.sub(r'		int parts\[\] = { RECTWIDTH\(rcClient\) - 150, -1 };\n		SendMessageW\(_hwndStatusBar, SB_SETPARTS, 2, \(LPARAM\)parts\);', layout_parts, mw)

    # WM_NOTIFY
    notify_block = '''		case WM_NOTIFY:
		{
			UINT uCode = ((LPNMHDR)lParam)->code;
			HWND hwndFrom = ((LPNMHDR)lParam)->hwndFrom;

			if (hwndFrom == _hwndStatusBar && uCode == NM_CLICK)
			{
				LPNMMOUSE pnm = (LPNMMOUSE)lParam;
				if (pnm->dwItemSpec == 2)
				{
					WCHAR szExePath[MAX_PATH];
					GetModuleFileNameW(NULL, szExePath, MAX_PATH);
					PathCchRemoveFileSpec(szExePath, MAX_PATH);
					PathCchAppend(szExePath, MAX_PATH, L"WinNTMU.log");
					ShellExecuteW(NULL, L"open", szExePath, NULL, NULL, SW_SHOWNORMAL);
				}
				return 0;
			}
'''
    mw = mw.replace('		case WM_NOTIFY:\n		{\n			UINT uCode = ((LPNMHDR)lParam)->code;\n', notify_block)
    # wait, TreeView NM_CLICK also uses uCode == NM_CLICK but we just need to ensure it skips if hwndFrom is status bar. 
    # since we return 0, it won't execute tree view code. But we should make sure tree view code doesn't get messed up.
    
    with open(mw_path, 'w', encoding='utf-8') as f:
        f.write(mw)

    mwh_path = r'C:\Users\Administrator\Desktop\Projects\Windows_NT_Modding_Utility\Windows_NT_Modding_Utility-FORK\src\MainWindow.h'
    with open(mwh_path, 'r', encoding='utf-8') as f:
        mwh = f.read()
    mwh = mwh.replace('void _LoadPack(LPCWSTR pszPath, LoadSource loadSource);', 'void _HandleLoadPath(LPCWSTR szPath, LoadSource loadSource);\n	void _LoadPack(LPCWSTR pszPath, LoadSource loadSource);')
    with open(mwh_path, 'w', encoding='utf-8') as f:
        f.write(mwh)
        
    log_path = r'C:\Users\Administrator\Desktop\Projects\Windows_NT_Modding_Utility\Windows_NT_Modding_Utility-FORK\src\Logging.cpp'
    with open(log_path, 'r', encoding='utf-8') as f:
        log = f.read()

    log_append = '''
	for (const auto &callback : s_logCallbacks)
	{
		(callback.second.pfnCallback)(callback.second.lpParam, szBuffer);
	}
    
	WCHAR szExePath[MAX_PATH];
	GetModuleFileNameW(NULL, szExePath, MAX_PATH);
	WCHAR* lastSlash = wcsrchr(szExePath, L'\\\\');
	if (lastSlash) {
		*lastSlash = L'\\0';
		wcscat_s(szExePath, MAX_PATH, L"\\\\WinNTMU.log");
		FILE* fLog = _wfsopen(szExePath, L"a, ccs=UTF-8", _SH_DENYNO);
		if (fLog) {
			fwprintf(fLog, L"%s\\n", szBuffer);
			fclose(fLog);
		}
	}
'''
    log = log.replace('''	for (const auto &callback : s_logCallbacks)
	{
		(callback.second.pfnCallback)(callback.second.lpParam, szBuffer);
	}''', log_append)
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write(log)

if __name__ == '__main__':
    main()
