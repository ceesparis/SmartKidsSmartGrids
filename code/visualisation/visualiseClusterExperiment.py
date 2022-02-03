import matplotlib.pyplot as plt
import numpy as np
import csv


def visualizeExp(csvFile, district):
    """
        Takes csv file.
        Shows visual representation of all results.
    """

    data = []
    order = []
    
    i = 0
    
    with open(csvFile, "r") as f:
        csvReader = csv.reader(f)
        for line in csvReader:
            order.append(i)
            line = line[0]
            print(line)
            data.append(int(line))
            i += 1
    
    data.sort()
    
    plt.ylim(30000, 40000)
    plt.bar(order, data, width=1)
    plt.xlabel("number of grids")
    plt.ylabel("grid costs")
    plt.savefig(f"./data/experiments/sharedcables/cluster_experiment_district_{district}.png")
    
   