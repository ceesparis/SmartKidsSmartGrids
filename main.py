import loader

class Grid():
    def __init__(self, district):
        # load the information from relevant district 
        grid = loader.load_grid(district)
        # add batteries of district to grid
        self.batteries = grid[0]
        # add houses of district to grid
        self.houses = grid[1]

if __name__ == "__main__":
    test_district = 1
    grid = Grid(test_district)
print(grid.batteries)