from code.classes.grid import Grid
import csv
from code.algorithms.clusterAlgorithm import Clusalgo
from code.calculations.sharedCostsCluster import calculateCostShared


def experiment(district):
    """
    Takes district number.
    Creates grid and lays down smart grid using cluster_algorithm. 
    Stores total costs of smartgrid in csv file.
    """

    # create grid object 
    grid = Grid(district)
    grid.loadFromCsv()
    
    # create cluster_algorithm object
    clusterGrid = Clusalgo(grid)
    
    # put houses in clusters
    clusterGrid.clusterHouses()
    
    # connect clusters to batteries
    clusterGrid.connectClusters()
    
    # update house information to calculate grid
    clusterGrid.updateHouses()
    
    # calculate total costs
    totalShared = calculateCostShared(clusterGrid.houses, clusterGrid.batteries)
    clusterGrid.output = totalShared

    # write total_cost to csv file
    with open(f"cluster_results_district{district}range5.csv", "a") as f:
        csvWriter = csv.writer(f, delimiter="-")
        csvWriter.writerow([totalShared])
    
# specify here what district you want to experiment with
experiment(3)
