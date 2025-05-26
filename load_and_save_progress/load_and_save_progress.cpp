#include <iostream>
#include <vector>
#include <fstream>
#include <string>

using namespace std;

void loadProgress(int& currentLength, vector<wstring>& triedPasswords, const string& progressFile) {
    wifstream file(progressFile);
    if (file.is_open()) {
        wstring line;
        while (getline(file, line)) {
            if (line.find(L"length:") == 0) {
                currentLength = stoi(line.substr(7));
            } else if (line.find(L"password:") == 0) {
                triedPasswords.push_back(line.substr(9));
            }
        }
        file.close();
    }
}

void saveProgress(int currentLength, const vector<wstring>& triedPasswords, const string& progressFile) {
    wofstream file(progressFile);
    if (file.is_open()) {
        file << L"length: " << currentLength << endl;
        for (const wstring& password : triedPasswords) {
            file << L"password: " << password << endl;
        }
        file.close();
    }
}
