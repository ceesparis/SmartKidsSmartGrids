import random
import copy

from matplotlib.pyplot import close


class distributionHillClimber():
    """
    Loop through the current best solution, first placing the houses in the closest battery to them, if
    it's an improvement, then randomly comparing the houses to find better distances.
    """

    def __init__(self, initialResult, batteries, houses, currentCapacities, distances, seed):
        self._bestResult = initialResult
        self._allBatteries = batteries
        self._allHouses = houses
        self._capacities = currentCapacities
        self._distancesToBatteries = distances
        self._batteryDict = None
        self._seed = seed
        self.batteryvHouses()
        self.getPerfectDistances()


    def distanceDifference(self, house, newBattery):
        """
        Check the difference between the distance to the
        current battery of a house and the potential new battery.
        """
        currentBatteryID = self._allBatteries.index(self._bestResult[house])
        currentDistance = self._distancesToBatteries[house][currentBatteryID]

        newBatteryID = self._allBatteries.index(newBattery)
        newDistance = self._distancesToBatteries[house][newBatteryID]

        return currentDistance - newDistance


    def updateNewState(self, randomHouseOne, randomHouseTwo, batteryHouseOne, batteryHouseTwo):
        """
        After finding a better solution, update the capacities and state with the swap of houses.
        """
        # update state
        self._bestResult[randomHouseOne] = batteryHouseTwo
        self._bestResult[randomHouseTwo] = batteryHouseOne

        # update capacities
        self._capacities[batteryHouseOne] = self._capacities[batteryHouseOne] + \
            randomHouseOne.output - randomHouseTwo.output
        self._capacities[batteryHouseTwo] = self._capacities[batteryHouseTwo] + \
            randomHouseTwo.output - randomHouseOne.output


    def mutateState(self):
        """
        Loop n amount of times to the current state, comparing two random houses to eachother to 
        see if the total distance to batteries will improve. If so, make the swap.
        """
        for i in range(250000):
            
            # pick random house
            random.seed(self._seed)
            randomHouseOne = self._allHouses[random.randint(0, 149)]
            randomHouseTwo = self._allHouses[random.randint(0, 149)]

            # get the batteries that belong to these houses
            batteryHouseOne = self._bestResult[randomHouseOne]
            batteryHouseTwo = self._bestResult[randomHouseTwo]

            # check if the capacities allow the swap
            if self._capacities[batteryHouseOne] + randomHouseOne.output - randomHouseTwo.output > 0:
                if self._capacities[batteryHouseTwo] + randomHouseTwo.output - randomHouseOne.output > 0:

                    # check if the distance will improve
                    distanceImprovementOne = self.distanceDifference(
                        randomHouseOne, batteryHouseTwo)
                    distanceImprovementTwo = self.distanceDifference(
                        randomHouseTwo, batteryHouseOne)

                    # update the state
                    if distanceImprovementOne + distanceImprovementTwo > 0:
                        self.updateNewState(
                            randomHouseOne, randomHouseTwo, batteryHouseOne, batteryHouseTwo)

        return self._bestResult


    def batteryvHouses(self):
        """
        Make list of all houses connected to a battery for each battery, store it in a dictionary.
        """
        batteryDict = {self._allBatteries[0]: [], self._allBatteries[1]: [
        ], self._allBatteries[2]: [], self._allBatteries[3]: [], self._allBatteries[4]: []}
        for house in self._bestResult:
            batteryDict[self._bestResult[house]].append(house)
        self._batteryDict = batteryDict


    def checkCapacity(self, houseOne, houseTwo, batteryTwo, batteryOne):
        """
        Check if the capacity of two batteries allow a swap.
        """
        if self._capacities[batteryTwo] - houseTwo.output + houseOne.output > 0:
            if self._capacities[batteryOne] - houseOne.output + houseTwo.output > 0:
                return True
        return False


    def getPerfectDistances(self):
        """
        Loop through the current state to see if each can be placed in it's closest battery, 
        if it improves the distance.
        """
        for i in range(250):
            
            # loop through all houses
            for houseOne in self._bestResult:
                batteryOne = self._bestResult[houseOne]
                
                # get it's closest battery
                sortedDistances = copy.deepcopy(
                    self._distancesToBatteries[houseOne])
                sortedDistances.sort()
                closestDistance = sortedDistances[0]
                closestDistanceIndex = self._distancesToBatteries[houseOne].index(
                    closestDistance)
                closestBatteryOne = self._allBatteries[closestDistanceIndex]

                # check if the house is not yet in the battery
                if closestBatteryOne != batteryOne:
                    
                    # get a house in the closest battery
                    for houseTwo in self._batteryDict[closestBatteryOne]:
                        
                        # get the current battery of the house that will be swapped
                        sortedDistances = copy.deepcopy(
                            self._distancesToBatteries[houseTwo])
                        sortedDistances.sort()
                        
                        closestDistance = sortedDistances[1]
                        closestDistanceIndex = self._distancesToBatteries[houseTwo].index(
                            closestDistance)
                        closestBatteryTwo = self._allBatteries[closestDistanceIndex]

                        bestImprovement = -1
                        improvement = -1

                        # check if the second closest battery to this house is the current battery of house one
                        if closestBatteryTwo == batteryOne:
                            if houseOne != houseTwo:
                                improvement = self.distanceDifference(
                                    houseOne, self._bestResult[houseTwo]) + self.distanceDifference(houseTwo, self._bestResult[houseOne])
                            
                            # check if the distance will be improved
                            if improvement > 0:
                                
                                # check if the capacities allow it
                                if self.checkCapacity(houseOne, houseTwo, closestBatteryTwo, closestBatteryOne):
                                    if improvement > bestImprovement:
                                        bestImprovement = improvement
                                        secondHouse = houseTwo
                                        break
                    
                    # make the swap
                    if bestImprovement > 0:
                        self.updateNewState(
                            houseOne, secondHouse, self._bestResult[houseOne], self._bestResult[secondHouse])

        return self._bestResult
