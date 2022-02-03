import copy
from code.classes.cluster import Cluster
import random

class Clusalgo():
    """
    Initialises the cluster algorithm, grouping certain houses together before distributing
    over the batteries, making it easier to share cables, and therefore most likely cheaper.
    """

    def __init__(self, grid):
        self.grid = grid
        self.district = grid.district
        self.houses = grid.houses
        self.batteries = grid.batteries
        self.houseClusters = []


    def clusterHouses(self):
        """
        Takes in grid of houses.
        Returns clusters of interconnected houses based on relational proximity.
        If no other houses are in proximity, the cluster will consist of only one house.
        """
        
        # check for each house if it is clusterable
        for house in self.houses:
            
            # make every house into a potential root
            rootHouse = house
            
            # check which houses are in proximity of rootHouse
            rootCluster = rootHouse.houseSonar(self.houses)
            branchClusters = []
            
            # check which houses are in proximity of these houses three layers down
            for clusHouse in rootCluster:
                if clusHouse:
                    subCluster = clusHouse.houseSonar(self.houses)
                
                if subCluster:
                    for sub in subCluster:
                        branchClusters.append(sub)
                        subSubCluster = sub.houseSonar(self.houses)
                        if subSubCluster:
                            for subSub in subSubCluster:
                                branchClusters.append(subSub)

            # add all branches that are found to the rootCluster
            for branch in branchClusters:
                rootCluster.append(branch)
            
            # if any house objects are found, make a Cluster object from these houses
            if len(rootCluster) > 0:
                newCluster = Cluster(rootCluster)
                
                # calculate shared output for houses in grid
                newCluster.determineOutput()
                
                # link the houses to each other
                newCluster.addClusterCables()
                
                # add cluster object to self
                self.houseClusters.append(newCluster)


    def updateHouses(self):
        """
        Takes information from cluster object.
        Changes house information accordingly for grid representation.
        """
        clusHouses = []
        for cluster in self.houseClusters:
            for clusterHouse in cluster.houses:
                clusHouses.append(clusterHouse)
        self.houses = clusHouses


    def connectClusters(self):
        """
        Takes clusters and batteries.
        Creates valid grid where all clusters are connected to a battery.
        """

        # make a deepcopy so 'empty grid' is preserved
        clustersCopy = copy.deepcopy(self.houseClusters)
        batteriesCopy = copy.deepcopy(self.batteries)
        count = 0
        
        # try to make a grid until one is found where all clusters are connected
        while count != len(self.houseClusters):
            count = 0
            
            for cluster in clustersCopy:
                try:
                    cluster.connectToBattery(batteriesCopy)
                    count += 1
                except Exception as e:
                    clustersCopy = copy.deepcopy(self.houseClusters)
                    batteriesCopy = copy.deepcopy(self.batteries)
                    random.shuffle(clustersCopy)
                    break
          
        # finally, change current grid into valid connected grid      
        self.houseClusters = clustersCopy
        self.batteries = batteriesCopy