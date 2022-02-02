import random
from code.algorithms.batteryDistribution import DistributeBatteries
from code.algorithms.randomCables import *
from code.calculations.costCalculation import *
from code.visualisation.visualisation import visualize
from code.algorithms.smartCables import GenerateSmartCables
from code.calculations.sharedCosts import *
from code.algorithms.connectionClimber import ClimbConnections
import sys


def iterateDistribution(grid, loops):
    """
    Loop through the distribution algorithm, printing out all costs and visualizing the improvements.
    """
    bestCosts = 100000
    bestResult = None

    seed = random.randint(0, 10000)

    # find the best solution by looping through the first algorithm n amount of times
    for i in range(loops):

        # random element #1
        random.seed(seed)
        random.shuffle(grid.houses)

        batteryDistribution = DistributeBatteries(
            grid.houses, grid.batteries, seed)

        results = batteryDistribution.returnResults()

        if results != "invalid":

            # lay all cables down
            for house in results:
                house.cables = randomizeCables(
                    house.location, results[house].location)
                results[house].houses.append(house)

            grid.district.ownCosts = calculateCostShared(
                len(grid.batteries), grid.batteries)

            # keep track of best solution so far
            if grid.district.ownCosts < bestCosts:
                bestCosts = grid.district.ownCosts
                bestResult = results
                bestState = batteryDistribution
            results[house].houses = []

    # reset the grid
    for battery in grid.batteries:
        battery.houses = []

    if bestResult == None:
        print("No valid solution generated")
        exit(1)

    # update the grid with current best solution
    for house in bestResult:
        house.cables = randomizeCables(
            house.location, bestResult[house].location)
        bestResult[house].houses.append(house)
    grid.district.ownCosts = bestCosts

    # lay the smarter cables down
    newCables = GenerateSmartCables(
        grid.batteries, grid.houses, bestResult, seed)
    result = newCables.findCentralPoint()

    for house in result:
        house.cables = randomizeCables(
            house.location, [result[house][0], result[house][1]])
        house.cables = house.cables + (randomizeCables(
            [result[house][0], result[house][1]], bestResult[house].location))

    grid.district.ownCosts = calculateCostShared(
        len(grid.batteries), grid.batteries)

    # use hillclimber to improve the current best solution
    bestResult = bestState.returnHillClimber()

    # reset the grid
    for battery in grid.batteries:
        battery.houses = []

    # update the grid with current best solution
    for house in bestResult:
        house.cables = randomizeCables(
            house.location, bestResult[house].location)
        bestResult[house].houses.append(house)
    grid.district.ownCosts = calculateCostShared(
        len(grid.batteries), grid.batteries)

    # lay the cables down smarter
    newCables = GenerateSmartCables(
        grid.batteries, grid.houses, bestResult, seed)
    result = newCables.findCentralPoint()

    for house in result:
        house.cables = randomizeCables(
            house.location, [result[house][0], result[house][1]])
        house.cables = house.cables + (randomizeCables(
            [result[house][0], result[house][1]], bestResult[house].location))

    centralPoints = newCables.returnCentralPoints()

    connectionClimber = ClimbConnections(
        grid.batteries, grid.houses, result, centralPoints, bestResult)
    connectionClimber.findConnections()

    grid.district.ownCosts = calculateCostShared(
        len(grid.batteries), grid.batteries)

    visualize(grid)

    print(f"{grid.district.ownCosts} {seed}")
    return grid
