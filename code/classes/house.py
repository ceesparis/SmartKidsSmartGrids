class House():

    def __init__(self, location, power):
        '''Initialises houses' locations, maximum power outputs, and cables attached to them.'''
        
        self.location = location
        self.output = power
        self.cables = []

    def add_cable(self, x, y):
        new_cable = (x, y)
        cables = self.cables
        cables.append(new_cable)