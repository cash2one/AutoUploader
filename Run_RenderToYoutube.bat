@ECHO OFF
cd /d %~dp0
"%~dp0Python27\python.exe" "%~dp0AutoUpload.py" %* -upload
PAUSE