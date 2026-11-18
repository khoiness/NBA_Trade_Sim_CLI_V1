import subprocess
import sys
from pathlib import Path


def main() -> int:
    """Launch the Streamlit app."""
    app_file = Path(__file__).resolve().parent.parent / "app.py"
    return subprocess.call(
        [sys.executable, "-m", "streamlit", "run", str(app_file)]
    )


__all__ = ["main"]
