import copy
from code.helpers.createRoute import layRoute

class Cluster():
    """
    Defines a cluster of houses close to each other, making it somewhat logical
    for these houses to share cables towards a battery.
    """

    def __init__(self, houses):
        self.houses = houses
        self.output = 0
        self.totalCables = []


    def determineOutput(self):
        """
        Takes output of houses.
        Calculates total output cluster.
        """

        output = 0
        for house in self.houses:
            output += house.output
        self.output = output


    def addClusterCables(self):
        """
        Takes houses of cluster.
        Lays cables between houses in an efficient manner using:
        1. Greedy algorithm starting from each house.
        2. Making a full circle and destroying longest cable.
        """

        # create list for all possible greedy paths
        possiblePaths = []

        # create 'roadmap' for each possible greedy path
        for house in self.houses:
            possiblePath = []
            starter = house

            # create copy of houses so once a house is connected it can be removed
            hoppingHouses = copy.deepcopy(self.houses)
            for hoppingHouse in hoppingHouses:
                if hoppingHouse.location == house.location:
                    starter = hoppingHouse
            
            # while there are still houses unvisited, find closest houses to them and put in map
            while hoppingHouses:
                possiblePath.append(starter)
                
                # find closest house in the cluster
                endHouse = starter.findClosest(hoppingHouses)
                hoppingHouses.remove(starter)
                
                # use this closest house as new starting point
                starter = endHouse
            
            # store roadmap in list
            possiblePaths.append(possiblePath)

        # lay cables according to greedy roadmaps
        for path in possiblePaths:
            i = 0
            
            # add cables from first to last house
            while i < (len(path)-1):
                beginHouse = path[i]
                endHouse = path[i+1]
                layRoute(beginHouse, endHouse)
                i += 1

            # complete circle, so that first house is directly connected to last house
            if len(path) > 1:
                beginHouse = path[i]
                endHouse = path[0]
                layRoute(beginHouse, endHouse)
            
            # part 3 break circle by destroying largest cable
            biggestCable = []
            for house in path:
                if len(house.cables) > len(biggestCable):
                    biggestCable = house.cables
            for house in path:
                if house.cables == biggestCable:
                    house.cables = []

        # determine which of the possible paths is optimal, and put this path in self.houses
        minimumCables = 1000
        smallestPath = []
        
        for path in possiblePaths:
            
            # determine total cables path by adding cables of each house
            totalCables = 0
            
            for house in path:
                totalCables += len(house.cables)
            
            # if this route has the smallest total cables, it is the smallest path
            if totalCables < minimumCables:
                minimumCables = totalCables
                smallestPath = path
        
        # update houses of the clusters to contain the smallest path
        self.houses = smallestPath


    def connect_to_batt(self, batteries):
        """
        Take cluster.
        Connect cluster to nearest possible battery.
        """
        possibleBatteries = []
        
        # check which batteries are available
        for battery in batteries:
            if battery.capacity > self.output:
                possibleBatteries.append(battery)
        
        # keep track of closest house to desired battery and desired battery
        closestPoint = 1000
        chosenBattery = None
        beginPoint = None
        beginHouse = None
        
        # determine closest point of cluster to a battery
        for house in self.houses:
            location = house.location
            x = location[0]
            y = location[1]
            
            for battery in possibleBatteries:
                batteryLocation = battery.location
                
                batteryX = batteryLocation[0]
                batteryY = batteryLocation[1]
                
                xDifference = abs(x - batteryX)
                yDifference = abs(y - batteryY)
                totalDifference = xDifference + yDifference
                
                # if house is the closest point to closest battery, update variables
                if totalDifference < closestPoint:
                    closestPoint = totalDifference
                    chosenBattery = battery
                    beginPoint = location
                    beginHouse = house
        
        # drain chosen battery
        chosenBattery.drain(self.output)
        
        # reverse cables of chosen house so that cables are continuously laid
        beginHouse.cables.reverse()
        
        # finally, connect cables from cluster to battery
        layRoute(beginHouse, chosenBattery)

