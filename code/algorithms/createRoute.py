def lay_Route(house, end):

    begin_house = house
    begin_x = begin_house.location[0]
    begin_y = begin_house.location[1]
    end_x = end.location[0]
    end_y = end.location[1]

    begin_house.add_cable(begin_x, begin_y)
    while begin_x < end_x:
        begin_x += 1
        begin_house.add_cable(begin_x, begin_y)
    while begin_x > end_x:
        begin_x -= 1
        begin_house.add_cable(begin_x, begin_y)
    while begin_y < end_y:
        begin_y += 1
        begin_house.add_cable(begin_x, begin_y)
    while begin_y > end_y:
        begin_y -= 1
        begin_house.add_cable(begin_x, begin_y)