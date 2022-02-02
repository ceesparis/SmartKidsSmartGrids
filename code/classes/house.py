class House():

    def __init__(self, location, power):
        '''Initialises houses' locations, maximum power outputs, and cables attached to them.'''

        self.location = location
        self.output = power
        self.cables = []
        self.grouped = False

    def add_cable(self, x, y):
        ''' Adds cable from house to coordinate.'''
        new_cable = (x, y)
        cables = self.cables
        cables.append(new_cable)

    def house_sonar(self, houses):
        '''
        Takes houses and own location.
        Returns list of houses within specified range of own location.
        '''

        # take as reference point house location
        x1 = self.location[0]
        y1 = self.location[1]
        # determine range (amount of ticks that will be searched around reference point)
        search_range = 5
        local_house_list = []
        # check for ungrouped houses in vicinity of reference point
        for house in houses:
            x = house.location[0]
            y = house.location[1]
            diff_x = abs(x - x1)
            diff_y = abs(y - y1)
            # if house is within range and not part of a cluster add it to this cluster
            total_diff = diff_x + diff_y
            if (total_diff < search_range) & (house.grouped == False):
                local_house_list.append(house)
                house.grouped = True
        # return all houses in the vicinity
        return local_house_list

    def find_closest(self, houses):
        '''
            Takes houses and own location.
            Returns house that is (one of the) closest to its own location.
        '''

        # seperate own location into x and y
        x1 = self.location[0]
        y1 = self.location[1]
        closest = 1000
        closest_house = None
        # check for all houses if they are the closest thus far
        for house in houses:
            if house.location != self.location:
                # check relative distance of house by calculating x_difference and y_difference
                x = house.location[0]
                y = house.location[1]
                diff_x = abs(x - x1)
                diff_y = abs(y - y1)
                total_diff = diff_x + diff_y
                # if house is closest, update closest house
                if total_diff < closest:
                    closest = total_diff
                    closest_house = house
        # after checking all houses, return the closest one
        return(closest_house)
