SCRIPT = main.cpp

OUTPUT_FILE = password_checker.exe

PROGRESS_FILE = progress.txt

build: 
	g++ -o $(OUTPUT_FILE) $(SCRIPT) load_and_save_progress\load_and_save_progress.cpp attemptLogin\attemptLogin.cpp

clean:
	@if not exist "$(OUTPUT_FILE)" (@echo here not file $(OUTPUT_FILE)) else (@echo here file $(OUTPUT_FILE) && del $(OUTPUT_FILE))
	@if not exist "$(PROGRESS_FILE)" (@echo here not file $(PROGRESS_FILE)) else (@echo here file $(PROGRESS_FILE) && del $(PROGRESS_FILE))