class Node():
    def __init__(self, batteryLocations, location):
        self._coordinates = location
        self._options = None
        self._hasBattery = False
        self.getOptions(location)
        self.checkBattery(batteryLocations)

    def getOptions(self, coordinate):
        optionList = [[coordinate[0] + 1, coordinate[1]], [coordinate[0] - 1, coordinate[1]],
                      [coordinate[0], coordinate[1] - 1], [coordinate[0], coordinate[1] + 1]]

        removeItems = []
        for option in optionList:
            for coordinate in option:
                if coordinate > 50 or coordinate < 0:
                    removeItems.append(option)

        for item in removeItems:
            optionList.remove(item)

        self._options = optionList

    def checkBattery(self, batteryLocations):
        for location in batteryLocations:
            if location == self._coordinates:
                self._hasBattery = True

    def printOptions(self):
        print(self._options)
