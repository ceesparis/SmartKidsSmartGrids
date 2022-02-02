def randomizeCables(houseLocation, batteryLocation):
    """
    Generates a cable route that follows simple straight lines from houses to batteries.
    """
    coordHouse = houseLocation
    coordBattery1 = batteryLocation

    # initial position of the cable
    coordCable = list(coordHouse)

    # complete route of the cable
    cableRoute = [list(coordHouse)]

    # move opposite of the position the house is compared to the battery (e.g. left: move right)
    while int(coordBattery1[0]) > coordCable[0]:
        coordCable[0] += 1
        cableRoute.append(coordCable[:])

    while int(coordBattery1[0]) < coordCable[0]:
        coordCable[0] -= 1
        cableRoute.append(coordCable[:])

    while int(coordBattery1[1]) > coordCable[1]:
        coordCable[1] += 1
        cableRoute.append(coordCable[:])

    while int(coordBattery1[1]) < coordCable[1]:
        coordCable[1] -= 1
        cableRoute.append(coordCable[:])

    return cableRoute
