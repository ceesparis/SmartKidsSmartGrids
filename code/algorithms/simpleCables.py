from pyrsistent import b
from code.algorithms.randomCables import *


class SimplerCables():
    """
    Add a description for the class
    """

    def __init__(self, batteries, houses, houseBattery):
        self._batteries = batteries
        self._houses = houses
        self._houseBattery = houseBattery
        self._houseLocs = self.getHouseLocs()
        self._bottomHouse = {}
        self._bottomDifference = {}
        self._bottomLeftHouse = {}
        self._bottomLeftHouses = None
        self.findBottomHouse()
        self.findBottomLeftCenter()


    def getHouseLocs(self):
        """
        Add a small description
        """
        houseLocs = {}
        
        for battery in self._batteries:
            houseLocs[battery] = []
            for house in battery.houses:
                houseLocs[battery].append(tuple(house.location))

        return houseLocs


    def getDistance(self, houseLocation, secondLocation):
        """
        Add a small description
        """
        distance = 0
        distance += abs(houseLocation[0] - secondLocation[0])
        distance += abs(houseLocation[1] - secondLocation[1])
        return distance


    def findClosestHouse(self, house, battery):
        """
        Add a small description
        """
        bestDistance = 0

        for location in self._houseLocs[battery]:
            if location != house.location:
                distance = self.getDistance(house.location, location)
                if distance < bestDistance:
                    bestDistance = distance
                    closestLoc = location

        return closestLoc


    def findBottomHouse(self):
        """
        Add a small description
        """
        for battery in self._batteries:
            self._bottomDifference[battery] = []
            lowestY = 0
            batteryY = battery.location[1]
            batteryX = battery.location[0]
            
            for location in self._houseLocs[battery]:
                if batteryY - location[1] > lowestY:
                    if abs(batteryX - location[0]) < 7:
                        lowestY = batteryY - location[1]
                        lowestlocation = location
                        self._bottomDifference[battery] = abs(
                            batteryY - location[1])

            for house in self._houses:
                if house.location == lowestlocation:
                    self._bottomHouse[battery] = house
                    self._bottomDifference[battery] = abs(
                        batteryY - house.location[1])


    def findBottomLeftCenter(self):
        """
        Add a small description
        """
        for battery in self._batteries:
            bestX = 0
            optimalY = self._bottomDifference[battery] / 2
            batteryX = battery.location[0]
            for location in self._houseLocs[battery]:
                if batteryX - location[0] > bestX:
                    if abs(optimalY - location[1]) < 4:
                        bestX = batteryX - location[0]
                        bestLeftlocation = location

            for house in self._houses:
                if house.location == bestLeftlocation:
                    self._bottomLeftHouse[battery] = house

    def findBottomLeftHouses(self):
        """
        Add a small description
        """
        for battery in self._batteries:
            batteryY = battery.location[1]
            batteryX = battery.location[0]
            
            for house in battery.houses:
                if house.location[1] < batteryY and house.location[0] < batteryX:
                    if house.location[1] - self._bottomLeftHouse[battery].location[1] > 0:
                        coordinateY = house.location[1]
                        house.cables = [house.location]
                        
                        while coordinateY != self._bottomLeftHouse[battery].location[1]:
                            coordinateY -= 1
                            house.cables.append(
                                [house.location[0], coordinateY])
                    
                    if house.location[1] - self._bottomLeftHouse[battery].location[1] < 0:
                        coordinateY = house.location[1]
                        house.cables = [house.location]
                        
                        while coordinateY != self._bottomLeftHouse[battery].location[1]:
                            coordinateY += 1
                            house.cables.append(
                                [house.location[0], coordinateY])
