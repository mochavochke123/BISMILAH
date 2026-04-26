@echo off
echo ======================================
echo BISMILAH - Creating Desktop Shortcut
echo ======================================
echo.

:: Создаем ярлык на рабочем столе текущего пользователя
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\BISMILAH.lnk'); $Shortcut.TargetPath = '%~dp0gaame.exe'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.Description = 'BISMILAH Game'; $Shortcut.Save()"

:: Если не получилось, пробуем в папку с игрой
if %errorlevel% neq 0 (
    echo Trying alternative location...
    copy /y "%~dp0gaame.exe" "%~dp0BISMILAH.exe" >nul
    echo Created BISMILAH.exe in game folder!
)

echo.
echo ======================================
echo Play BISMILAH!
echo ======================================
start gaame.exe
pause