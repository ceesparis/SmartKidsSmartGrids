from code.algorithms.randomCables import randomizeCables


class ClimbConnections():
    """
    Add a description for the class!
    """

    def __init__(self, batteries, houses, centralPoints, allCentrals, batteryHouses):
        self._batteries = batteries
        self._houses = houses
        self._centralPoints = centralPoints
        self._allCentrals = allCentrals
        self._batteryLocs = []
        self._batteryHouses = batteryHouses
        self.findBatteries()


    def findBatteries(self):
        """Add a small description"""
        for battery in self._batteries:
            self._batteryLocs.append(tuple(battery.location))

        self._batteryLocs = tuple(self._batteryLocs)


    def calculateDistance(self, houseLocation, secondLocation):
        """Add a small description"""
        distance = 0
        distance += abs(houseLocation[0] - secondLocation[0])
        distance += abs(houseLocation[1] - secondLocation[1])
        return distance


    def findConnections(self):
        """Add a small description"""
        cableTuples = {}

        # Add tuple of all cables for each battery
        for battery in self._batteries:
            for house in battery.houses:
                cableTuples[battery] = tuple(map(tuple, house.cables))

        # Loop through all batteries
        for battery in self._batteries:
            lockedHouses = set()

            # Loop through all houses
            for houseOne in battery.houses:
                
                if tuple(houseOne.location) in self._allCentrals:
                    continue
                
                if houseOne in lockedHouses:
                    continue
                
                bestImprovement = 0
                cableHouseOne = None
                coordinateCableTwo = None
                
                # Calculate the distance from the house to the central point
                if houseOne in self._centralPoints:
                    distanceCentral = self.calculateDistance(
                        houseOne.location, self._centralPoints[houseOne])
                else:
                    distanceCentral = self.calculateDistance(
                        houseOne.location, self._batteryHouses[houseOne].location)
                
                # Loop through all cables from this house
                for cableOne in houseOne.cables:
                    distanceCentral -= 1
                    
                    # See if there's other houses coords closer to the battery than this house's distance
                    for i in range((-distanceCentral - 1), (distanceCentral - 1), 1):
                        for j in range(-distanceCentral, distanceCentral, 1):
                            if ((cableOne[0] + i), (cableOne[1]) + j) in cableTuples[battery]:
                                distanceCable = self.calculateDistance(
                                    cableOne, ((cableOne[0] + i), (cableOne[1]) + j))
                                distanceImprovement = distanceCentral - distanceCable
                                
                                # If smaller, save current coord's index, the other cable's coord, and the difference between the two
                                if distanceImprovement > bestImprovement:
                                    if ((cableOne[0] + i), (cableOne[1]) + j) not in self._batteryLocs:
                                        bestImprovement = distanceImprovement
                                        coordinateCableTwo = (
                                            (cableOne[0] + i), (cableOne[1]) + j)
                                        cableHouseOne = cableOne
                                        secondCentral = coordinateCableTwo

                if coordinateCableTwo != None:
                    indexCable = houseOne.cables.index(
                        list(cableHouseOne)) + 1

                    houseOne.cables = houseOne.cables[:indexCable]
                    
                    pathToNew = randomizeCables(
                        houseOne.location, [coordinateCableTwo[0], coordinateCableTwo[1]])
                    pathToGattery = randomizeCables(
                        [coordinateCableTwo[0], coordinateCableTwo[1]], self._batteryHouses[houseOne].location)
                    houseOne.cables = pathToNew + pathToGattery

                    # Remove everything other than the best index, and make a path to the other cable's coords
                    for house in battery.houses:
                        if house != houseOne:
                            if secondCentral in tuple(map(tuple, house.cables)):
                                lockedHouses.add(house)
                                break
