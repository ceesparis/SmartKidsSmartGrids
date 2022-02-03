import csv
from .battery import Battery
from .house import House
from .district import District


def loadGrid(districtNumber):
    """
        Takes district-number.
        Creates and returns grid with data from corresponding district.
    """

    # make a list to store batteries and housess from csv in
    batteries = []
    houses = []

    # open the batteries-csv from the district you want to represent
    with open(f"./data/district_{districtNumber}/district-{districtNumber}_batteries.csv", "r") as f:
        csvReader = csv.reader(f)
        
        # skip the first row with the row-names
        next(csvReader)
        
        # make battery objects from the remaining rows
        for line in csvReader:
            location = tuple(map(int, line[0].split(',')))
            power = float(line[1])
            newBattery = Battery(location, power)
            batteries.append(newBattery)

    # open the housess-csv from the district you want to represent
    with open(f"./data/district_{districtNumber}/district-{districtNumber}_houses.csv", "r") as f:
        csvReader = csv.reader(f)
        
        # skips the first row with the row-names
        next(csvReader)
        
        # makes house objects from the remaining rows
        for line in csvReader:
            location = (int(line[0]), int(line[1]))
            power = float(line[2])
            newHouse = House(location, power)
            houses.append(newHouse)

    district = District(districtNumber, 0)

    # return a list containing all made objects
    grid = [district, batteries, houses]
    return grid
