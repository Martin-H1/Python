# Macros to enable Linux versus Windows portability.
ifeq ($(OS),Windows_NT)
    / = $(strip \)
    PYTHON = C:\Users\Martin\AppData\Local\Programs\Python\Python38\python.exe
    RM = del /f /q
    RMDIR = rmdir /s /q
    SHELL_EXT = bat
    TOUCH = type nul >
else
    / = /
    PYTHON = python
    RM = rm -f
    RMDIR = rm -rf
    SHELL_EXT = sh
    TOUCH = touch
endif

bears:
	$(PYTHON) scramble_squares.py bears.json

wolves:
	$(PYTHON) scramble_squares.py wolves.json