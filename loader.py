import re 
import csv 
from battery import Battery
from house import House

def load_grid(dis_number):

    # make a list to store batteries and housess from csv in 
    batteries = []
    houses = []

    # open the batteries-csv from the district you want to represent
    with open(f'./Huizen&Batterijen/district_{dis_number}/district-{dis_number}_batteries.csv', 'r') as f:
        csv_reader = csv.reader(f)
        # skip the first row with the row-names
        next(csv_reader)
        # make battery objects from the remaining rows
        for line in csv_reader:
            location = line[0].strip('')
            power = line[1]
            new_battery = Battery(location, power)
            batteries.append(new_battery)
    
    # open the housess-csv from the district you want to represent
    with open(f'./Huizen&Batterijen/district_{dis_number}/district-{dis_number}_houses.csv', 'r') as f:
        csv_reader = csv.reader(f)
        # skipt the first row with the row-names
        next(csv_reader)
        # make house objects from the remaining rows
        for line in csv_reader:
            location = (int(line[0]), int(line[1]))
            power = line[2]
            new_house = House(location, power)
            houses.append(new_house)

    # return a list containing all made objects 
    grid = [batteries, houses]
    return grid