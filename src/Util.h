#pragma once
#include "NTMU.h"
#include <string>

void trim(std::wstring &s);

HRESULT WaitForProcess(LPCWSTR pszCommandLine, DWORD *lpdwExitCode, DWORD dwCreationFlags = 0);
void ScreenCenteredRect(int cx, int cy, DWORD dwStyle, DWORD dwExStyle, bool fMenu, LPRECT lprc);
void ParentCenteredRect(
	HWND hwndParent,
	int cx,
	int cy,
	DWORD dwStyle,
	DWORD dwExStyle,
	bool fMenu,
	LPRECT lprc);