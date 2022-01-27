import random
from code.algorithms.astar import astar
from code.algorithms.randomCables import *
from code.calculations.costCalculation import *
from code.visualisation.visualisation import visualize
from code.algorithms.smartCables import GenerateSmartCables
from code.calculations.sharedCosts import *


def iterateAstar(grid, loops):
    ''' Loop through the astar algorithm, printing out all costs and visualizing the improvements '''
    bestCosts = 100000
    bestResult = None

    # find the best solution by looping through the first algorithm n amount of times
    for i in range(loops):
        # random element #1
        random.shuffle(grid.houses)
        astarTest = astar(grid.houses, grid.batteries)
        results = astarTest.returnResults()
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
                bestState = astarTest
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
    visualize(grid, "initial")
    print(
        f"Costs before hillclimber, with shared cables, without smarter cables: {grid.district.ownCosts}")

    # lay the smarter cables down
    newCables = GenerateSmartCables(grid.batteries, grid.houses, bestResult)
    result = newCables.findCentralPoint()
    for house in result:
        house.cables = randomizeCables(
            house.location, [result[house][0], result[house][1]])
        house.cables = house.cables + (randomizeCables(
            [result[house][0], result[house][1]], bestResult[house].location))

    grid.district.ownCosts = calculateCostShared(
        len(grid.batteries), grid.batteries)
    print(
        f"Costs before hillclimber, with shared cables, smart cables: {grid.district.ownCosts}")
    visualize(grid, "sharedInitial")

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
    visualize(grid, "climber")

    # lay the cables down smarter
    newCables = GenerateSmartCables(grid.batteries, grid.houses, bestResult)
    result = newCables.findCentralPoint()
    for house in result:
        house.cables = randomizeCables(
            house.location, [result[house][0], result[house][1]])
        house.cables = house.cables + (randomizeCables(
            [result[house][0], result[house][1]], bestResult[house].location))

    grid.district.ownCosts = calculateCostShared(
        len(grid.batteries), grid.batteries)
    print(
        f"Costs after hillclimber, with shared cables, smart cables:{grid.district.ownCosts}")
    visualize(grid, "sharedClimber")

    return grid
