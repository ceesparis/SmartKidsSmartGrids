import time
from subprocess import PIPE, run

start = time.time()
n_runs = 0
lowestCosts = 100000

with open("smartDistributionResultDis1.txt", 'w') as f:
    while time.time() - start < 60:
        print(f"run: {n_runs}")
        f.write(f"run: {n_runs} \n")

        command = ["python3", "main.py", "1", "SD"]
        result = run(command, stdout=PIPE, stderr=PIPE,
                     universal_newlines=True)

        if result.stdout[0] != "N":

            results = result.stdout.split(" ")
            results = [results[0], results[1].strip("\n")]

            if int(results[0]) < lowestCosts:
                lowestCosts = int(results[0])
                bestSeed = int(results[1])

            f.write(f"result: {results[0]} \n")
            f.write(f"seed: {results[1]} \n")

        else:
            f.write("No valid solution found \n")

        n_runs += 1

    f.write(f"Best Costs: {lowestCosts}, seed: {bestSeed}")
