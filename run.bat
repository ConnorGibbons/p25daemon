@echo off
cd /d %~dp0

echo [INFO] Running P25 Daemon via conda...
call C:\ProgramData\miniconda3\condabin\conda.bat run -n whisperEnv python -m src.p25daemon

echo [INFO] Script complete.
pause
