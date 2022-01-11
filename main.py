import loader

class Grid():
    def __init__(self, batteryfile, housefile):
        self.grid = loader.load_grid(batteryfile, housefile)