#include "Logging.h"
#include <unordered_map>
#include <stdio.h>
#include <share.h>

struct LogCallbackStore
{
	LogCallback pfnCallback;
	void *lpParam;
};

std::unordered_map<DWORD, LogCallbackStore> s_logCallbacks;

void Log(LPCWSTR pszFormat, ...)
{
	va_list args;
	va_start(args, pszFormat);

	WCHAR szBuffer[2048];
	_vsnwprintf_s(szBuffer, 2048, pszFormat, args);


	for (const auto &callback : s_logCallbacks)
	{
		(callback.second.pfnCallback)(callback.second.lpParam, szBuffer);
	}
    
	WCHAR szExePath[MAX_PATH];
	GetModuleFileNameW(NULL, szExePath, MAX_PATH);
	WCHAR* lastSlash = wcsrchr(szExePath, L'\\');
	if (lastSlash) {
		*lastSlash = L'\0';
		wcscat_s(szExePath, MAX_PATH, L"\\WinNTMU.log");
		FILE* fLog = _wfsopen(szExePath, L"a", _SH_DENYNO);
		if (fLog) {
			SYSTEMTIME st;
			GetLocalTime(&st);
			fwprintf(fLog, L"[%04d-%02d-%02d %02d:%02d:%02d] %s\n", st.wYear, st.wMonth, st.wDay, st.wHour, st.wMinute, st.wSecond, szBuffer);
			fclose(fLog);
		}
	}

	va_end(args);

}

void AddLogCallback(LogCallback pfnCallback, void *lpParam, DWORD *pdwCallbackID)
{
	*pdwCallbackID = s_logCallbacks.size();
	s_logCallbacks[*pdwCallbackID] = {
		pfnCallback,
		lpParam
	};
}

void RemoveLogCallback(DWORD dwCallbackID)
{
	s_logCallbacks.erase(dwCallbackID);
}