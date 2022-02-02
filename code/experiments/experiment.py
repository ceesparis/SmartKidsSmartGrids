from code.classes.grid import Grid
import csv
from code.algorithms.cluster_alg import Clusalgo
from code.calculations.clus_cost_shared import calculateCostShared


def experiment(district):
    '''
    Takes district number.
    Creates grid and lays down smart grid using cluster_algorithm. 
    Stores total costs of smartgrid in csv file.
    '''

    # create grid object 
    grid = Grid(district)
    grid.load_from_csv()
    # create cluster_algorithm object
    cluster_grid = Clusalgo(grid)
    # put houses in clusters
    cluster_grid.cluster_houses()
    # connect clusters to batteries
    cluster_grid.connect_clusters()
    # update house information to calculate grid
    cluster_grid.update_houses()
    # calculate total costs
    total_shared = calculateCostShared(cluster_grid.houses, cluster_grid.batteries)
    cluster_grid.output = total_shared

    # write total_cost to csv file
    with open(f"cluster_results_district{district}range5.csv", "a") as f:
        csv_writer = csv.writer(f, delimiter="-")
        csv_writer.writerow([total_shared])
    
# specify here what district you want to experiment with
experiment(3)
