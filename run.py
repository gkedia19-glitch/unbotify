"""
Unbotify Unified Launcher.
Tagline: "Less formula. More expression."
Launch the modern Streamlit Web Application, the FastAPI Enterprise server, or the CLI.

Usage:
  python run.py            # Starts the Unbotify Web Studio
  python run.py --api      # Starts the Unbotify Enterprise REST API (port 8000)
  python run.py --cli ...  # Executes the Unbotify CLI
"""

import sys
import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    if "--api" in sys.argv:
        print("🚀 Starting Unbotify Enterprise REST API on http://127.0.0.1:8000...")
        import uvicorn
        sys.path.insert(0, os.path.join(BASE_DIR, "src"))
        uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
    elif "--cli" in sys.argv:
        sys.argv.remove("--cli")
        import cli
        cli.main()
    else:
        app_path = os.path.join(BASE_DIR, "app.py")
        print("🚀 Launching Unbotify Web Studio on http://localhost:8501...")
        cmd = [sys.executable, "-m", "streamlit", "run", app_path]
        subprocess.run(cmd)

if __name__ == "__main__":
    main()
