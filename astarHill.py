import random
import copy

from matplotlib.pyplot import close


class astarHillClimber():

    def __init__(self, initialResult, batteries, houses, currentCapacities, distances):
        self._bestResult = initialResult
        self._allBatteries = batteries
        self._allHouses = houses
        self._capacities = currentCapacities
        self._distancesToBatteries = distances
        self._batteryDict = None
        self.batteryvHouses()
        self.getPerfectDistances()

    def distanceDifference(self, house, newBattery):
        currentBatteryID = self._allBatteries.index(self._bestResult[house])
        currentDistance = self._distancesToBatteries[house][currentBatteryID]

        newBatteryID = self._allBatteries.index(newBattery)
        newDistance = self._distancesToBatteries[house][newBatteryID]

        return currentDistance - newDistance

    def updateNewState(self, randomHouseOne, randomHouseTwo, batteryHouseOne, batteryHouseTwo):
        self._bestResult[randomHouseOne] = batteryHouseTwo
        self._bestResult[randomHouseTwo] = batteryHouseOne
        self._capacities[batteryHouseOne] = self._capacities[batteryHouseOne] + \
            randomHouseOne.output - randomHouseTwo.output
        self._capacities[batteryHouseTwo] = self._capacities[batteryHouseTwo] + \
            randomHouseTwo.output - randomHouseOne.output

    def mutateState(self):
        for i in range(10000):
            randomHouseOne = self._allHouses[random.randint(0, 149)]
            randomHouseTwo = self._allHouses[random.randint(0, 149)]

            batteryHouseOne = self._bestResult[randomHouseOne]
            batteryHouseTwo = self._bestResult[randomHouseTwo]
            if self._capacities[batteryHouseOne] + randomHouseOne.output - randomHouseTwo.output > 0:
                if self._capacities[batteryHouseTwo] + randomHouseTwo.output - randomHouseOne.output > 0:
                    distanceImprovementOne = self.distanceDifference(
                        randomHouseOne, batteryHouseTwo)
                    distanceImprovementTwo = self.distanceDifference(
                        randomHouseTwo, batteryHouseOne)
                    if distanceImprovementOne + distanceImprovementTwo > 0:
                        self.updateNewState(
                            randomHouseOne, randomHouseTwo, batteryHouseOne, batteryHouseTwo)
        return self._bestResult

    def batteryvHouses(self):
        batteryDict = {self._allBatteries[0]: [], self._allBatteries[1]: [
        ], self._allBatteries[2]: [], self._allBatteries[3]: [], self._allBatteries[4]: []}
        for house in self._bestResult:
            batteryDict[self._bestResult[house]].append(house)
        self._batteryDict = batteryDict

    def checkCapacity(self, houseOne, houseTwo, batteryTwo, batteryOne):
        if self._capacities[batteryTwo] - houseTwo.output + houseOne.output > 0:
            if self._capacities[batteryOne] - houseOne.output + houseTwo.output > 0:
                return True
        return False

    def getPerfectDistances(self):
        for i in range(10):
            # Loop door alle huizen
            for houseOne in self._bestResult:
                batteryOne = self._bestResult[houseOne]
                # Pak zijn meest dichtsbijzijnde batterij
                sortedDistances = copy.deepcopy(
                    self._distancesToBatteries[houseOne])
                sortedDistances.sort()
                closestDistance = sortedDistances[0]
                closestDistanceIndex = self._distancesToBatteries[houseOne].index(
                    closestDistance)
                closestBatteryOne = self._allBatteries[closestDistanceIndex]

                # zit hij hier niet in?
                if closestBatteryOne != batteryOne:
                    # 	pak een huis met deze batterij
                    for houseTwo in self._batteryDict[closestBatteryOne]:
                        # 	pak zijn dichtstbijzijnde batterij
                        sortedDistances = copy.deepcopy(
                            self._distancesToBatteries[houseTwo])
                        sortedDistances.sort()
                        closestDistance = sortedDistances[1]
                        closestDistanceIndex = self._distancesToBatteries[houseTwo].index(
                            closestDistance)
                        closestBatteryTwo = self._allBatteries[closestDistanceIndex]

                        bestImprovement = -1
                        improvement = -1

                        # is dit dezelfde als waar huis 1 in zit?
                        if closestBatteryTwo == batteryOne:
                            if houseOne != houseTwo:
                                improvement = self.distanceDifference(
                                    houseOne, self._bestResult[houseTwo]) + self.distanceDifference(houseTwo, self._bestResult[houseOne])
                            if improvement > 0:
                                if self.checkCapacity(houseOne, houseTwo, closestBatteryTwo, closestBatteryOne):
                                    if improvement > bestImprovement:
                                        bestImprovement = improvement
                                        secondHouse = houseTwo
                                        break
                    if bestImprovement > 0:
                        self.updateNewState(
                            houseOne, secondHouse, self._bestResult[houseOne], self._bestResult[secondHouse])

        return self._bestResult
