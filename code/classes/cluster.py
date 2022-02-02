import copy
from code.algorithms.createRoute import lay_Route

class Cluster():

    def __init__(self, houses):
        self.houses = houses
        self.output = 0
        self.total_cables = []

    def determine_output(self):
        '''
        Takes output of houses.
        Calculates total output cluster.
        '''

        output = 0
        for house in self.houses:
            output += house.output
        self.output = output


    def add_cluster_cables(self):
        '''
        Takes houses of cluster.
        Lays cables between houses in an efficient manner using:
        1. Greedy algorithm starting from each house.
        2. Making a full circle and destroying longest cable.
        '''

        # create list for all possible greedy paths
        possible_paths = []
        # create 'roadmap' for each possible greedy path
        for house in self.houses:
            possible_path = []
            starter = house
            # create copy of houses so once a house is connected it can be removed
            hoppin_houses = copy.deepcopy(self.houses)
            for hop_house in hoppin_houses:
                if hop_house.location == house.location:
                    starter = hop_house
            # while there are still houses unvisited, find closest houses to them and put in map
            while hoppin_houses:
                possible_path.append(starter)
                begin_x = starter.location[0]
                begin_y = starter.location[1]
                # find closest house in the cluster
                end_house = starter.find_closest(hoppin_houses)
                hoppin_houses.remove(starter)
                # use this closest house as new starting point
                starter = end_house
            # store roadmap in list
            possible_paths.append(possible_path)


        # lay cables according to greedy roadmaps
        for path in possible_paths:
            i = 0
            # add cables from first to last house
            while i < (len(path)-1):
                begin_house = path[i]
                end_house = path[i+1]
                lay_Route(begin_house, end_house)
                i += 1


            # complete circle, so that first house is directly connected to last house
            if len(path) > 1:
                begin_house = path[i]
                end_house = path[0]
                lay_Route(begin_house, end_house)
            # part 3 break circle by destroying largest cable
            biggest_cable = []
            for house in path:
                if len(house.cables) > len(biggest_cable):
                    biggest_cable = house.cables
            for house in path:
                if house.cables == biggest_cable:
                    house.cables = []

        # determine which of the possible paths is optimal, and put this path in self.houses
        min_cables = 1000
        smallest_path = []
        for path in possible_paths:
            # determine total cables path by adding cables of each house
            total_cables = 0
            for house in path:
                total_cables += len(house.cables)
            # if this route has the smallest total cables, it is the smallest path
            if total_cables < min_cables:
                min_cables = total_cables
                smallest_path = path
        # update houses of the clusters to contain the smallest path
        self.houses = smallest_path

    def connect_to_batt(self, batteries):
        '''
        Take cluster.
        Connect cluster to nearest possible battery.
        '''
        possible_batt = []
        # check which batteries are available
        for battery in batteries:
            if battery.capacity > self.output:
                possible_batt.append(battery)
        # keep track of closest house to desired battery and desired battery
        closest_point = 1000
        chosen_batt = None
        begin_point = None
        begin_house = None
        # determine closest point of cluster to a battery
        for house in self.houses:
            location = house.location
            x = location[0]
            y = location[1]
            for battery in possible_batt:
                bat_loc = battery.location
                bat_x = bat_loc[0]
                bat_y = bat_loc[1]
                x_diff = abs(x - bat_x)
                y_diff = abs(y - bat_y)
                total_diff = x_diff + y_diff
                # if house is the closest point to closest battery, update variables
                if total_diff < closest_point:
                    closest_point = total_diff
                    chosen_batt = battery
                    begin_point = location
                    begin_house = house
        # drain chosen battery
        chosen_batt.drain(self.output)
        # reverse cables of chosen house so that cables are continuously laid
        begin_house.cables.reverse()
        # finally, connect cables from cluster to battery
        lay_Route(begin_house, chosen_batt)

