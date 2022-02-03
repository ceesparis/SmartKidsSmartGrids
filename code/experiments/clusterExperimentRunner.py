import subprocess
import time

def clusExperiment():
    """
    The script used to run the experiment for our cluster algorithm.
    """
    start = time.time()
    n_runs = 0
    
    while time.time() - start < 1800:
        print(f"run: {n_runs}")
        subprocess.call(["python3", "experiment.py"])
        n_runs += 1