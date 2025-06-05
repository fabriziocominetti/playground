import os
from dotenv import load_dotenv
import subprocess

# Load environment variables from .env file
load_dotenv()

# Get the API URL from the environment
api_url = os.getenv("PREFECT_API_URL")
if not api_url:
    raise ValueError("PREFECT_API_URL is not set in the environment.")

print(f"Starting Prefect worker with PREFECT_API_URL={api_url}")

# Run the prefect worker start command in the shell
subprocess.run(["prefect", "worker", "start", "--pool", "default-agent-pool"])
