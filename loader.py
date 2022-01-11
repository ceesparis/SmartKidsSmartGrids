import re 
import csv 
from battery import Battery
from house import House

def load_grid(dis_number):

    batteries = []
    houses = []

    with open(f'./Huizen&Batterijen/district_{dis_number}/district-{dis_number}_batteries.csv', 'r') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)
        for line in csv_reader:
            location = line[0].strip('')
            power = line[1]
            new_battery = Battery(location, power)
            batteries.append(new_battery)
    
    with open(f'./Huizen&Batterijen/district_{dis_number}/district-{dis_number}_houses.csv', 'r') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)
        for line in csv_reader:
            location = (int(line[0]), int(line[1]))
            power = line[2]
            new_house = House(location, power)
            houses.append(new_house)

    grid = [batteries, houses]
    print(grid)
    return grid