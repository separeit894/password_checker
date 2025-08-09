#pragma once
#include <vector>
#include <fstream>
#include <string>

using namespace std;

void loadProgress(wstring& username, wstring& charset, int& currentLength, vector<wstring>& triedPasswords, const string& progressFile);

void saveProgress(const wstring charset, const wstring username, int currentLength, const vector<wstring>& triedPasswords, const string& progressFile);