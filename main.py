import subprocess

def run_script(script_name):
    try:
        subprocess.run(["python", script_name], check=True)
    except subprocess.CalledProcessError:
        print(f"Error running {script_name}")

# Run scripts sequentially
run_script("VideoGenerator.py")
run_script("srtGenerator.py")
run_script("ytUploader.py")
