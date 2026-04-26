@echo off
echo ======================================
echo BISMILAH - Installation
echo ======================================
echo.

:: Создаем ярлык через VBS
echo Set WshShell = CreateObject("WScript.Shell") > temp.vbs
echo Set Shortcut = WshShell.CreateShortcut("%USERPROFILE%\Desktop\BISMILAH.lnk") >> temp.vbs
echo Shortcut.TargetPath = "%~dp0gaame.exe" >> temp.vbs
echo Shortcut.WorkingDirectory = "%~dp0" >> temp.vbs
echo Shortcut.IconLocation = "%~dp0bis.ico" >> temp.vbs
echo Shortcut.Description = "BISMILAH Game" >> temp.vbs
echo Shortcut.Save() >> temp.vbs

:: Запускаем VBS скрытно
cscript //Nologo temp.vbs
del temp.vbs

:: Проверяем
if exist "%USERPROFILE%\Desktop\BISMILAH.lnk" (
    echo [OK] Shortcut created!
) else (
    echo [!] Could not create shortcut
)

echo.
echo ======================================
echo Play BISMILAH!
echo ======================================
start "" "%~dp0gaame.exe"
pause