import loader

class Grid():
    def __init__(self, district):
        self.grid = loader.load_grid(district)

if __name__ == "__main__":
    test_district = 1
    grid = Grid(test_district)
print(grid)