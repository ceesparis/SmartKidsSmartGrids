from cgitb import small
import random


class GenerateSmartCables():
    def __init__(self, batteries, houses, houseBattery):
        self._batteries = batteries
        self._houses = houses
        self._radius = []
        self._houseBattery = houseBattery
        self._bestBigRadius = None
        self._smallRadius = None
        self._centralPoints = {}
        self.bigRadiusLoop()

    def findCentralPoint(self):

        # print(f"Amound of big radius: {len(self._bestBigRadius)}")
        amount = 0
        housesAmount = 0
        for bigRadiusID in range(len(self._smallRadius)):
            for smallRadius in self._smallRadius[bigRadiusID]:
                amount += 1
                for house in smallRadius:
                    housesAmount += 1
        # print(f"Amount of small radius: {amount}")
        # print(f"Amount of houses: {housesAmount}")

        housesAdded = 0

        for bigRadiusID in range(len(self._smallRadius)):
            for smallRadius in self._smallRadius[bigRadiusID]:
                for house in smallRadius:
                    if smallRadius[0] != house and house in self._bestBigRadius[bigRadiusID]:
                        self._centralPoints[house] = smallRadius[0].location
                        self._bestBigRadius[bigRadiusID].remove(house)
                        housesAdded += 1

        for bigRadius in self._bestBigRadius:
            for house in bigRadius:
                if bigRadius[0] != house:
                    self._centralPoints[house] = bigRadius[0].location
                    housesAdded += 1
                else:
                    self._centralPoints[house] = self._houseBattery[house].location
                    housesAdded += 1

        # print(f"amount of houses added {housesAdded}")

        return self._centralPoints

    def calculateDistance(self, house, battery):
        distance = 0
        distance += abs(battery.location[0] - house.location[0])
        distance += abs(battery.location[1] - house.location[1])
        return distance

    def bigRadiusLoop(self):
        bestScore = 9999
        for i in range(100):
            random.shuffle(self._houses)
            radius = random.randint(15, 60)
            houseLimit = random.randint(50, 80)
            removedItems = []
            radiusHouses = []

            loopAmount = 0
            while len(self._houses) > houseLimit:
                loopAmount += 1
                mostHousesInRadius = self.generateRadius(radius, self._houses)
                for house in mostHousesInRadius:
                    if house in self._houses:
                        removedItems.append(house)
                        self._houses.remove(house)
                    else:
                        mostHousesInRadius.remove(house)
                radiusHouses.append(mostHousesInRadius)
                if loopAmount > 20:
                    break

            distanceToBattery = self.calculateDistance(
                mostHousesInRadius[0], self._houseBattery[mostHousesInRadius[0]])

            score = len(self._houses) + (len(radiusHouses) * 2) + \
                (distanceToBattery * 3)

            if score < bestScore:
                self._bestBigRadius = radiusHouses
                bestScore = score

            for item in removedItems:
                self._houses.append(item)

        self.smallRadiusLoop()

    def smallRadiusLoop(self):
        smallRadius = []

        for bigRadiusID in range(len(self._bestBigRadius)):
            smallRadiusHouses = []
            removedItems = []
            while len(self._bestBigRadius[bigRadiusID]) > 0:
                bestSmallRadius = self.generateRadius(
                    4, self._bestBigRadius[bigRadiusID])
                for house in bestSmallRadius:
                    self._bestBigRadius[bigRadiusID].remove(house)
                    removedItems.append(house)
                smallRadiusHouses.append(bestSmallRadius)
            self._bestBigRadius[bigRadiusID] = removedItems
            smallRadius.append(smallRadiusHouses)
        self._smallRadius = smallRadius

        # print(self._smallRadius)

    def generateRadius(self, radius, houses):
        mostHousesInRadius = []

        for centralHouse in houses:
            centralPoint = centralHouse.location
            xRadius = []
            yRadius = []
            housesInRadius = [centralHouse]

            for i in range(-radius, radius, 1):
                xRadius.append(centralPoint[0] + i)
                yRadius.append(centralPoint[1] + i)

            xRadius = tuple(xRadius)
            yRadius = tuple(yRadius)

            for houseInRadius in houses:
                if houseInRadius != centralHouse:
                    if self._houseBattery[houseInRadius] == self._houseBattery[centralHouse]:
                        if houseInRadius.location[0] in xRadius:
                            if houseInRadius.location[1] in yRadius:
                                housesInRadius.append(houseInRadius)

            if len(mostHousesInRadius) < len(housesInRadius):
                mostHousesInRadius = housesInRadius

        return mostHousesInRadius
