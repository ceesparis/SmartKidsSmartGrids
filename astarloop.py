import random
from astar import astar
from randomCables import *
from costCalculation import *
from visualization import visualize
from smartCables import GenerateSmartCables
from sharedCosts import *


def iterateAstar(grid, loops):
    bestCosts = 100000
    bestResult = None
    for i in range(loops):
        random.shuffle(grid.houses)
        astarTest = astar(grid.houses, grid.batteries)
        results = astarTest.returnResults()
        if results != "invalid":
            for house in results:
                house.cables = randomizeCables(
                    house.location, results[house].location)
                results[house].houses.append(house)

            grid.district.ownCosts = calculateCostShared(
                len(grid.batteries), grid.batteries)

            if grid.district.ownCosts < bestCosts:
                bestCosts = grid.district.ownCosts
                bestResult = results
                bestState = astarTest
            results[house].houses = []

    for battery in grid.batteries:
        battery.houses = []

    if bestResult == None:
        print("No valid solution generated")
        exit(1)

    for house in bestResult:
        house.cables = randomizeCables(
            house.location, bestResult[house].location)
        bestResult[house].houses.append(house)
    grid.district.ownCosts = bestCosts
    # print(bestCosts)
    visualize(grid, "initial")

    newCables = GenerateSmartCables(grid.batteries, grid.houses, bestResult)
    result = newCables.findCentralPoint()
    for house in result:
        house.cables = randomizeCables(
            house.location, [result[house][0], result[house][1]])
        house.cables = house.cables + (randomizeCables(
            [result[house][0], result[house][1]], bestResult[house].location))

    grid.district.ownCosts = calculateCostShared(
        len(grid.batteries), grid.batteries)
    print(grid.district.ownCosts)
    visualize(grid, "sharedInitial")

    bestResult = bestState.returnHillClimber()
    for battery in grid.batteries:
        battery.houses = []

    for house in bestResult:
        house.cables = randomizeCables(
            house.location, bestResult[house].location)
        bestResult[house].houses.append(house)
    grid.district.ownCosts = calculateCostShared(
        len(grid.batteries), grid.batteries)
    # print(grid.district.ownCosts)
    visualize(grid, "climber")

    newCables = GenerateSmartCables(grid.batteries, grid.houses, bestResult)
    result = newCables.findCentralPoint()
    for house in result:
        house.cables = randomizeCables(
            house.location, [result[house][0], result[house][1]])
        house.cables = house.cables + (randomizeCables(
            [result[house][0], result[house][1]], bestResult[house].location))

    grid.district.ownCosts = calculateCostShared(
        len(grid.batteries), grid.batteries)
    print(grid.district.ownCosts)
    visualize(grid, "sharedClimber")

    return grid
