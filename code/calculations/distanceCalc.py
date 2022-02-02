from cmath import sqrt
import math


def calc_distance():
    """
    Calculates the distance between two points on the grid.
    """
    
    # ex: x = location[0], y = location[1]
    x = 2
    y = 50
    
    battery = (3, 45)
    diff_x = (x - battery[0])
    diff_y = (y - battery[1])
    
    if diff_x < 0:
        diff_x = diff_x * -1
        
    if diff_y < 0:
        diff_y = diff_y * -1
        
    distance = diff_x+diff_y
    print(distance)

