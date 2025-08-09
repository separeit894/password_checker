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

using namespace std;

clock_t start;
string progressFile = "progress.txt";



void generateCombinations(const wstring& charset, int length, wstring prefix, 
                         const wstring& username, vector<wstring>& triedPasswords) {
    
    if (length == 0) {
        if (!binary_search(triedPasswords.begin(), triedPasswords.end(), prefix)) {
            wcout << L"Попытка № " << triedPasswords.size() + 1 << L" для пароля: " << prefix << endl;
            
            if (attemptLogin(username, prefix)) {
                wcout << L"Успех! Пароль найден: " << prefix << endl;
                clock_t end = clock();
                double elapsed = static_cast<double>(end - start) / CLOCKS_PER_SEC;
                wcout << L"Поиск завершен. Общее время выполнения: " << elapsed << L" секунд." << endl;
                system("pause");
                exit(0);
            } else {
                triedPasswords.push_back(prefix);
                saveProgress(length + 1, triedPasswords, progressFile);
            }
        }
        return;
    }
    
    for (wchar_t c : charset) {
        generateCombinations(charset, length - 1, prefix + c, username, triedPasswords);
    }
}

int main() {
    // Включение поддержки Unicode в консоли
    _setmode(_fileno(stdin), _O_U16TEXT);
    _setmode(_fileno(stdout), _O_U16TEXT);

    system("net user");
    wstring username; // Изменен на wstring
    wstring charset;  // Изменен на wstring
    int minLength = 1;
    vector<wstring> triedPasswords; // Изменен на wstring
    int currentLength = minLength;

    
    loadProgress(currentLength, triedPasswords, progressFile);

    std::wcout << L"Version: " << 2.6 << std::endl <<
    L"Github: " << L"https://github.com/separeit894/password_checker" << std::endl;

    // Ввод имени пользователя через wcin
    wcout << L"Введите имя учетной записи: ";
    wcin >> username;

    vector<wstring> req_types = { // Изменен на wstring
        L"Цифры (y/n): ",
        L"Латинские буквы (y/n): ",
        L"Русские буквы (y/n): ",
        L"Спецсимволы (y/n): "
    };

    int level = 1;
    while (true) {
        if (level > 4) {
            break;
        }

        wcout << req_types[level - 1]; // Используется wcout
        wstring digits; // Изменен на wstring
        getline(wcin >> ws, digits); // Используется wcin

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
            level++;
        } else if (digits == L"n" || digits == L"N" || digits == L"н" || digits == L"Н") {
            level++;
        } else {
            wcout << L"Вы неправильно ввели! Введите 'y' или 'n'." << endl;
            if (level > 1) {
                level--;
            }
        }
    }

    start = clock();

    sort(triedPasswords.begin(), triedPasswords.end());

    while (true) {
        wcout << L"Начинаю проверку паролей длиной " << currentLength << L" символов..." << endl;
        generateCombinations(charset, currentLength, L"", username, triedPasswords);
        currentLength++;
    }

    return 0;
}