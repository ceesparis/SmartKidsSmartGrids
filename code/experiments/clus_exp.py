import subprocess
import time

def clus_experiment():
    start = time.time()
    n_runs = 0
    while time.time() - start < 1800:
        print(f"run: {n_runs}")
        subprocess.call(["python3", "experiment.py"])
        n_runs += 1