import loader
from randomCables import *
from costCalculation import *
from sys import argv
from visualization import visualize


class Grid():
    def __init__(self, district):
        # load the information from relevant district
        grid = loader.load_grid(district)
        # specify district of grid
        self.district = grid[0]
        # add batteries of district to grid
        self.batteries = grid[1]
        # add houses of district to grid
        self.houses = grid[2]

    def returnHouses(self):
        return self.houses

    def returnBatteries(self):
        return self.batteries

    def updateBatteryPow(self, powerUsed, batteryID):
        self.batteries[batteryID].power = self.batteries[batteryID].power - powerUsed

    def addCables(self, houseID, cableRoute):
        self.houses[houseID].cables = cableRoute

    def printOutput(self):
        with open('output.json', 'w') as f:
            f.write(f"{vars(self.district)}")
            f.write(f"{vars(self.houses)}")


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

    # declare the houses and batteries using the grid class
    houses = grid.returnHouses()
    batteries = grid.returnBatteries()
    batteryID = 4
    houseID = 0

    # loop through every house in the district
    for house in houses:
        # check if the capacity of a battery has been reached, if so, change to a new battery
        if batteries[batteryID].power < house.power:
            batteryID -= 1

        # generate the route of the cable from a house to a battery
        cableRoute = randomizeCables(
            house.location, batteries[batteryID].location)

        # update the grid
        grid.updateBatteryPow(house.power, batteryID)
        grid.addCables(houseID, cableRoute)
        houseID += 1

    for house in houses:
        print(house.cables[len(house.cables) - 1])

    # calculate the costs, print them out and save them
    completeCosts = calculateCost(houses, len(batteries))
    print(f"The costs of this smartgrid are: €{completeCosts},-")
    visualize(grid)
