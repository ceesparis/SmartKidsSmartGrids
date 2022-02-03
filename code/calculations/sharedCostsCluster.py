def calculateCostShared(houses, batteries):
    """
    Calculates the cost of the cables and batteries when cables can be shared.
    """
    uniqueCables = []
    for house in houses:
        cables = house.cables
        for i in range(len(cables)-1):
            uniqueCable = (cables[i], cables[i+1])
            uniqueCables.append(uniqueCable)
    
    uniqueCables = set(uniqueCables)
    
    cableCosts = len(uniqueCables) * 9
    batteryCosts = len(batteries) * 5000
    total = cableCosts + batteryCosts
    
    return total
            