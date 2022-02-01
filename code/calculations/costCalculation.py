def calculateCost(houses, batterySum):
    '''Calculates the cost of the cables and batteries.'''

    completeCableSet = []
    cables = 0

    # loop through all houses
    for house in houses:
        cables += len(house.cables)

    # calculate the costs
    cableCosts = cables * 9
    batteryCosts = batterySum * 5000
    total = cableCosts + batteryCosts

    return total
