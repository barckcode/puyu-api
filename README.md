# puyu-api

### Set up project:

1. Create a virtual environment: `python3 -m venv .venv`
2. Activate the virtual environment: `source .venv/bin/activate`
3. Install the requirements: `pip install -r api/requirements.txt`
4. Export the following environment variables:
    - `PVE_HOST`
    - `PVE_USER`
    - `PVE_TOKEN_NAME`
    - `PVE_TOKEN_VALUE`
    - `PVE_NODE`
5. Run the API: `fastapi dev api/main.py`
