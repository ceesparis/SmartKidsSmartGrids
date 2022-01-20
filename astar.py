from os import close, replace
from astarNodes import Node
import copy


class astar():
    def __init__(self, houses, batteries):
        self._houses = houses
        self._batteries = batteries
        self._batteryProx = {}
        self._result = None
        self._capacities = None
        self.fillCapacity()

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
            # print(self._batteryProx[house])

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

        # add fifty houses to the priority list
        for house in distancesSorted:
            priorityHouses.append(house)
            i += 1
            if i == 20:
                break

        # dictionary containing all houses with their closest batteries
        topHouses = {}

        # remove all houses that have been prioritized from the houses list and store them
        # in the topHouses dictionary
        for houseID in range(len(priorityHouses)):
            topHouses[priorityHouses[houseID]] = batteryDict.pop(
                priorityHouses[houseID])
            self._batteryProx.pop(priorityHouses[houseID])

        # add the first results to the class
        self._result = topHouses

        for house in priorityHouses:
            self._capacities[topHouses[house]] -= house.output

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
                            self._result.pop(replaceHouse)
                            batteryPicked = closestBatteryID
                            self._capacities[self._batteries[batteryPicked]
                                             ] += replaceHouse.output
                            replaceHousePicked = replaceHouse
                            break
                # the house could not be placed, start over
                notPossible = True
                closestBatteryID = -1
        else:
            # no house has been replaced
            replaceHousePicked = False

        # add the newly assigned house to the dicts, update the capacities
        houseBattery[house] = self._batteries[batteryPicked]
        self._capacities[self._batteries[batteryPicked]
                         ] -= house.output
        self._result[house] = houseBattery[house]

        if replaceHousePicked:
            self.initialDistribution(houseBattery, replaceHousePicked)

    # find the closest battery that hasn't reached it's capacity yet
    def findBattery(self):
        # store all batteries that are matched with each house
        houseBattery = {}

        # loop through all houses that have not yet been assigned a battery
        for house in self._batteryProx:
            self.initialDistribution(houseBattery, house)

    def fillCapacity(self):
        batteryCapacities = {}
        for battery in self._batteries:
            batteryCapacities[battery] = battery.capacity
        self._capacities = batteryCapacities
