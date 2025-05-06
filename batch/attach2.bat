@echo off
setlocal enabledelayedexpansion

set LOGFILE=usbip_log.txt
set CONFIG_FILE=usbip_conf.txt

:: Function to log and display messages
:log
set message=%*
echo %message% | %SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe -Command "$input | Tee-Object -FilePath \"%LOGFILE%\" -Append"
goto :eof

:: Read configuration from file
set SERVER=
set BUSID=
for /f "tokens=1,2 delims== " %%A in (%CONFIG_FILE%) do (
    if /i "%%A"=="server" set SERVER=%%B
    if /i "%%A"=="busid" set BUSID=%%B
)

:: Check if configuration was loaded
if "%SERVER%"=="" (
    call :log "Error: Server not specified in config file"
    exit /b 1
)
if "%BUSID%"=="" (
    call :log "Error: Bus ID not specified in config file"
    exit /b 1
)

:loop
call :log "Attempting connection to %SERVER% for device %BUSID% at %date% %time%"
"C:\Program Files\USBip\usbip.exe" attach -r %SERVER% -b %BUSID% | %SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe -Command "$input | Tee-Object -FilePath \"%LOGFILE%\" -Append"
if %errorlevel% equ 0 (
    call :log "Success at %date% %time%"
    exit /b 0
)
call :log "Attempt failed, retrying in 1 second..."
timeout /t 1 /nobreak >nul
goto loop