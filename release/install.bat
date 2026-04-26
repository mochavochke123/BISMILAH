@echo off
echo ======================================
echo BISMILAH - Creating Desktop Shortcut
echo ======================================
echo.

:: Создаем ярлык на рабочем столе
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut([Environment]::GetFolderPath('CommonDesktopDirectory') + '\BISMILAH.lnk'); $Shortcut.TargetPath = '%~dp0gaame.exe'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.Description = 'BISMILAH Game'; $Shortcut.Save()"

if %errorlevel%==0 (
    echo.
    echo Shortcut created on Desktop!
) else (
    echo Error creating shortcut
)

echo.
echo ======================================
echo Play BISMILAH!
echo ======================================
pause