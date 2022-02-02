def calculateCostShared(houses, batteries):
    """
    Calculates the cost of the cables and batteries when cables can be shared.
    """
    unique_cables = []
    for house in houses:
        cables = house.cables
        for i in range(len(cables)-1):
            unique_cable = (cables[i], cables[i+1])
            unique_cables.append(unique_cable)
    
    unique_cables = set(unique_cables)
    
    costs_cables = len(unique_cables) * 9
    costs_batteries = len(batteries) * 5000
    total = costs_cables + costs_batteries
    
    return total
            