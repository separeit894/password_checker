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


std::wstring VERSION = L"3.3"; 

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
        // We remove three lines from the beginning because they are empty
        result_vec.erase(result_vec.begin());
        result_vec.erase(result_vec.begin());
        result_vec.erase(result_vec.begin());
        // We remove three lines from the end because they are empty
        result_vec.erase(result_vec.end());
        result_vec.erase(result_vec.end());

    return result_vec;
}


int main(int argc, char* argv[]) {
    SetConsoleCtrlHandler(ConsoleHandler, TRUE);
    
    bool debug = false;
    std::wstring username; // creating a variable to which the account username will be passed
    std::wstring charset ;  // creating a variable that will be passed the characters that will be used in combinations.
    for(int i = 1; i < argc; ++i)
    {
        if(strcmp(argv[i], "--debug") == 0)
        {
            debug = true;
            
        } else if (strcmp(argv[i],"--username") == 0)
        {
            int b = ++i;
            if(b < argc && argv[b][0] != '-')
            {
                username = string_to_wstring(argv[b]);
                
            } else
            {
                wprintf(L"Username is incorrect!\n");
                exit(0);
            }
        } else if(strcmp(argv[i], "--charset") == 0)
        {
            int b = ++i;
            if(b < argc && argv[b][0] != '-')
            {
                charset = string_to_wstring(argv[b]);
                
            } else
            {
                wprintf(L"Charset is incorrect!\n");

                exit(0);
            }

        } else if(strcmp(argv[i], "--version") == 0 || strcmp(argv[i], "-v") == 0) 
        {
            wprintf(L"Password Checker C++ V-%ls \n", VERSION.c_str());

            exit(0);
        } else if(strcmp(argv[i], "--help") == 0 || strcmp(argv[i], "/?") == 0)
        {
            wprintf(L"Usage: password_checker [options]\n\n");
            wprintf(L"Description:\n");
            wprintf(L"  Password Checker is a program that logs into a Windows account by iterating through the characters given to it by the user.\n");
            wprintf(L"  It works if the user has a null value of \"lock threshold value\" in secpol.msc.\n");
            wprintf(L"  Read more on Github: https://github.com/separeit894/password_checker/tree/password_checker_c%2B%2B\n\n");
            wprintf(L"Options:\n");
            wprintf(L"  --debug              Enable debug mode.\n");
            wprintf(L"  --version, -v        Show the program version.\n");
            wprintf(L"  --username USERNAME  Specify the username.\n");
            wprintf(L"  --charset CHARSET    Specify the character set.\n");
            wprintf(L"  --help, /?           Show this help message.\n");
            wprintf(L"\nExamples:\n");
            wprintf(L"  password_checker --username JohnDoe --charset 01234\n");
            wprintf(L"  password_checker --debug\n");
            wprintf(L"  password_checker --version\n");
            wprintf(L"  password_checker\n");
            
            exit(0);
        }
        else
        {
            wprintf(L"There is no such argument to learn more about the program --help or /?\n");
            
            exit(0);
        }
    }
    

    // the command to check how many users
    std::vector<std::wstring> result;
    if(username.empty() || charset.empty())
    {
        std::string command_list_user = "powershell -Command \"Get-WmiObject -Class Win32_UserAccount -Filter 'LocalAccount=True' | Select-Object Name\"";
        result = exec(command_list_user.c_str());

        if(username.empty())
        {
            int i = 0;
            for(std::wstring line : result)
            {
                wprintf(L"%i : %ls\n", i, line.c_str());
                ++i;
            }
            std::cout << std::endl;
        }
        
    }
    
    
    int minLength = 1;
    std::vector<std::wstring> triedPasswords; 
    int currentLength = minLength;
    
    bool result_find_file = std::filesystem::exists(progressFile);
    
    if(result_find_file)
    {
        
        if(debug)
        {
            wprintf(L"File %ls find here! \n", string_to_wstring(progressFile).c_str());
        }
        loadProgress(username, charset, currentLength, triedPasswords, progressFile);
    }
    else
    {
        if(debug)
        {
            wprintf(L"File %ls not here! \n", string_to_wstring(progressFile).c_str());
        }
        
    }        

    std::wstring link_github_page_password_checker = L"https://github.com/separeit894/password_checker";
    std::wstring my_github_page = L"https://github.com/separeit894";

    wprintf(L"Version: %ls \nGithub Page Password Checker: %ls \nMy Github Page: %ls \n", VERSION.c_str(), link_github_page_password_checker.c_str(), my_github_page.c_str());
    
    
    // Entering the user's number via wcin
    int number_account;
    if(username.empty())
    {
        wprintf(L"Enter the number account: ");
        
        std::wcin >> number_account;

        // Clearing the buffer wcin
        std::wcin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        username = result[number_account];
    }
    

    std::vector<std::wstring> req_types = { 
        L"Digits (y/n): ",
        L"Ascii letters (y/n): ",
        L"Special characters (y/n): "
    };

    if(charset.empty())
    {
        int level = 0;
        while (true) {
            if (level > 2) {
                break;
            }

            level++;
            std::wstring digits;
            
            wprintf(L"%ls", req_types[level - 1].c_str());
            
            if (!std::getline(std::wcin, digits)) {

                // If the input is broken (for example, Ctrl+C), exit
                wprintf(L"\nInput interrupted. Exiting.\n");
                
                return -1;
            }
            
            if (digits == L"y" || digits == L"Y") {
                if (level == 1) {
                    charset += L"0123456789"; // Digits
                } else if (level == 2) {
                    charset += L"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"; // Latin alphabet
                }  else if (level == 3) {
                    charset += L"!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"; // Special symbols
                }
                
            } else if (digits == L"n" || digits == L"N") {
                continue;
            } else {
                wprintf(L"You entered it incorrectly! Enter 'y' or 'n'.\n");
                level--;
            }
        }
        
    }
    

    start = clock();

    sort(triedPasswords.begin(), triedPasswords.end());

    while (true) {
        wprintf(L"I'm starting to check passwords. %i  characters...\n", currentLength);
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
            DWORD Error = GetLastError();
            triedPasswords.push_back(line_combination);
            wprintf(L"Error : %i : Attempt number %i for password: %ls \n", Error, triedPasswords.size(), line_combination.c_str());
            
            if (attemptLogin(username, line_combination)) {
                wprintf(L"Success! Password found: %ls \n", line_combination.c_str());
                
                clock_t end = clock();
                double elapsed = static_cast<double>(end - start) / CLOCKS_PER_SEC;
                
                wprintf(L"The search is completed. Total lead time: %.2lf seconds.\n", elapsed);

                system("pause");
                exit(0);
            } else
            {
                
                if(Error == 1909)
                {
                    wprintf(L"Error 1909 means that your account has been blocked\n\tthe end of the work \n");
                    
                    system("pause");
                
                    exit(0);
                }

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
        wprintf(L"\nCaught Ctrl+C! Exit...\n");
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