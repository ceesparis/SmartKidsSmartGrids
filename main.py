
import code.classes.loader
from sys import argv
from code.classes.randomizer import Randomizer
from code.classes.grid import Grid
from distributeLoop import iterateDistribution

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

    loops = 25
    grid = iterateDistribution(grid, loops)
    grid.printOutput()

    # random_algorithm
    # random_grid = Randomizer(grid)
    # grids = random_grid.multiple_random()
    # random_grid.calc_average(grids)
