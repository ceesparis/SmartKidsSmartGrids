from house_cluster import Cluster
import copy
from house import House

class Clusalgo():

    def __init__(self, grid):
        self.grid = grid
        self.district = grid.district
        self.houses = grid.houses
        self.batteries = grid.batteries
        self.house_clusters = []

    def cluster_houses(self):
        '''
        Takes in grid of houses.
        Returns clusters of interconnected houses based on relational proximity.
        '''
        # loop over houses
        for house in self.houses:
            # make every house into a potential root
            root_house = house
            # check which houses are in proximity of root_house
            root_cluster = root_house.house_sonar(self.houses)
            branch_clusters = []
            # if there are any houses in proximity, check which houses are in proximity of these houses
            for clus_house in root_cluster:
                if clus_house:
                    sub_cluster = clus_house.house_sonar(self.houses)
                # add all houses that are found to the branches of the root_house
                if sub_cluster:
                    for sub in sub_cluster:
                        branch_clusters.append(sub)

            # make list containing all house objects found
            for branch in branch_clusters:
                root_cluster.append(branch)
            # if any house objects are found, make a Cluster object from these houses
            if root_cluster:
                # root_cluster = sorted(root_cluster, key=lambda x: x.location[0]+x.location[1])
                new_cluster = Cluster(root_cluster)
                new_cluster.add_cluster_cables()
                # add every cluster to house_clusters
                self.house_clusters.append(new_cluster)
        # print(self.house_clusters)





    def connect_cluster(self):
        pass
        # for cluster in self.house_clusters:
        #     begin_house = cluster.houses[0]
        #     distanceList = []

        #     # loop through all batteries
        #     for battery in self.batteries:
        #         distance = 0

        #         # check the distances of houses to batteries by adding the difference on the x-axis to the
        #         # difference on the y-axis
        #         distance += abs(battery.location[0] - begin_house.location[0])
        #         distance += abs(battery.location[1] - begin_house.location[1])

        #         # add atribute to battery
        #         battery.clusdis = distance

        #         # add distance from house_cluster to battery
        #         distanceList.append(distance)

        #     # sort the batteries in ascending order with regards to distance from house_cluster
        #     BatDistances = sorted(self.batteries, key=lambda x: x.clusdis)
        #     # for battery in BatDistances:
        #     #     print(battery.clusdis)

        #     i = 0

        #     # hier nog error handling
        #     while BatDistances[i].capacity < cluster.output:
        #         i += 1
        #         if i == len(BatDistances):
        #         # exit(1)
        #             print('cluster failed')

        #     best_pos_bat = BatDistances[i]

        #     x_distance = best_pos_bat.location[0] - begin_house.location[0]
        #     y_distance = best_pos_bat.location[0] - begin_house.location[0]
        #     begin_x = begin_house.location[0]
        #     begin_y = begin_house.location[1]

        #     # is there already cable on house? think so
        #     while x_distance < 0:
        #         begin_house.add_cable(begin_x - 1, begin_y)
        #         x_distance += 1

        #     while x_distance > 0:
        #         begin_house.add_cable(begin_x + 1, begin_y)
        #         x_distance -= 1

        #     while y_distance < 0:
        #         begin_house.add_cable(begin_x, begin_y - 1)
        #         y_distance += 1

        #     while y_distance > 0:
        #         begin_house.add_cable(begin_x, begin_y + 1)
        #         y_distance -= 1

        # print('cluster succeeded')
        # need to drain batteries still







