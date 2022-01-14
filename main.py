import loader
from randomCables import *
from costCalculation import *
from sys import argv
from visualization import visualize
import json
from distanceCalc import calc_distance


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

    def addCables(self, house, cableRoute):
        house.cables = cableRoute

    def addHouse(self, batteryID, house):
        self.batteries[batteryID].houses.append(house)

    # print the result to the json file
    def printOutput(self):
        # convert the district class to json
        jsonStringDistrict = json.dumps(
            self.district, default=lambda o: o.__dict__).replace("\\", "")

        batteryList = ''

        # loop through all batteries to convert their contents to the json format
        for battery in self.batteries:
            # convert the location list to a string containing the coordinates
            battery.location = ','.join(map(str, battery.location))
            for house in battery.houses:
                house.location = ','.join(map(str, house.location))
                # make a new list that will be filled with all coordinates in a string format
                newCableList = []
                for cable in house.cables:
                    newCable = ','.join(map(str, cable))
                    newCableList.append(newCable)
                house.cables = newCableList
            # convert the battery class to the json format
            jsonString = json.dumps(
                battery, default=lambda o: o.__dict__).replace("\\", "")
            # add the battery to the list of all batteries
            if batteryList == '':
                batteryList = jsonString
            else:
                batteryList = batteryList + ", " + jsonString

            # put the district and batteries together, adding some syntax for the json file
            jsonOutput = '[' + jsonStringDistrict.replace(
                "ownCosts", "costs-own") + ', ' + batteryList + ']'

            # print the result in output.json
            with open("output.json", 'w') as f:
                f.write(f"{jsonOutput}")

    def updateCosts(self, costs):
        self.district.ownCosts = costs


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
    batteryID = 0
    houseID = 0
    capacity = batteries[0].capacity

    # loop through every house in the district
    for house in houses:
        # check if the capacity of a battery has been reached, if so, change to a new battery
        if capacity < house.output:
            batteryID += 1
            capacity = batteries[batteryID].capacity

        # generate the route of the cable from a house to a battery
        cableRoute = randomizeCables(
            house.location, batteries[batteryID].location)

        # update the grid
        capacity = capacity - house.output
        grid.addCables(house, cableRoute)
        grid.addHouse(batteryID, house)
        houseID += 1

        # battery capacity will be reached if all houses get a battery, remove later
        if houseID == 147:
            break

    # calculate the costs, print them out and save them
    completeCosts = calculateCost(houses, len(batteries))
    print(f"The costs of this smartgrid are: €{completeCosts},-")
    
    visualize(grid)
