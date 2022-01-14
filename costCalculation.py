# calculate the cost of the batteries and the cables
def calculateCost(houses, batterySum):
    completeCableSet = []
    cables = 0
    # loop through all houses
    for house in houses:
        cables += len(house.cables)

    # calculate the costs
    print(cables)
    cableCosts = cables * 9
    batteryCosts = batterySum * 5000

    return cableCosts + batteryCosts
