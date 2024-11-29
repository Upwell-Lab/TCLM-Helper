@echo off
chcp 65001 > nul

:: Set variables
set PYTHON_VERSION=3.10.11
set VENV_DIR=Packages
set PYTHON_INSTALL_DIR=%~dp0system_\Python%PYTHON_VERSION%
set LOG_DIR=%~dp0Logs\System logs
set LOG_FILE=%LOG_DIR%\system.log

:: Create log directory if it doesn't exist
if not exist "%LOG_DIR%" (
    mkdir "%LOG_DIR%"
)

:: Check if Python is already installed and get its version
for /f "tokens=2 delims== " %%i in ('"%PYTHON_INSTALL_DIR%\python.exe" --version 2^>nul') do set PYTHON_INSTALLED_VERSION=%%i
if defined PYTHON_INSTALLED_VERSION (
echo Found Python version: %PYTHON_INSTALLED_VERSION%
echo Found Python version: %PYTHON_INSTALLED_VERSION% >> "%LOG_FILE%" 2>&1
    echo Found Python version: %PYTHON_INSTALLED_VERSION%
    echo Found Python version: %PYTHON_INSTALLED_VERSION% >> "%LOG_FILE%" 2>&1
    if "%PYTHON_INSTALLED_VERSION%" == "%PYTHON_VERSION%" (
        echo Python %PYTHON_VERSION% is already installed
        echo Python %PYTHON_VERSION% is already installed >> "%LOG_FILE%" 2>&1
        set "PYTHON_EXEC=%PYTHON_INSTALL_DIR%\python"
        goto check_venv
    )
)
:: Check if the Python install directory exists, create it if necessary
if not exist "%PYTHON_INSTALL_DIR%" (
    echo Python installation directory does not exist. Creating %PYTHON_INSTALL_DIR% 
    echo Python installation directory does not exist. Creating %PYTHON_INSTALL_DIR% >> "%LOG_FILE%" 2>&1
    mkdir "%PYTHON_INSTALL_DIR%"
)

:: Check if the script was already restarted
set PYTHON_INSTALLER=%PYTHON_INSTALL_DIR%\python-%PYTHON_VERSION%-amd64.exe
if exist %PYTHON_INSTALLER% (
    echo Previous installer file found. Skipping download.
    echo Previous installer file found. Skipping download. >> "%LOG_FILE%" 2>&1
    goto install_python
)

:: Set the URL variable for downloading
set PYTHON_INSTALLER_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-amd64.exe

:: Download the installer file
echo Downloading Python %PYTHON_VERSION% >> "%LOG_FILE%"
echo Downloading Python %PYTHON_VERSION% >> "%LOG_FILE%" 2>&1
powershell -Command "Invoke-WebRequest -Uri %PYTHON_INSTALLER_URL% -OutFile %PYTHON_INSTALLER%"

:: Check if the download was successful
if not exist %PYTHON_INSTALLER% (
    echo Error downloading the installer file
    echo Error downloading the installer file >> "%LOG_FILE%" 2>&1
    exit /b 1
)

:install_python
echo Installing Python %PYTHON_VERSION% to %PYTHON_INSTALL_DIR%
echo Installing Python %PYTHON_VERSION% to %PYTHON_INSTALL_DIR% >> "%LOG_FILE%" 2>&1

:: Silent installation of Python with addition to PATH
%PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1 TargetDir=%PYTHON_INSTALL_DIR%

:: Check if the installation was successful
if %ERRORLEVEL% equ 0 (
    echo Python %PYTHON_VERSION% installed successfully
    echo Python %PYTHON_VERSION% installed successfully >> "%LOG_FILE%" 2>&1
    :: Delete the installer file
    del /f /q %PYTHON_INSTALLER%
    :: Restart the script to refresh the environment variables
    start cmd /c "%~f0"
    exit /b 0
) else (
    echo Error installing Python %PYTHON_VERSION% 
    echo Error installing Python %PYTHON_VERSION% >> "%LOG_FILE%" 2>&1
    exit /b 1
)

:check_venv
:: Check if the virtual environment exists
if not exist %VENV_DIR% (
    echo Virtual environment not found. Creating virtual environment.
    echo Virtual environment not found. Creating virtual environment. >> "%LOG_FILE%" 2>&1
    %PYTHON_EXEC% -m venv %VENV_DIR% >> "%LOG_FILE%" 2>&1
)

:: Activate the virtual environment and install dependencies
echo Installing dependencies from system_/packages.txt
echo Installing dependencies from system_/packages.txt >> "%LOG_FILE%" 2>&1
call %VENV_DIR%\Scripts\activate
%VENV_DIR%\Scripts\python.exe -m pip install --upgrade pip >> "%LOG_FILE%" 2>&1
%VENV_DIR%\Scripts\python.exe -m pip install -r _system\packages.txt >> "%LOG_FILE%" 2>&1
echo Dependencies installed successfully
echo Dependencies installed successfully >> "%LOG_FILE%" 2>&1

echo Server launch >> "%LOG_FILE%"
echo Server launch >> "%LOG_FILE%" 2>&1
python launch.py
pause