# Run query_influxdb.py with uv
# Usage: .\run.ps1 my_bucket my_token fqdn.de 18086

param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Arguments
)

# Change to script directory
Set-Location $PSScriptRoot

# Run with uv
& .\.venv\Scripts\python.exe -m uv run query_influxdb.py @Arguments
