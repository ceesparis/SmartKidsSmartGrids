class Battery():

    def __init__(self, location, power):
        '''Initialises batteries' locations, capacities, and the houses attached to them.'''
        
        self.location = location
        self.capacity = power
        self.houses = []
