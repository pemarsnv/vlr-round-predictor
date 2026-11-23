import os
import subprocess
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

import data_fetcher

API_DIR = Path(__file__).resolve().parent / "vlrggapi"
API_PYTHON = API_DIR / ".venv" / (
    "Scripts/python.exe" if os.name == "nt" else "bin/python"
)
API_URL = "http://127.0.0.1:3001"

def main():
    api = subprocess.Popen(
        [
            str(API_PYTHON), "-m", "uvicorn", "main:app",
            "--host", "127.0.0.1", "--port", "3001",
        ],
        cwd=API_DIR,
     )
    try:
        # start the vlrggapi
        wait_for_api(api)
        # start data retrieval
        if os.path.exists("rounds.csv"):
            os.remove("rounds.csv")
        data_fetcher.retrieve_rounds()
    finally:
        if api.poll() is None:
            api.terminate()
            try:
                api.wait(timeout=5)
            except subprocess.TimeoutExpired:
                api.kill()
                api.wait()


def wait_for_api(api):
    deadline = time.monotonic() + 20
    while time.monotonic() < deadline:
        if api.poll() is not None:
            raise RuntimeError(f"vlrggapi exited with code {api.returncode}")

        try:
            with urlopen(f"{API_URL}/version", timeout=1):
                return
        except (URLError, TimeoutError):
            time.sleep(0.25)

    raise TimeoutError(f"vlrggapi did not start at {API_URL}")


if __name__ == "__main__":
    main()
