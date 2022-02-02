import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import (MultipleLocator)
import csv


def visualize(csv_file):
    '''
        Takes grid.
        Shows visual representation of grid.
    '''

    data = []
    order = []
    i = 0
    with open(csv_file, "r") as f:
        csv_reader = csv.reader(f)
    for line in csv_reader:
        order.append(i)
        data.append(line)
        i += 1
    plt.bar(order, data)
   