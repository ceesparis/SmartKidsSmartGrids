from math import dist


class CableClimber():
    """
    This hillclimber will slowly improve the radiusses that have been made before.
    """

    def __init__(self, centralPoints, smallRadius, bigRadius, houseBattery):
        self._centralPoints = centralPoints
        self._smallRadius = smallRadius
        self._bigRadius = bigRadius
        self._houseBattery = houseBattery
        self._allCentrals = None

    def calculateDistance(self, houseLocation, centralLocation):
        """
        Calculate the distance from a house to a central locatiom
        """
        distance = 0
        distance += abs(houseLocation[0] - centralLocation[0])
        distance += abs(houseLocation[1] - centralLocation[1])
        return distance

    def betterSmall(self):
        """
        Generate better small radiusses by comparing each house to another central point
        """
        centralPoints = {}

        # add all central points connecting to a battery in a dict
        for bigRadiusID in range(len(self._smallRadius)-1):
            centralPoints[bigRadiusID] = []
            for radius in self._smallRadius[bigRadiusID]:
                centralPoints[bigRadiusID].append(radius[0])

        # loop through all houses in each small radius
        for bigRadiusID in range(len(self._smallRadius)-1):
            for radiusID in range(len(centralPoints)-1):
                for centralPointID in range(len(centralPoints[radiusID])-1):
                    for house in self._smallRadius[radiusID][centralPointID]:
                        # compare if the distance will be improved by swapping to a new central point
                        currentDistance = self.calculateDistance(
                            house.location, centralPoints[radiusID][centralPointID].location)
                        for centralPointTwoID in range(len(centralPoints)-1):
                            if self._houseBattery[centralPoints[radiusID][centralPointID]] == self._houseBattery[centralPoints[radiusID][centralPointTwoID]]:
                                if currentDistance > self.calculateDistance(house.location, centralPoints[radiusID][centralPointTwoID].location):
                                    self.swapSmallRadius(
                                        house, centralPointTwoID, radiusID, centralPointID)

        return self._smallRadius

    def betterBig(self):
        """
        Generate better big radiusses
        """
        centralPoints = []

        # add all central points of each battery together
        for radius in self._bigRadius:
            centralPoints.append(radius[0].location)
        self._allCentrals = tuple(centralPoints)

        # loop through all houses in each big radius
        for centralPointID in range(len(centralPoints)-1):
            for house in self._bigRadius[centralPointID]:
                # compare the distance to the current central point to a new central point
                currentDistance = self.calculateDistance(
                    house.location, centralPoints[centralPointID])
                for centralPointTwoID in range(len(centralPoints)-1):
                    if centralPointID != centralPointTwoID:
                        if currentDistance > self.calculateDistance(house.location, centralPoints[centralPointTwoID]):
                            self.swapBigRadius(
                                house, centralPointTwoID, centralPointID)

        return self._bigRadius

    def swapSmallRadius(self, house, centralPointTwoID, radiusID, centralPointID):
        """
        Perform the swap to a new small radius
        """
        self._smallRadius[radiusID][centralPointID].remove(house)
        self._smallRadius[radiusID][centralPointTwoID].append(house)

    def swapBigRadius(self, house, centralPointTwoID, centralPointID):
        """
        Perform the swap to a new big radius
        """
        if house in self._bigRadius[centralPointID]:
            self._bigRadius[centralPointID].remove(house)
            self._bigRadius[centralPointTwoID].append(house)

    def betterRadiuses(self):
        """
        Return the improved radiusses
        """
        return [self.betterBig(), self.betterSmall()]

    def returnCentralPoints(self):
        return self._allCentrals
