from code.classes import loader
import json


class Grid():
    """
    Characteristics and functions for the loaded in neighbourhood grids.
    """

    def __init__(self, district):
        """
            * Loads the information from relevant district
            * Specifies the district of the grid
            * Adds corresponding batteries to the grid
            * Adds corresponding houses to the grid
        """
        self.district = district
        self.batteries = []
        self.houses = []

    def load_from_csv(self):
        """
        Loads the district from the desired/given csv file.
        """
        number = self.district
        grid = loader.load_grid(number)
        self.district = grid[0]
        self.batteries = grid[1]
        self.houses = grid[2]

    def returnHouses(self):
        """
        Returns the grid's house coords.
        """
        return self.houses

    def returnBatteries(self):
        """
        Returns the grid's battery coords.
        """
        return self.batteries

    def addCables(self, house, cableRoute):
        """
        Adds an order of cables to the houses.
        """
        house.cables = cableRoute

    def addHouse(self, batteryID, house):
        """
        When cables connect a house to a battery, the house
        gets appended to a list from the battery.
        """
        self.batteries[batteryID].houses.append(house)

    def printOutput(self):
        """
        Prints the result to the json file.
        """
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
                "ownCosts", "costs-shared") + ', ' + batteryList + ']'

            # print the result in output.json
            with open("output.json", 'w') as f:
                f.write(f"{jsonOutput}")

    def updateCosts(self, costs):
        """
        Updates the district's costs when cables are added.
        """
        self.district.ownCosts = costs
