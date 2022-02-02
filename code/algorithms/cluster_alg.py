import copy
from code.classes.house import House
from code.classes.cluster import Cluster
import random

class Clusalgo():
    """
    Add a small description for the class!
    """

    def __init__(self, grid):
        self.grid = grid
        self.district = grid.district
        self.houses = grid.houses
        self.batteries = grid.batteries
        self.house_clusters = []


    def cluster_houses(self):
        """
        Takes in grid of houses.
        Returns clusters of interconnected houses based on relational proximity.
        If no other houses are in proximity, the cluster will consist of only one house.
        """
        
        # check for each house if it is clusterable
        for house in self.houses:
            
            # make every house into a potential root
            root_house = house
            
            # check which houses are in proximity of root_house
            root_cluster = root_house.house_sonar(self.houses)
            branch_clusters = []
            
            # check which houses are in proximity of these houses three layers down
            for clus_house in root_cluster:
                if clus_house:
                    sub_cluster = clus_house.house_sonar(self.houses)
                
                if sub_cluster:
                    for sub in sub_cluster:
                        branch_clusters.append(sub)
                        sub_sub_cluster = sub.house_sonar(self.houses)
                        if sub_sub_cluster:
                            for sub_sub in sub_sub_cluster:
                                branch_clusters.append(sub_sub)

            # add all branches that are found to the root_cluster
            for branch in branch_clusters:
                root_cluster.append(branch)
            
            # if any house objects are found, make a Cluster object from these houses
            if len(root_cluster) > 0:
                new_cluster = Cluster(root_cluster)
                
                # calculate shared output for houses in grid
                new_cluster.determine_output()
                
                # link the houses to each other
                new_cluster.add_cluster_cables()
                
                # add cluster object to self
                self.house_clusters.append(new_cluster)


    def update_houses(self):
        """
        Takes information from cluster object.
        Changes house information accordingly for grid representation.
        """
        clus_houses = []
        for cluster in self.house_clusters:
            for cluster_house in cluster.houses:
                clus_houses.append(cluster_house)
        self.houses = clus_houses


    def connect_clusters(self):
        """
        Takes clusters and batteries.
        Creates valid grid where all clusters are connected to a battery.
        """

        # make a deepcopy so 'empty grid' is preserved
        clusters_copy = copy.deepcopy(self.house_clusters)
        batteries_copy = copy.deepcopy(self.batteries)
        count = 0
        
        # try to make a grid until one is found where all clusters are connected
        while count != len(self.house_clusters):
            count = 0
            
            for cluster in clusters_copy:
                try:
                    cluster.connect_to_batt(batteries_copy)
                    count += 1
                except Exception as e:
                    clusters_copy = copy.deepcopy(self.house_clusters)
                    batteries_copy = copy.deepcopy(self.batteries)
                    random.shuffle(clusters_copy)
                    break
          
        # finally, change current grid into valid connected grid      
        self.house_clusters = clusters_copy
        self.batteries = batteries_copy
 