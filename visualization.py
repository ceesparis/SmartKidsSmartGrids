import matplotlib.pyplot as plt
import numpy as np 
from matplotlib.ticker import (MultipleLocator)

def visualize(grid):
    # make seperate lists for x and y coordinates
    houses_x = []
    houses_y = []
    cables_x = []
    cables_y = []
    houses = grid.houses 
    # make two lists (x and y) for all houses
    for house in houses:
        house_cables_x = []
        house_cables_y = []
        x = house.location[0]
        y = house.location[1]
        houses_y.append(y)
        houses_x.append(x)
        # make two lists (x and y) for every cable 
        for cable in house.cables:
            cab_x = cable[0]
            cab_y = cable[1]
            house_cables_x.append(cab_x)
            house_cables_y.append(cab_y)
        cables_x.append(house_cables_x)
        cables_y.append(house_cables_y)
       
    
    batteries_x = []
    batteries_y = []
    batteries = grid.batteries
    # make two lists (x and y) for all batteries
    for battery in batteries:
        y = battery.location[0]
        x = battery.location[1]
        batteries_y.append(y)
        batteries_x.append(x)

    # make scatter plots for houses and batteries
    fig, ax = plt.subplots()
    ax.scatter(houses_x, houses_y)
    ax.scatter(batteries_x, batteries_y)
    # make line plot for every cable
    for i in range(len(cables_x)):
        ax.plot(cables_x[i], cables_y[i], color='red', lw=0.6)
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.yaxis.set_minor_locator(MultipleLocator(1))
    # show grid
    ax.grid(b=True, lw=1.1)
    ax.grid(b=True, which='minor')
    plt.show()



