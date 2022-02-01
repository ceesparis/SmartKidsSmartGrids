def calculateCostShared(batterySum, batteries):
    '''
    calculates the cost of the cables and batteries
    '''

    cables = 0
    cablesBattery = {}

    # make sets of two coordinates for each house, adding them together and storing them
    # with the current battery in the dictionary
    for battery in batteries:
        completeCableSet = []
        for house in battery.houses:
            for cableID in range(0, len(house.cables) - 1):
                cableLine = str(house.cables[cableID]) + \
                    "." + str(house.cables[cableID + 1])
                cableLineOpposite = str(house.cables[cableID + 1]) + \
                    "." + str(house.cables[cableID])
                if cableLineOpposite not in completeCableSet:
                    completeCableSet.append(cableLineOpposite)
                if cableLine not in completeCableSet:
                    completeCableSet.append(cableLine)

        cablesBattery[battery] = completeCableSet

    # make a set of all cablesets for each battery
    for battery in batteries:
        completeCablesSplit = set()
        # split all sets of cables up again to get just one coordinate per cable
        for cableID in range(len(cablesBattery[battery])-1):
            cablesTemp = cablesBattery[battery][cableID].split(".")
            completeCablesSplit.add(cablesTemp[0])
            completeCablesSplit.add(cablesTemp[1])

        # add these coordinates to the total cable length
        cables += len(completeCablesSplit)

    # calculate the costs
    cableCosts = cables * 9
    batteryCosts = batterySum * 5000
    total = cableCosts + batteryCosts

    return total
