@echo off
setlocal enabledelayedexpansion

set LOGFILE=usbip_log.txt
set CONFIG_FILE=usbip_conf.txt

:: Read configuration from file
set SERVER=
set BUSID=
for /f "tokens=1,2 delims== " %%A in (%CONFIG_FILE%) do (
    if /i "%%A"=="server" set SERVER=%%B
    if /i "%%A"=="busid" set BUSID=%%B
)

:: Check if configuration was loaded
if "%SERVER%"=="" (
    echo Error: Server not specified in config file | %SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe -Command "$input | Tee-Object -FilePath \"%LOGFILE%\" -Append"
    exit /b 1
)
if "%BUSID%"=="" (
    echo Error: Bus ID not specified in config file | %SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe -Command "$input | Tee-Object -FilePath \"%LOGFILE%\" -Append"
    exit /b 1
)

:loop
echo Attempting connection to %SERVER% for device %BUSID% at %date% %time% | %SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe -Command "$input | Tee-Object -FilePath \"%LOGFILE%\" -Append"
"C:\Program Files\USBip\usbip.exe" attach -r %SERVER% -b %BUSID% | %SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe -Command "$input | Tee-Object -FilePath \"%LOGFILE%\" -Append"
if %errorlevel% equ 0 (
    echo Success at %date% %time% | %SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe -Command "$input | Tee-Object -FilePath \"%LOGFILE%\" -Append"
    exit /b 0
)
echo Attempt failed, retrying in 1 second... | %SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe -Command "$input | Tee-Object -FilePath \"%LOGFILE%\" -Append"
timeout /t 1 /nobreak >nul
goto loop