#pragma once
#include <vector>
#include <fstream>
#include <string>


void loadProgress(std::wstring& username, std::wstring &locale,std::wstring& charset, int& currentLength, std::vector<std::wstring>& triedPasswords, const std::string& progressFile);

void saveProgress(const std::wstring charset, const std::wstring username, std::wstring locale,int currentLength, const std::vector<std::wstring>& triedPasswords, const std::string& progressFile);