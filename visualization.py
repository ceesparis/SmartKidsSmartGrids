import matplotlib.pyplot as plt
import numpy as np 
from matplotlib.ticker import (MultipleLocator)

def visualize(grid):
    houses_x = []
    houses_y = []
    houses = grid.houses
    for house in houses:
        x = house.location[0]
        y = house.location[1]
        houses_y.append(y)
        houses_x.append(x)
    
    batteries_x = []
    batteries_y = []
    batteries = grid.batteries
    for battery in batteries:
        y = battery.location[0]
        x = battery.location[1]
        batteries_y.append(y)
        batteries_x.append(x)

    fig, ax = plt.subplots()
    ax.scatter(houses_x, houses_y)
    ax.scatter(batteries_x, batteries_y)
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.yaxis.set_minor_locator(MultipleLocator(1))
    ax.grid(b=True, lw=1.1)
    ax.grid(b=True, which='minor')
    plt.show()



