import sys
from pathlib import Path

# Ensure the project root (containing `backend`) is on sys.path
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from backend.main import run_console_app


if __name__ == "__main__":
    run_console_app()
