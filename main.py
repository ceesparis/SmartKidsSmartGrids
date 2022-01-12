import loader
from sys import argv
from visualization import visualize

class Grid():
    def __init__(self, district):
        # load the information from relevant district 
        grid = loader.load_grid(district)
        # specify district of grid
        self.district =  district
        # add batteries of district to grid
        self.batteries = grid[0]
        # add houses of district to grid
        self.houses = grid[1]

if __name__ == "__main__":
    if len(argv) != 2:
        print('Usage: Python3 main.py [district number]')
        exit(1)
    test_district = argv[1]
    try:
        grid = Grid(test_district)
    except Exception:
        print('district not found')
        exit(2)
    visualize(grid)
