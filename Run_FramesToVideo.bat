@ECHO OFF

cd /d %~dp0
"%~dp0Python34\python.exe" "%~dp0AutoUpload.py" %* 
PAUSE