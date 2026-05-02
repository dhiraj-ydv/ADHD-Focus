import subprocess
import sys
import time
import os
import signal

def run():
    print("Starting FocusFlow Launcher...")
    
    while True:
        # Cleanup signals
        if os.path.exists("restart.signal"): os.remove("restart.signal")
        if os.path.exists("stop.signal"): os.remove("stop.signal")
        
        print("Launching Backend and Frontend...")
        backend = subprocess.Popen([sys.executable, "backend/app.py"])
        # Use shell=True for npm on Windows
        frontend = subprocess.Popen(["npm", "run", "dev"], cwd="frontend", shell=True)
        
        should_restart = False
        while True:
            if os.path.exists("restart.signal"):
                print("Restart signal received...")
                should_restart = True
                break
            
            if os.path.exists("stop.signal"):
                print("Stop signal received...")
                should_restart = False
                break
            
            # Check if processes are still running
            if backend.poll() is not None or frontend.poll() is not None:
                print("One of the processes exited unexpectedly.")
                break
                
            time.sleep(1)
        
        print("Cleaning up processes...")
        backend.terminate()
        frontend.terminate()
        
        try:
            backend.wait(timeout=5)
            frontend.wait(timeout=5)
        except subprocess.TimeoutExpired:
            backend.kill()
            frontend.kill()
            
        if not should_restart:
            print("FocusFlow stopped.")
            break
        
        print("Restarting FocusFlow in 2 seconds...")
        time.sleep(2)

if __name__ == "__main__":
    run()
