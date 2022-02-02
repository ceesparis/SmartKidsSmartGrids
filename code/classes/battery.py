class Battery():
    """
    Initialises characteristics and functions for the grid's batteries.
    """

    def __init__(self, location, power):
        """
        Initialises batteries' locations, capacities, and the houses attached to them.
        """
        self.location = location
        self.capacity = power
        self.houses = []


    def drain(self, house_power):
        """
        When a house is connected to the battery, its output gets subtracted from
        the battery's capacity.
        """
        self.capacity = self.capacity - house_power
