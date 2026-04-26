@echo off
echo ======================================
echo BISMILAH - Creating Desktop Shortcut
echo ======================================
echo.

:: Создаем ярлык через VBS скрипт
echo Set WshShell = CreateObject("WScript.Shell") > temp.vbs
echo Set Shortcut = WshShell.CreateShortcut("%USERPROFILE%\Desktop\BISMILAH.lnk") >> temp.vbs
echo Shortcut.TargetPath = "%~dp0gaame.exe" >> temp.vbs
echo Shortcut.WorkingDirectory = "%~dp0" >> temp.vbs
echo Shortcut.Description = "BISMILAH Game" >> temp.vbs
echo Shortcut.Save() >> temp.vbs

cscript //Nologo temp.vbs
del temp.vbs

if exist "%USERPROFILE%\Desktop\BISMILAH.lnk" (
    echo.
    echo Shortcut created on Desktop!
) else (
    echo Could not create shortcut
)

echo.
echo ======================================
echo Play BISMILAH!
echo ======================================
start gaame.exe
pause