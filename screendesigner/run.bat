@echo off
REM Quick run script for query_influxdb.py using uv

setlocal enabledelayedexpansion

cd /d "%~dp0"

REM Try to sync with uv
python -m uv sync >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo Running with uv...
    python -m uv run query_influxdb.py %*
) else (
    echo uv sync not available, running directly...
    python query_influxdb.py %*
)
