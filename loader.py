def load_grid(district):

    batteries = []
    houses = []

    with open(f"{district}_batteries.csv") as f:
        while (True):
            line = f.readline()
            if line == '\n':
                break
            line = line.rstrip("\n")
            battery_info = line.split(',')
            batteries.append(battery_info)
            