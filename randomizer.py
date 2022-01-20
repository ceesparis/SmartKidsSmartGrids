import random
import copy
from grid import Grid
from costCalculation import calculateCost
from visualization import visualize

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
        returns these randomly connected houses and batteries as a list.
        NB works but heavy on the deepcopy!
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

        # return a list with the connected houses and drained batteries
        ran_grid_info = [houses, batteries]
        return ran_grid_info


    def multiple_random(self):
        '''
        Calls random_cables function for as long as is needed to get
        x amount of valid random configurated grids.
        Returns list of valid random grids.
        '''
        # create a list to store grids
        suc_rand_grids = []
        # specify number of grids
        number_of_grids = 100
        # while this number is not yet reached, make random configurations and keep them if they are valid
        while len(suc_rand_grids) < number_of_grids:
            valid = True
            random_grid = self.random_cables()
            # if nothing is returned, the grid made was invalid
            if random_grid == None:
                valid = False
            # if the grid is valid, make Grid object with info of the randomly configured grid
            if valid == True:
                new_grid = Grid(self.district)
                houses = random_grid[0]
                batteries = random_grid[1]
                new_grid.houses = houses
                new_grid.batteries = batteries
                suc_rand_grids.append(new_grid)
        # return list of valid random grids
        return(suc_rand_grids)

    def calc_average(self, grid_list):
        '''
        Takes in list of valid grids.
        Prints average cost of this list of grids.
        '''
        total = 0
        # divide over the number of grids in the list
        grids_count = len(grid_list)
        # use calculate function to determine costs for each grid, then add these to total
        for grid in grid_list:
            batterySum = len(grid.batteries)
            houses = grid.houses
            cost = calculateCost(houses, batterySum)
            total += cost
        # divide total over quantity grids in the list
        average = total / grids_count
        print(average)