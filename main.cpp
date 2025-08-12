#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <ctime>
#include <windows.h>
#include <algorithm>
#include <io.h>
#include <fcntl.h> // Для _setmode
#include "load_and_save_progress/load_and_save_progress.h"
#include "attemptLogin/attemptLogin.h"
#include <filesystem>
#include <csignal>
#include <cstdlib>
#include <atomic>
#include <thread>


using namespace std;

clock_t start;
string progressFile = "progress.txt";

std::atomic<bool> stop(false);

BOOL WINAPI ConsoleHandler(DWORD signal) {
    if (signal == CTRL_C_EVENT) {
        std::cout << "\nПоймал Ctrl+C! Выход...\n";
        stop = true;
        return TRUE;
    }
    return FALSE;
}

void generateCombinations(const wstring& charset, int length, wstring prefix, const wstring& username, vector<wstring>& triedPasswords); 


int main() {
    SetConsoleCtrlHandler(ConsoleHandler, TRUE);
    // Включение поддержки Unicode в консоли
    _setmode(_fileno(stdin), _O_U16TEXT);
    _setmode(_fileno(stdout), _O_U16TEXT);

    system("net user");
    wstring username; // Изменен на wstring
    wstring charset ;  // Изменен на wstring
    int minLength = 1;
    vector<wstring> triedPasswords; // Изменен на wstring
    int currentLength = minLength;
    
    bool find_file = false;
    if(filesystem::exists(progressFile))
    {
        find_file = true;
        std::cout << "file here" << std::endl;
    }
    else
    {
        std::cout << "file not here" << std::endl;
    }
    
    if(find_file)
        std::cout << "if else find file " << std::endl;
        loadProgress(username, charset, currentLength, triedPasswords, progressFile);

    std::wcout << L"Version: " << 2.8 << std::endl <<
    L"Github Page Password Checker: " << L"https://github.com/separeit894/password_checker" << std::endl <<
    L"My Github Page: " << L"https://github.com/separeit894" << std::endl;

    
    // Ввод имени пользователя через wcin
    if(username.empty())
    {
        wcout << L"Enter the account name: ";
        std::getline(wcin, username);
    }
    

    vector<wstring> req_types = { // Изменен на wstring
        L"Digits (y/n): ",
        L"Ascii letters (y/n): ",
        L"Russian letters (y/n): ",
        L"Special characters (y/n): "
    };

    if(charset.empty())
    {
        int level = 0;
        while (true) {
            if (level > 3) {
                break;
            }

            level++;
            wstring digits;
            // getline(wcin >> ws, digits); // Используется wcin
            wcout << req_types[level - 1] << " : "; // Используется wcout
            
            int result = !std::getline(wcin, digits);
            std::cout << "result: " << result << std::endl;
            if (!std::getline(wcin, digits)) {

                // Если ввод сломан (например, Ctrl+C), выходим
                wcout << L"\nInput interrupted. Exiting.\n";
                return -1;
                
            }
            
            
            if (digits == L"y" || digits == L"Y" || digits == L"д" || digits == L"Д") {
                if (level == 1) {
                    charset += L"0123456789"; // Добавлен префикс L для Unicode
                } else if (level == 2) {
                    charset += L"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
                } else if (level == 3) {
                    charset += L"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ";
                } else if (level == 4) {
                    charset += L"!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~";
                }
                
            } else if (digits == L"n" || digits == L"N" || digits == L"н" || digits == L"Н") {
                continue;
            } else {
                wcout << L"You entered it incorrectly! Enter 'y' or 'n'." <<  endl;
                level--;
                continue;
                
            }
        }
    }
    

    start = clock();

    sort(triedPasswords.begin(), triedPasswords.end());

    while (true) {

        wcout << L"I'm starting to check passwords. " << currentLength << L" characters..." << endl;
        thread mythread2(generateCombinations, std::ref(charset), currentLength, L"", username, std::ref(triedPasswords));
        mythread2.join();
        
        currentLength++;
    }

    return 0;
}



void generateCombinations(const wstring& charset, int length, wstring prefix, const wstring& username, vector<wstring>& triedPasswords) 
{
    
    std::vector<std::wstring> combinations;
    combinations.push_back(L"");

    for(int i = 0; i < length; ++i)
    {
        std::vector<std::wstring> newCombinations;
        for(const std::wstring combination : combinations)
        {
            for(wchar_t c : charset)
            {
                newCombinations.push_back(combination + c);
            }
        }
        combinations = newCombinations;
    }

    for(std::wstring line_combination : combinations)
    {
        if (!binary_search(triedPasswords.begin(), triedPasswords.end(), line_combination))
        {
            
            triedPasswords.push_back(line_combination);
            wcout << L"Attempt number " << triedPasswords.size() << L" for password: " << line_combination << endl;
            if (attemptLogin(username, line_combination)) {
                wcout << L"Success! Password found: " << prefix << endl;
                clock_t end = clock();
                double elapsed = static_cast<double>(end - start) / CLOCKS_PER_SEC;
                wcout << L"The search is completed. Total lead time: " << elapsed << L" seconds." << endl;
                system("pause");
                exit(0);
            } else
            {
                saveProgress(charset, username, length, triedPasswords, progressFile);
            }

        }
    }

    
}