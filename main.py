from sys import argv
from code.classes.randomizer import Randomizer
from code.classes.grid import Grid
from astarloop import iterateAstar
from code.visualisation.old_visualisation import visualize
from code.visualisation.visualize_clus_exp import visualize_exp
from code.algorithms.cluster_alg import Clusalgo
from code.calculations.clus_cost_shared import calculateCostShared
from code.experiments.experiment import experiment

if __name__ == "__main__":
    # check for correct usage
    if len(argv) != 2:
        print('Usage: Python3 main.py [district number]')
        exit(1)
    district = argv[1]
    # check if district number is valid
    try:
        grid = Grid(district)
        grid.load_from_csv()
    except Exception:
        print('district not found')
        exit(2)
    
    # experiment(1)
    visualize_exp("./data/experiments/cluster/cluster_results_district1.csv", district)
    # ask user what algorithm they want to employ for laying the smartgrid
    print(f"\nchoose your algorithm for district {district}: clusterWebz or smartDistribution\n")
    algo_choice = input("Make your choice here(CW or SD): ")
    algo_choice = algo_choice.upper()
    trying = True

    #
    while trying:
        if algo_choice in "SD":
            loops = 10
            grid = iterateAstar(grid, loops)
            grid.printOutput()
            trying = False
        elif algo_choice in "CW":
            cluster_grid = Clusalgo(grid)
            cluster_grid.cluster_houses()
            cluster_grid.connect_clusters()
            cluster_grid.update_houses()
            total_shared = calculateCostShared(cluster_grid.houses, cluster_grid.batteries)
            print(total_shared)
            visualize(cluster_grid)
            trying = False
        elif algo_choice in "QUIT":
            break
        else:
            print("be more clear please\n")
            print("choose your algorithm: clusterWebz(CW), smartDistribution(SD), or Q to quit\n")
            algo_choice = input("Make your choice here(CW or SD): ")

