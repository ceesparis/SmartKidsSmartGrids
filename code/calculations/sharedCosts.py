def calculateCostShared(batterySum, batteries):
    '''Calculates the cost of the cables and batteries.'''

    cables = 0
    cablesBattery = {}

    for battery in batteries:
        completeCableSet = []
        # loop through all houses
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

    for battery in batteries:
        completeCablesSplit = set()
        for cableID in range(len(cablesBattery[battery])-1):
            cablesTemp = cablesBattery[battery][cableID].split(".")
            completeCablesSplit.add(cablesTemp[0])
            completeCablesSplit.add(cablesTemp[1])

        cables += len(completeCablesSplit)

    # calculate the costs
    cableCosts = cables * 9
    batteryCosts = batterySum * 5000
    total = cableCosts + batteryCosts

    return total
