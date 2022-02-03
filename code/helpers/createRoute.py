def layRoute(house, end):
    """
    Will lay cables between the house and configured battery coords
    for as long as the end point has not been reached.
    """

    beginHouse = house

    beginX = beginHouse.location[0]
    beginY = beginHouse.location[1]

    endX = end.location[0]
    endY = end.location[1]

    beginHouse.addCable(beginX, beginY)

    # house is somewhere on the left of the end point
    while beginX < endX:
        beginX += 1
        beginHouse.addCable(beginX, beginY)
    
    # house is somewhere on the right of the end point
    while beginX > endX:
        beginX -= 1
        beginHouse.addCable(beginX, beginY)

    # house is somewhere below the end point
    while beginY < endY:
        beginY += 1
        beginHouse.addCable(beginX, beginY)

    # house is somewhere above the end point
    while beginY > endY:
        beginY -= 1
        beginHouse.addCable(beginX, beginY)