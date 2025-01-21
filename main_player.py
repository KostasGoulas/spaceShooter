import subprocess
import time
import platform
from boot_imp import is_server_open

def open_in_terminal(script_name):
    system = platform.system()
    if system == "Windows":
        # For Windows
        subprocess.Popen(["start", "python", script_name], shell=True)
    elif system == "Darwin":
        # For macOS
        subprocess.Popen(["open", "-a", "Terminal", "python", script_name])
    elif system == "Linux":
        # For Linux
        subprocess.Popen(["gnome-terminal", "--", "python3", script_name])
    else:
        print(f"Unsupported OS: {system}")

if __name__ == "__main__":
    if not is_server_open() :
        # Run a.py
        open_in_terminal("main_server.py")
        time.sleep(7)  # Wait for 7 seconds (or adjust as needed)

    # Run b.py
    open_in_terminal("main.py")
