from os import close, replace
from astarNodes import Node
import copy
import random
from astarHill import astarHillClimber


class astar():
    def __init__(self, houses, batteries):
        self._houses = houses
        self._batteries = batteries
        self._batteryProx = {}
        self._result = None
        self._capacities = None
        self._allDistances = {}
        self.fillCapacity()
        self.getDistances()
        self.findBattery()

    def getDistances(self):
        # dictionary of all the houses containing the closest batteries
        batteryDict = {}

        # dictionary of all houses containing the difference between the closest and the second closest battery
        distanceDict = {}

        # loop through all houses
        for house in self._houses:
            minimalDistance = 999999
            # list of all distances from a house to a battery
            distanceList = []

            # loop through all batteries
            for battery in self._batteries:
                distance = 0

                # check the distances of houses to batteries by adding the difference on the x-axis to the
                # difference on the y-axis
                distance += abs(battery.location[0] - house.location[0])
                distance += abs(battery.location[1] - house.location[1])

                # check if the distance for this battery is less than the closest battery till now
                if minimalDistance > distance:
                    minimalDistance = distance
                    closestBattery = battery

                distanceList.append(distance)

            # add the battery that is closest to the dictionary
            batteryDict[house] = closestBattery

            # save the distances to each battery in the class
            self._batteryProx[house] = copy.deepcopy(distanceList)
            self._allDistances[house] = copy.deepcopy(distanceList)

            # sort the distances from in descending order
            distanceList.sort()

            # add the difference between the shortest and second shortest distance to a battery
            distanceDict[house] = distanceList[1] - distanceList[0]

        # call function that removes the houses that should get priority
        self.closestHouses(distanceDict, batteryDict)

    def closestHouses(self, distanceDict, batteryDict):

        # sort the difference between the distances of the batteries in descending order
        distancesSorted = dict(
            sorted(distanceDict.items(), key=lambda item: item[1], reverse=True))

        # a list containing all houses that have the highest distance between closest batteries
        priorityHouses = []
        i = 0
        randomLimit = random.randint(0, 150)

        # add fifty houses to the priority list
        for house in distancesSorted:
            priorityHouses.append(house)
            i += 1
            if i == randomLimit:
                break

        # dictionary containing all houses with their closest batteries
        topHouses = {}

        # remove all houses that have been prioritized from the houses list and store them
        # in the topHouses dictionary
        for houseID in range(len(priorityHouses)):
            # check if the capacity has not yet been reached
            if self._capacities[batteryDict[priorityHouses[houseID]]] - priorityHouses[houseID].output > 0:
                topHouses[priorityHouses[houseID]] = batteryDict.pop(
                    priorityHouses[houseID])
                self._batteryProx.pop(priorityHouses[houseID])
                self._capacities[topHouses[priorityHouses[houseID]]
                                 ] -= priorityHouses[houseID].output

        # add the first results to the class
        self._result = topHouses

    # fill the nodes to allow smarter path finding (not yet used)
    def fillNodes(self):
        batteryLocations = []
        for battery in self._batteries:
            batteryLocations.append(battery.location)

        nodeList = []
        for i in range(50):
            for j in range(50):
                newNode = Node(batteryLocations, [i, j])
                nodeList.append(newNode)

    def initialDistribution(self, houseBattery, house):
        # set the closest distance to a battery mber higher than any distance possible
        closestDistance = 9999
        # this will keep track of which battery is closest to the house
        batteryPicked = None
        previousDistance = closestDistance

        # loop through all distances stored in the batteryProx dictionary
        for batteryID in range(len(self._batteryProx[house])):

            # check if the distance to the current battery is closer than the closest so far
            if self._batteryProx[house][batteryID] < closestDistance:

                # keep track of which battery is closest
                if previousDistance > self._batteryProx[house][batteryID]:
                    # update the battery that is currently closest
                    closestBatteryID = batteryID

                previousDistance = self._batteryProx[house][batteryID]

                # check if the capacity of the battery is able to hold the output of the house
                if house.output < self._capacities[self._batteries[batteryID]]:
                    closestDistance = self._batteryProx[house][batteryID]
                    batteryPicked = batteryID

        # a boolean to check if it is impossible to fit a house in it's closest battery
        notPossible = False

        # no battery was found that hasn't reached it's capacity yet
        if closestDistance == 9999:
            # keep going until a battery has been picked for each house
            while batteryPicked == None:
                # if the closest battery is not a possibility, try all other batteries in order
                if notPossible == True:
                    closestBatteryID += 1

                # check all houses that have already been assigned a battery
                for replaceHouse in houseBattery:
                    # find a house that has been assigned the battery we want this house to be assigned to
                    if self._batteries[closestBatteryID] == houseBattery[replaceHouse]:
                        # check if the capacity will be improved by replacing the house
                        if (self._capacities[self._batteries[closestBatteryID]] + replaceHouse.output - house.output) < self._capacities[self._batteries[closestBatteryID]] and (self._capacities[self._batteries[closestBatteryID]] + replaceHouse.output - house.output) > 0:
                            # replace the house
                            houseBattery[house] = self._batteries[closestBatteryID]
                            houseBattery.pop(replaceHouse)
                            if self._result != "invalid":
                                self._result.pop(replaceHouse)
                                batteryPicked = closestBatteryID
                                self._capacities[self._batteries[batteryPicked]
                                                 ] += replaceHouse.output
                                replaceHousePicked = replaceHouse
                            break

                if notPossible == False:
                    closestBatteryID = -1

                # the house could not be placed, start over
                notPossible = True

                if closestBatteryID == 4:
                    break
        else:
            # no house has been replaced
            replaceHousePicked = False

        if batteryPicked == None or self._result == "invalid":
            self._result = "invalid"
            return False
        else:
            # add the newly assigned house to the dicts, update the capacities
            houseBattery[house] = self._batteries[batteryPicked]
            self._capacities[self._batteries[batteryPicked]
                             ] -= house.output
            self._result[house] = houseBattery[house]

        # find a new battery for the house that is replaced
        if replaceHousePicked:
            self.initialDistribution(houseBattery, replaceHousePicked)

        return True

    # find the closest battery that hasn't reached it's capacity yet

    def findBattery(self):
        # print(houseList)
        # store all batteries that are matched with each house
        houseBattery = {}
        # loop through all houses that have not yet been assigned a battery
        for house in self._batteryProx:
            isValid = self.initialDistribution(houseBattery, house)
            if not isValid:
                break

    # make a list of all capacities of the batteries
    def fillCapacity(self):
        batteryCapacities = {}
        for battery in self._batteries:
            batteryCapacities[battery] = battery.capacity
        self._capacities = batteryCapacities

    def returnResults(self):
        return self._result

    def returnHillClimber(self):
        climber = astarHillClimber(
            self._result, self._batteries, self._houses, self._capacities, self._allDistances)
        return climber.mutateState()
