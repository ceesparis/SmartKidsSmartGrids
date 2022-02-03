import random
import copy
from code.calculations.costCalculation import calculateCost


class Randomizer():
    """
    Randomises combinations of houses and batteries and the cables
    laid between those, until correct configurations come out.
    """

    def __init__(self, grid):
        """
        Creates an empty grid to use as a template for the random grids
        """
        self.grid = grid
        self.district = grid.district
        self.houses = grid.houses
        self.batteries = grid.batteries


    def randomCables(self):
        """
        Copies lists of houses and batteries.
        Randomnly connects houses to batteries and
        if resulting grid is valid, returns the cost of 
        this configuration. Else returns None. 
        """
        houses = copy.deepcopy(self.houses)
        batteries = copy.deepcopy(self.batteries)
        
        # lay cables from each house in grid
        for house in houses:
            houseOutput = house.output
            
            # pick a random battery to connect the house to
            battery = random.choice(batteries)
            
            # make a copy of the batteries that you can remove batteries from
            lessBatteries = batteries.copy()
            
            # while capacity battery is insufficient, remove it from choices
            while battery.capacity < houseOutput:
                lessBatteries.remove(battery)
                
                # if all batteries are insufficient for house, stop making the grid
                if len(lessBatteries) == 0:
                    return
                
                # else pick other random battery
                battery = random.choice(lessBatteries)
            
            # determine end and starting point of the cableline
            start = house.location
            end = battery.location

            xStart = start[0]
            yStart = start[1]

            xEnd = end[0]
            yEnd = end[1]

            # add cables from start to end (inclusive)
            house.addCable(xStart, yStart)
            
            while xStart < xEnd:
                xStart += 1
                house.addCable(xStart, yStart)
            
            while xStart > xEnd:
                xStart -= 1
                house.addCable(xStart, yStart)
            
            while yStart < yEnd:
                yStart += 1
                house.addCable(xStart, yStart)
            
            while yStart > yEnd:
                yStart -= 1
                house.addCable(xStart, yStart)
            
            house.addCable(xStart, yStart)
            battery.drain(house.output)

        # calculate cost of valid grid and return it
        cost = calculateCost(houses, len(batteries))
        return cost


    def multipleRandom(self):
        """
        Calls random_cables function for as long as is needed to get
        x amount of valid random configurated grids.
        Returns list wth total cost and number of grids.
        """

        # add up grid costs in total
        total = 0
        
        # keep track of how many grids we currently have in currentGrids
        currentGrids = 0
        
        # specify number of grids
        numberOfGrids = 10000
        
        # while this number is not yet reached, make random configurations and keep them if they are valid
        while currentGrids < numberOfGrids:
            valid = True
            randomGrid = self.random_cables()
            
            # if nothing is returned, the grid made was invalid
            if randomGrid == None:
                valid = False
            
            # if the grid is valid, add its costs to total and add to number of current grids
            if valid == True:
                total += randomGrid
                currentGrids += 1
        
        # return both the number of valid grids as well as their total cost
        gridsInfo = [total, numberOfGrids]
        return gridsInfo


    def calcAverage(self, gridsInfo):
        """
        Takes in list of total cost and number of grids.
        Prints average cost of these grids.
        """
        total = gridsInfo[0]
        gridCount = gridsInfo[1]
        average = total / gridCount
        
        print(int(average))
