#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <ctime>
#include <windows.h>
#include <algorithm>
#include <io.h>
#include <filesystem>
#include <csignal>
#include <cstdlib>
#include <atomic>
#include <thread>
#include <codecvt>
#include <array>
#include <memory>

#include "load_and_save_progress/load_and_save_progress.h"
#include "attemptLogin/attemptLogin.h"


clock_t start;
std::string progressFile = "progress.txt";
int tryed = 0;

std::atomic<bool> stop(false);

std::wstring string_to_wstring(const std::string& str);

BOOL WINAPI ConsoleHandler(DWORD signal);

void generateCombinations(const std::wstring& charset, int length, std::wstring prefix, const std::wstring& username, std::vector<std::wstring>& triedPasswords); 

std::vector<std::wstring> exec(const char* cmd)
{
    std::array<wchar_t, 128> buffer;
    std::vector<std::wstring> result_vec;
    

    std::unique_ptr<FILE, decltype(&pclose)> pipe(popen(cmd, "r"), pclose);

    while(fgetws(buffer.data(), buffer.size(), pipe.get()) != nullptr)
    {
        std::wstring line = buffer.data();
        line.erase(std::find_if(line.rbegin(), line.rend(), [](unsigned char ch) {
            return !std::isspace(ch);
        }).base(), line.end());
        
        if(!line.empty());
            
            result_vec.push_back(line.substr());
    }

    if(!result_vec.empty())
        result_vec.erase(result_vec.begin());
        result_vec.erase(result_vec.begin());
        result_vec.erase(result_vec.begin());
        result_vec.erase(result_vec.end());
        result_vec.erase(result_vec.end());

    return result_vec;
}


int main(int argc, char* argv[]) {
    SetConsoleCtrlHandler(ConsoleHandler, TRUE);
    
    std::vector<std::string> args(argv, argv + argc);

    bool debug = false;
    for(const std::string arg : args)
    {
        
        if(arg == "--debug")
        {
            debug = true;
        }
    }

    // команда для проверки сколько пользователей
    std::string command_list_user = "powershell -Command \"Get-WmiObject -Class Win32_UserAccount -Filter 'LocalAccount=True' | Select-Object Name\"";
    std::vector<std::wstring> result = exec(command_list_user.c_str());

    int i = 0;
    for(std::wstring line : result)
    {
        std::wcout << i << L" : " << line << std::endl;
        
        ++i;
    }
    std::cout << std::endl;
    

    std::wstring username; // Изменен на wstring
    std::wstring charset ;  // Изменен на wstring
    int minLength = 1;
    std::vector<std::wstring> triedPasswords; // Изменен на wstring
    int currentLength = minLength;
    
    bool find_file = false;
    bool result_find_file = std::filesystem::exists(progressFile);
    
    if(debug)
    {
        std::wcout << L"result_find_file " <<result_find_file << std::endl;
    }
    
    if(result_find_file)
    {
        find_file = true;
        if(debug)
        {
            std::wcout << L"File " << string_to_wstring(progressFile) << L" find here!" << std::endl;

        }
    }
    else
    {
        if(debug)
        {
            std::wcout << L"File " << string_to_wstring(progressFile) << L" not here!" << std::endl;
        }
        
    }
    
    if(find_file)
        if(debug)
        {
            std::cout << "find file " << std::endl;
        }
            
        loadProgress(username, charset, currentLength, triedPasswords, progressFile);

    std::wcout << L"Version: " << (float)3.0 << std::endl <<
    L"Github Page Password Checker: " << L"https://github.com/separeit894/password_checker" << std::endl <<
    L"My Github Page: " << L"https://github.com/separeit894" << std::endl;

    
    // Ввод имени пользователя через wcin
    int number_account;
    if(username.empty())
    {
        std::wcout << L"Enter the number account: ";
        std::cin >> number_account;

        // Очистка буфера
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        username = result[number_account];
    }
    

    std::vector<std::wstring> req_types = { // Изменен на wstring
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
            std::wstring digits;
            // getline(wcin >> ws, digits); // Используется wcin
            std::wcout << req_types[level - 1]; // Используется wcout
            
            // int result = !std::getline(wcin, digits);
            //std::cout << "result: " << result << std::endl;
            if (!std::getline(std::wcin, digits)) {

                // Если ввод сломан (например, Ctrl+C), выходим
                std::wcout << L"\nInput interrupted. Exiting.\n";
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
                std::wcout << L"You entered it incorrectly! Enter 'y' or 'n'." <<  std::endl;
                level--;
                continue;
                
            }
        }
    }
    

    start = clock();

    sort(triedPasswords.begin(), triedPasswords.end());

    while (true) {

        std::wcout << L"I'm starting to check passwords. " << currentLength << L" characters..." << std::endl;
        std::thread mythread2(generateCombinations, std::ref(charset), currentLength, L"", username, std::ref(triedPasswords));
        mythread2.join();
        
        currentLength++;
    }

    return 0;
}



void generateCombinations(const std::wstring& charset, int length, std::wstring prefix, const std::wstring& username, std::vector<std::wstring>& triedPasswords) 
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
            std::wcout << L"Attempt number " << triedPasswords.size() << L" for password: " << line_combination << std::endl;
            if (attemptLogin(username, line_combination)) {
                std::wcout << L"Success! Password found: " << line_combination << std::endl;
                clock_t end = clock();
                double elapsed = static_cast<double>(end - start) / CLOCKS_PER_SEC;
                std::wcout << L"The search is completed. Total lead time: " << elapsed << L" seconds." << std::endl;
                system("pause");
                exit(0);
            } else
            {
                // the file will be saved once every 10 attempts.
                tryed++;
                if(tryed == 10)
                {
                    saveProgress(charset, username, length, triedPasswords, progressFile);
                    tryed = 0;
                }
                
            }
        }
    }

    
}

BOOL WINAPI ConsoleHandler(DWORD signal) {
    if (signal == CTRL_C_EVENT) {
        std::cout << "\nCaught Ctrl+C! Exit...\n";
        stop = true;
        exit(0);
        return TRUE;
        
    }
    return FALSE;
}

std::wstring string_to_wstring(const std::string& str)
{
    std::wstring_convert<std::codecvt_utf8<wchar_t>> converter;
    return converter.from_bytes(str);
}