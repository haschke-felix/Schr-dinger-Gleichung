@echo off

SET mypath=%~dp0
reg Query "HKLM\Hardware\Description\System\CentralProcessor\0" | find /i "x86" > NUL && set OS=32BIT || set OS=64BIT

mkdir temp

SET /P AREYOUSURE1=Did you had problems? (Y/[N])?
IF /I "%AREYOUSURE1%" NEQ "Y" GOTO PROMPT ELSE GOTO PROBLEMS

:PROBLEMS
echo select Problem
echo 1: need PS1 for Windows 7
echo 2: need update for Windows 7
echo 3: no Problem
set /p id="Problem: "
IF %id% == 1 (
	IF %OS%==64BIT (
		"%mypath%/curl.exe" -k "https://securedl.cdn.chip.de/downloads/9694911/windows6.1-KB976932-X64.exe?cid=54475724&platform=chip&1642250347-1642257847-39c65c-B-ed8db05ac777d6af4a89f6c68a3d4437.exe" -o "./temp/Windows7SP1.exe"
	) ELSE (
		"%mypath%/curl.exe" -k "https://securedl.cdn.chip.de/downloads/8815485/windows6.1-KB976932-x86.exe?cid=54468118&platform=chip&1642251400-1642258900-30dbf-B-16722449e612d9b460939604cd56e10a.exe" -o "./temp/Windows7SP1.exe"
	)
	"%mypath%/temp/Windows7SP1.exe"
)
IF %id% == 2 (
	IF %OS%==64BIT (
		"%mypath%/curl.exe" -k "https://download.microsoft.com/download/0/8/E/08E0386B-F6AF-4651-8D1B-C0A95D2731F0/Windows6.1-KB3063858-x64.msu" -o "./temp/Windows6.1-KB3063858.msu"
	) ELSE (
		"%mypath%/curl.exe" -k "https://download.microsoft.com/download/C/9/6/C96CD606-3E05-4E1C-B201-51211AE80B1E/Windows6.1-KB3063858-x86.msu" -o "./temp/Windows6.1-KB3063858.msu"
	)
	"%mypath%/temp/Windows6.1-KB3063858.msu"
)
IF %id% == 3 (
	GOTO PROMPT
)
GOTO PROBLEMS

:PROMPT
echo start the instalation?
SET /P AREYOUSURE1=Are you sure (Y/[N])?
IF /I "%AREYOUSURE1%" NEQ "Y" GOTO END

echo starting the installation process

::installing python
py --version>NUL
if errorlevel 1 (
	"%mypath%/curl.exe" -k "https://www.python.org/ftp/python/3.8.6/python-3.8.6.exe" -o "./temp/pythonInstall.exe"
	"%mypath%/temp/pythonInstall.exe"
) ELSE (
	echo python already installed
)
"%mypath%/curl.exe" -k -L "https://github.com/haschke-felix/Schr-dinger-Gleichung/releases/latest/download/checkPython.py" -o "./temp/checkPython.py"
for /f "delims=" %%i in ('py ./temp/checkPython.py') do set RESULT=%%i
echo The directory is %RESULT%

::download 7zip
"%mypath%/curl.exe" -k -L "https://github.com/haschke-felix/Schr-dinger-Gleichung/releases/latest/download/7za.exe" -o "./temp/7za.exe"
"%mypath%/curl.exe" -k -L "https://github.com/haschke-felix/Schr-dinger-Gleichung/releases/latest/download/7za.exe" -o "./temp/7z.dll"

::download the latest Version of Schr-dinger
"%mypath%/curl.exe" -k -L "https://github.com/haschke-felix/Schr-dinger-Gleichung/releases/latest/download/main.zip" -o "main.zip"
echo please accept override, when ask for!!!
"%mypath%/temp/7za.exe" x "%mypath%/main.zip" -o"%mypath%/"

::pip install
cd "%RESULT%\Scripts"
pip>NUL
if errorlevel 1 (
	cd "%mypath%"
	"%mypath%/curl.exe" -k "https://bootstrap.pypa.io/get-pip.py" -o "./temp/get-pip.py"
	py ./temp/get-pip.py
) ELSE (
	echo pip already installed
)
cd "%RESULT%\Scripts"
pip install -r "%mypath%/requirements.txt"
cd "%mypath%"

::remove temp
echo please accept deletion
rmdir /s temp
:END