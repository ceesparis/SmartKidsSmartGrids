from math import dist


class CableClimber():
    def __init__(self, centralPoints, smallRadius, bigRadius, houseBattery):
        self._centralPoints = centralPoints
        self._smallRadius = smallRadius
        self._bigRadius = bigRadius
        self._houseBattery = houseBattery
        self._allCentrals = None

    def calculateDistance(self, houseLocation, centralLocation):
        distance = 0
        distance += abs(houseLocation[0] - centralLocation[0])
        distance += abs(houseLocation[1] - centralLocation[1])
        return distance

    def betterSmall(self):

        centralPoints = {}

        for bigRadiusID in range(len(self._smallRadius)-1):
            centralPoints[bigRadiusID] = []
            for radius in self._smallRadius[bigRadiusID]:
                centralPoints[bigRadiusID].append(radius[0])

        for bigRadiusID in range(len(self._smallRadius)-1):
            for radiusID in range(len(centralPoints)-1):
                for centralPointID in range(len(centralPoints[radiusID])-1):
                    for house in self._smallRadius[radiusID][centralPointID]:
                        currentDistance = self.calculateDistance(
                            house.location, centralPoints[radiusID][centralPointID].location)
                        for centralPointTwoID in range(len(centralPoints)-1):
                            if self._houseBattery[centralPoints[radiusID][centralPointID]] == self._houseBattery[centralPoints[radiusID][centralPointTwoID]]:
                                if currentDistance > self.calculateDistance(house.location, centralPoints[radiusID][centralPointTwoID].location):
                                    self.swapSmallRadius(
                                        house, centralPointTwoID, radiusID, centralPointID)

        return self._smallRadius

    def betterBig(self):
        centralPoints = []
        for radius in self._bigRadius:
            centralPoints.append(radius[0].location)
        self._allCentrals = tuple(centralPoints)

        for centralPointID in range(len(centralPoints)-1):
            for house in self._bigRadius[centralPointID]:
                currentDistance = self.calculateDistance(
                    house.location, centralPoints[centralPointID])
                for centralPointTwoID in range(len(centralPoints)-1):
                    if centralPointID != centralPointTwoID:
                        if currentDistance > self.calculateDistance(house.location, centralPoints[centralPointTwoID]):
                            # print(
                            #     f"current distance: {currentDistance}, new: {self.calculateDistance(house.location, centralPoints[centralPointTwoID])}")
                            self.swapBigRadius(
                                house, centralPointTwoID, centralPointID)

        return self._bigRadius

    def swapSmallRadius(self, house, centralPointTwoID, radiusID, centralPointID):
        self._smallRadius[radiusID][centralPointID].remove(house)
        self._smallRadius[radiusID][centralPointTwoID].append(house)

    def swapBigRadius(self, house, centralPointTwoID, centralPointID):
        if house in self._bigRadius[centralPointID]:
            self._bigRadius[centralPointID].remove(house)
            self._bigRadius[centralPointTwoID].append(house)

    def betterRadiuses(self):
        return [self.betterBig(), self.betterSmall()]

    def returnCentralPoints(self):
        return self._allCentrals
