#include <iostream>
#include <vector>
#include <fstream>
#include <string>



void loadProgress(std::wstring& username, std::wstring& charset, int& currentLength, std::vector<std::wstring>& triedPasswords, const std::string& progressFile) {
    std::wifstream file(progressFile);
    if (file.is_open()) {
        std::wstring line;
        while (std::getline(file, line)) {
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

void saveProgress(const std::wstring charset, const std::wstring username, int currentLength, const std::vector<std::wstring>& triedPasswords, const std::string& progressFile) {
    std::wofstream file(progressFile);
    if (file.is_open()) {
        file << "username: " << username << std::endl;
        file << L"charset: " << charset << std::endl;
        file << L"length: " << currentLength << std::endl;
        for (const std::wstring& password : triedPasswords) {
            file << L"password: " << password << std::endl;
        }
        file.close();
    }
    
}
