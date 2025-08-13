#include <iostream>
#include <string>
#include <windows.h>


bool attemptLogin(const std::wstring& username, const std::wstring& password) {
    HANDLE tokenHandle;
    bool result = LogonUserW(
        username.c_str(),
        NULL,
        password.c_str(),
        LOGON32_LOGON_INTERACTIVE,
        LOGON32_PROVIDER_DEFAULT,
        &tokenHandle
    );

    if (result) CloseHandle(tokenHandle);
    return result;
}