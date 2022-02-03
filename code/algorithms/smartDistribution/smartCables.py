from cgitb import small
from os import remove
import random
from code.algorithms.smartDistribution.smartCableClimber import *


class GenerateSmartCables():
    """
    Lays cables based on groupings of houses within x radius, making sharing cables more likely.
    """

    def __init__(self, batteries, houses, houseBattery, seed):
        self._batteries = batteries
        self._houses = houses
        self._radius = []
        self._houseBattery = houseBattery
        self._bestBigRadius = None
        self._smallRadius = None
        self._centralPoints = {}
        self._seed = seed
        self.bigRadiusLoop()
        self.radiusClimber = None


    def findCentralPoint(self):
        """
        For each house, connect it to the central point in its radius. First for all small radiuses, 
        then for the big radiuses.
        """

        for bigRadiusID in range(len(self._smallRadius)):
            for smallRadius in self._smallRadius[bigRadiusID]:
                for house in smallRadius:
                    if smallRadius[0] != house and house in self._bestBigRadius[bigRadiusID]:
                        self._centralPoints[house] = smallRadius[0].location
                        self._bestBigRadius[bigRadiusID].remove(house)

        for bigRadius in self._bestBigRadius:
            for house in bigRadius:
                if bigRadius[0] != house:
                    self._centralPoints[house] = bigRadius[0].location
                else:
                    self._centralPoints[house] = self._houseBattery[house].location

        return self._centralPoints


    def returnRadius(self):
        """
        Returns the size of the radius, small or big.
        """
        return [self._smallRadius, self._bestBigRadius]


    def updateCentralPoints(self, radius):
        """
        Retrieves a central point within the small and big radiuses.
        """
        self._bestBigRadius = radius[0]
        self._smallRadius = radius[1]
        return self.findCentralPoint()


    def calculateDistance(self, house, battery):
        """
        Calculates the distance between a battery and house.
        """
        distance = 0
        distance += abs(battery.location[0] - house.location[0])
        distance += abs(battery.location[1] - house.location[1])
        return distance


    def bigRadiusLoop(self):
        """
        Loop through all houses to find an optimal house to be the central point of the houses
        in its radius. Loop until n amount of houses have found a big radius. Loop through that algorithm
        n amount of times, to find the best score of big radiuses.
        """
        bestScore = 9999
        for i in range(100):
            
            # randomise house order, each radius' size and the limit of houses not allowed a radius
            random.seed(self._seed)
            random.shuffle(self._houses)
            
            radius = random.randint(5, 60)
            houseLimit = random.randint(0, 20)
            
            removedItems = []
            radiusHouses = []

            loopAmount = 0
            
            for battery in self._batteries:

                # keep finding radius until enough houses are placed in one, depending on set limit
                while len(self._houses) > houseLimit:
                    loopAmount += 1
                    mostHousesInRadius = self.generateRadius(
                        radius, battery.houses)

                    # remove house that was placed in a radius
                    for house in mostHousesInRadius:
                        removedItems.append(house)
                        battery.houses.remove(house)

                    if len(mostHousesInRadius) > 0:
                        radiusHouses.append(mostHousesInRadius)

                    # make sure the loop doesn't become endless
                    if loopAmount > 20:
                        break

                for item in removedItems:
                    battery.houses.append(item)
                removedItems = []

            # calculate the total proximity to batteries for all central points
            batteryProximity = 0
            for radius in radiusHouses:
                distanceToBattery = self.calculateDistance(
                    mostHousesInRadius[0], self._houseBattery[radius[0]])
                batteryProximity += distanceToBattery

            # calculate current distribution score: the lower the score, the lower the distribution
            score = \
                (len(radiusHouses) * 2) + batteryProximity

            # keep track of the best distribution
            if score < bestScore:
                self._bestBigRadius = radiusHouses
                bestScore = score

        self.smallRadiusLoop()


    def smallRadiusLoop(self):
        """
        Generate a bunch of smaller radiuses inside each big radius, connecting 1-10 houses together
        to lay cables together to the central point of the big radius.
        """
        smallRadius = []

        # loop through all big radiuses
        for bigRadiusID in range(len(self._bestBigRadius)):
            smallRadiusHouses = []
            removedItems = []

            # make sure all houses in the radius get added to a small radius
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


    def returnCentralPoints(self):
        """
        Retrieves the central points from the radiuses within the bigger radius.
        """
        centralPoints = []
        
        for radius in self._bestBigRadius:
            centralPoints.append(radius[0].location)
        return tuple(centralPoints)


    def generateRadius(self, radius, houses):
        """
        Generate the most optimal radius in the houses that are left. The best radius is the
        one with most houses in it.
        """
        mostHousesInRadius = []

        # loop through all houses
        for centralHouse in houses:
            centralPoint = centralHouse.location
            xRadius = []
            yRadius = []
            housesInRadius = [centralHouse]

            # calculate the radius on the x- and y-axis
            for i in range(-radius, radius, 1):
                xRadius.append(centralPoint[0] + i)
                yRadius.append(centralPoint[1] + i)

            xRadius = tuple(xRadius)
            yRadius = tuple(yRadius)

            # find houses in the radius
            for houseInRadius in houses:
                if houseInRadius != centralHouse:
                    if self._houseBattery[houseInRadius] == self._houseBattery[centralHouse]:
                        if houseInRadius.location[0] in xRadius:
                            if houseInRadius.location[1] in yRadius:
                                housesInRadius.append(houseInRadius)

            # keep track of the house with most houses in its radius
            if len(mostHousesInRadius) < len(housesInRadius):
                mostHousesInRadius = housesInRadius

        return mostHousesInRadius
