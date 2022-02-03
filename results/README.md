## Experiments
In deze folder staan de drie verschillende experimenten die wij gerund hebben, allemaal gebaseerd op een runtijd van 30 minuten per district.
Er is een folder voor de uitkomsten van het Cluster algoritme, een voor de uitkomsten van het Smart Distribution algoritme, en een gebaseerd
op de staat van onze Baseline; deze uitkomsten zijn duidelijk niet beter dan de twee gevorderde algoritmes, maar was interessant om toe te
voegen om de vooruitgang van onze case te zien. Dit experiment valt op dezelfde manier te runnen als de Smart Distribution algoritme; alleen de code in code/helpers/distributionLoop moet volledig worden vervangen door het volgende:

```
import random
from code.algorithms.batteryDistribution import DistributeBatteries
from code.algorithms.randomCables import *
from code.calculations.costCalculation import *
from code.visualisation.visualisation import visualize
from code.algorithms.smartCables import GenerateSmartCables
from code.calculations.sharedCosts import *
from code.algorithms.smartCableClimber import CableClimber
from code.algorithms.connectionClimber import ClimbConnections

def iterateAstar(grid, loops):
    """
    Loop through the astar algorithm, printing out all costs and visualizing the improvements.
    """
    bestCosts = 100000
    bestResult = None
    
    for i in range(loops):
    """
    Find the best solution by looping through the first algorithm n amount of times.
    """
        
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
        f"Costs before hillclimber, with shared cables, without smart cables: {grid.district.ownCosts}")
    
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
    
    print(
        f"Costs after hillclimber, with shared cables, without smart cables: {grid.district.ownCosts}")
    
    return grid
```
