import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import (MultipleLocator)
import csv


def visualize_exp(csv_file):
    '''
        Takes csv_file.
        Shows visual representation of all results.
    '''

    data = []
    order = []
    i = 0
    with open(csv_file, "r") as f:
        csv_reader = csv.reader(f)
        for line in csv_reader:
            order.append(i)
            line = line[0]
            print(line)
            data.append(int(line))
            i += 1
    data.sort()
    plt.ylim(30000, 40000)
    plt.bar(order, data, width=1)
    plt.show()
    
   