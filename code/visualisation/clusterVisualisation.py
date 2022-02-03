import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import (MultipleLocator)


def visualize(grid):
    """
        Takes grid.
        Shows visual representation of grid.
    """

    # make seperate lists for x and y coordinates
    housesX = []
    housesY = []
    cablesX = []
    cablesY = []
    houses = grid.houses
    cableColour = []
    colors = ['red', 'green', 'blue', 'yellow', 'black']

    # make two lists (x and y) for all houses
    for house in houses:
        houseCablesX = []
        houseCablesY = []
        x = house.location[0]
        y = house.location[1]
        housesY.append(y)
        housesX.append(x)

        # make two lists (x and y) for every cable
        for cable in house.cables:
            cableX = cable[0]
            cableY = cable[1]
            houseCablesX.append(cableX)
            houseCablesY.append(cableY)
        cablesX.append(houseCablesX)
        cablesY.append(houseCablesY)

        for batteryID in range(len(grid.batteries)):
            if batteryID:
                for houseBattery in grid.batteries[batteryID].houses:
                    if house == houseBattery:
                        cableColour.append(colors[batteryID])
            else: 
                cableColour.append(colors[0])

    batteriesX = []
    batteriesY = []
    batteries = grid.batteries

    # make two lists (x and y) for all batteries
    for battery in batteries:
        y = battery.location[1]
        x = battery.location[0]
        batteriesY.append(y)
        batteriesX.append(x)

    # make scatter plots for houses and batteries
    fig, ax = plt.subplots()
    ax.scatter(housesX, housesY)
    ax.scatter(batteriesX, batteriesY)
    # make line plot for every cable
    for i in range(len(cablesX)):
        ax.plot(cablesX[i], cablesY[i], color=cableColour[i], lw=0.6)
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.yaxis.set_minor_locator(MultipleLocator(1))

    # show grid
    ax.grid(b=True, lw=1.1)
    ax.grid(b=True, which='minor')

    plt.plot(range(10))
    fig.savefig('./grid.png', dpi=fig.dpi)
