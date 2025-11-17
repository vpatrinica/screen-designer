# Quick start with uv:
#
# OPTION 1: Using the batch file (Windows)
#   run.bat my_bucket my_token_here fqdn.de 18086
#   run.bat my_bucket my_token_here fqdn.de 18086 --org my_organization --json
#
# OPTION 2: Manual installation and usage
# 
# 1. Install uv (if not already installed):
#    - Via pip: pip install uv
#    - Or download from: https://github.com/astral-sh/uv/releases
#    - Or on Windows via installer from: https://astral.sh/uv
#
# 2. Install dependencies:
#    uv sync
#
# 3. Run the script:
#    uv run query_influxdb.py my_bucket my_token_here fqdn.de 18086
#    uv run query_influxdb.py my_bucket my_token_here fqdn.de 18086 --org my_organization
#    uv run query_influxdb.py my_bucket my_token_here fqdn.de 18086 --json
#
# 4. Or activate the virtual environment:
#    On Windows:
#      .venv\Scripts\activate
#    On Unix/Linux/Mac:
#      source .venv/bin/activate
#    Then run:
#      python query_influxdb.py my_bucket my_token_here fqdn.de 18086
