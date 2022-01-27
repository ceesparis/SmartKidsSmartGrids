import random
import copy
from code.calculations.costCalculation import calculateCost


class Randomizer():

    def __init__(self, grid):
        # create an emptry grid to use as template for the random grids
        self.grid = grid
        self.district = grid.district
        self.houses = grid.houses
        self.batteries = grid.batteries

    def random_cables(self):
        '''
        Copies lists of houses and batteries.
        Randomnly connects houses to batteries and
        if resulting grid is valid, returns the cost of 
        this configuration. Else returns None. 
        '''

        houses = copy.deepcopy(self.houses)
        batteries = copy.deepcopy(self.batteries)
        # lay cables from each house in grid
        for house in houses:
            house_output = house.output
            # pick a random battery to connect the house to
            battery = random.choice(batteries)
            # make a copy of the batteries that you can remove batteries from
            less_batteries = batteries.copy()
            # while capacity battery is insufficient, remove it from choices
            while battery.capacity < house_output:
                less_batteries.remove(battery)
                # if all batteries are insufficient for house, stop making the grid
                if len(less_batteries) == 0:
                    return
                # else pick other random battery
                battery = random.choice(less_batteries)
            # determine end and starting point of the cableline
            start = house.location
            end = battery.location
            x_start = start[0]
            y_start = start[1]
            x_end = end[0]
            y_end = end[1]

            # add cables from start to end (inclusive)
            house.add_cable(x_start, y_start)
            while x_start < x_end:
                x_start += 1
                house.add_cable(x_start, y_start)
            while x_start > x_end:
                x_start -= 1
                house.add_cable(x_start, y_start)
            while y_start < y_end:
                y_start += 1
                house.add_cable(x_start, y_start)
            while y_start > y_end:
                y_start -= 1
                house.add_cable(x_start, y_start)
            house.add_cable(x_start, y_start)
            battery.drain(house.output)

        # calculate cost of valid grid and return it
        cost = calculateCost(houses, len(batteries))
        return cost

    def multiple_random(self):
        '''
        Calls random_cables function for as long as is needed to get
        x amount of valid random configurated grids.
        Returns list wth total cost and number of grids.
        '''
        # add up grid costs in total
        total = 0
        # keep track of how many grids we currently have in current_grids
        current_grids = 0
        # specify number of grids
        number_of_grids = 10000
        # while this number is not yet reached, make random configurations and keep them if they are valid
        while current_grids < number_of_grids:
            valid = True
            random_grid = self.random_cables()
            # if nothing is returned, the grid made was invalid
            if random_grid == None:
                valid = False
            # if the grid is valid, add its costs to total and add to number of current grids
            if valid == True:
                total += random_grid
                current_grids += 1
        # return both the number of valid grids as well as their total cost
        grids_info = [total, number_of_grids]
        return grids_info

    def calc_average(self, grids_info):
        '''
        Takes in list of total cost and number of grids.
        Prints average cost of these grids.
        '''
        total = grids_info[0]
        grids_count = grids_info[1]
        average = total / grids_count
        print(int(average))
