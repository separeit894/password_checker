#include <iostream>
#include <vector>
#include <fstream>
#include <string>

using namespace std;

void loadProgress(wstring& username, wstring& charset, int& currentLength, vector<wstring>& triedPasswords, const string& progressFile) {
    wifstream file(progressFile);
    if (file.is_open()) {
        wstring line;
        while (getline(file, line)) {
            if(line.find(L"username:")== 0)
            {
                username = line.substr(10);
            }

            if(line.find(L"charset:") == 0)
            {
                charset = line.substr(9);
            }

            if (line.find(L"length:") == 0) {
                currentLength = stoi(line.substr(7));
            } 
            
            if (line.find(L"password:") == 0) {
                triedPasswords.push_back(line.substr(10));
                
            }
        }
        file.close();
    }
}

void saveProgress(const wstring charset, const wstring username, int currentLength, const vector<wstring>& triedPasswords, const string& progressFile) {
    wofstream file(progressFile);
    if (file.is_open()) {
        file << "username: " << username << endl;
        file << L"charset: " << charset << endl;
        file << L"length: " << currentLength << endl;
        for (const wstring& password : triedPasswords) {
            file << L"password: " << password << endl;
        }
        file.close();
    }
    else
    {
        wcout << L"Не открылся файл" << std::endl;
    }
}
