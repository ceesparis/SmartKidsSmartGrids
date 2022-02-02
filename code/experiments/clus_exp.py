import subprocess
import time
from experiment import experiment

start = time.time()
n_runs = 0
while time.time() - start < 1:
    print(f"run: {n_runs}")
    subprocess.call(["python3", "experiment.py"])
    # experiment()
    n_runs += 1