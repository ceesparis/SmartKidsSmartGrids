# calculate the cost of the batteries and the cables
def calculateCost(houses, batterySum):
    completeCableSet = []
    counter = 0
    # loop through all houses
    for house in houses:
        for i in range(len(house.cables) - 1):
            # join every other coördinate of a cable together to draw a line
            listToStr = ' '.join(
                map(str, house.cables[i] + house.cables[i + 1]))
            i += 1
            # add the cable line to a set, because cables that run over shouldn't be counted twice
            completeCableSet.append(listToStr)
            counter += 1
    # completeCableSet.remove('')

    # calculate the costs
    print(counter)
    cableCosts = len(completeCableSet) * 9
    batteryCosts = batterySum * 5000

    return cableCosts + batteryCosts
