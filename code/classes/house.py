class House():
    """
    Characteristics and functions of houses on the grid.
    """

    def __init__(self, location, power):
        """
        Initialises houses' locations, maximum power outputs, and cables attached to them.
        """
        self.location = location
        self.output = power
        self.cables = []
        self.grouped = False


    def addCable(self, x, y):
        """
        Adds cable from house to coordinate.
        """
        newCable = (x, y)
        cables = self.cables
        cables.append(newCable)


    def houseSonar(self, houses):
        """
        Takes houses and own location.
        Returns list of houses within specified range of own location.
        """

        # take as reference point house location
        x1 = self.location[0]
        y1 = self.location[1]

        # determine range (amount of ticks that will be searched around reference point)
        searchRange = 5
        localHouseList = []

        # check for ungrouped houses in vicinity of reference point
        for house in houses:
            x = house.location[0]
            y = house.location[1]
            differenceX = abs(x - x1)
            differenceY = abs(y - y1)

            # if house is within range and not part of a cluster add it to this cluster
            totalDifference = differenceX + differenceY

            if (totalDifference < searchRange) & (house.grouped == False):
                localHouseList.append(house)
                house.grouped = True

        # return all houses in the vicinity
        return localHouseList


    def findClosest(self, houses):
        """
            Takes houses and own location.
            Returns house that is (one of the) closest to its own location.
        """

        # seperate own location into x and y
        x1 = self.location[0]
        y1 = self.location[1]

        closest = 1000
        closestHouse = None

        # check for all houses if they are the closest thus far
        for house in houses:
            if house.location != self.location:
                
                # check relative distance of house by calculating x_difference and y_difference
                x = house.location[0]
                y = house.location[1]
                
                differenceX = abs(x - x1)
                differenceY = abs(y - y1)
                totalDifference = differenceX + differenceY
                
                # if house is closest, update closest house
                if totalDifference < closest:
                    closest = totalDifference
                    closestHouse = house
        
        # after checking all houses, return the closest one
        return(closestHouse)
