import loader
from randomCables import *
from costCalculation import *
from sys import argv
from visualization import visualize
import json
from distanceCalc import calc_distance
from randomizer import randomizer
from grid import Grid



if __name__ == "__main__":
    if len(argv) != 2:
        print('Usage: Python3 main.py [district number]')
        exit(1)
    district = argv[1]
    try:
        grid = Grid(district)
        grid.load_from_csv()
    except Exception:
        print('district not found')
        exit(2)


    # random_algorithm
    random_grid = randomizer(grid)
    grids = random_grid.multiple_random()
    random_grid.calc_average(grids)