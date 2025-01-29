import os
import sys
import subprocess
from utils import installPrereq

#checking and installing any prerequites/dependencies
installPrereq()

def run_app():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    #constructing path to story gen file
    app_path = os.path.join(current_dir, "ui.py")

    if not os.path.isfile(app_path):
        print(f"!! ERROR: The file {app_path} does not exist !!")
        return

    try:
        print(f"Launching system at: {app_path}")
        subprocess.run([sys.executable, "-m", "streamlit", "run", app_path], check=True)
    except Exception as e:
        print(f"!! ERROR: Failed to launch system with exception: {e}")

if __name__ == "__main__":
    run_app()