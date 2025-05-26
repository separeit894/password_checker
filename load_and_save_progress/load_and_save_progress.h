#pragma once
#include <vector>
#include <fstream>
#include <string>

using namespace std;

void loadProgress(int& currentLength, vector<wstring>& triedPasswords, const string& progressFile);

void saveProgress(int currentLength, const vector<wstring>& triedPasswords, const string& progressFile);