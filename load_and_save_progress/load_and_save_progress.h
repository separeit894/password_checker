#pragma once
#include <vector>
#include <fstream>
#include <string>


void loadProgress(std::wstring& username, std::wstring& charset, int& currentLength, std::vector<std::wstring>& triedPasswords, const std::string& progressFile);

void saveProgress(const std::wstring charset, const std::wstring username, int currentLength, const std::vector<std::wstring>& triedPasswords, const std::string& progressFile);