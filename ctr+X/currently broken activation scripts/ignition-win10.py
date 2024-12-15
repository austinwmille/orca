import subprocess
import os

def activate_and_run(env_path, script_path):
    if os.name == 'nt':  # Windows
        activate_script = os.path.join(env_path, 'Scripts', 'activate.bat')
        full_command = f'cmd.exe /k "{activate_script} && python {script_path}"'
    else:  # Linux/macOS
        activate_script = os.path.join(env_path, 'bin', 'activate')
        full_command = f'bash -c "source {activate_script} && python {script_path}"'
    
    # Start a subprocess to activate environment and run script
    process = subprocess.Popen(full_command, shell=True)
    process.wait()  # Wait for script completion

# Define your virtual environment and script paths
env_path = "cliaenv"
script_path = "clipmev2.py"

activate_and_run(env_path, script_path)
