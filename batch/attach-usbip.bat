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
    echo Error: Server not specified in config file >> %LOGFILE%
    exit /b 1
)
if "%BUSID%"=="" (
    echo Error: Bus ID not specified in config file >> %LOGFILE%
    exit /b 1
)

:loop
echo Attempting connection to %SERVER% for device %BUSID% at %date% %time%
echo Attempting connection to %SERVER% for device %BUSID% at %date% %time% >> %LOGFILE%
"C:\Program Files\USBip\usbip.exe" attach -r %SERVER% -b %BUSID% >> %LOGFILE% 2>&1
if %errorlevel% equ 0 (
    echo Success at %date% %time%
    echo Success at %date% %time% >> %LOGFILE%
    exit /b 0
)
echo Attempt failed, retrying in 1 second...
echo Attempt failed, retrying in 1 second... >> %LOGFILE%
timeout /t 1 /nobreak >nul
goto loop