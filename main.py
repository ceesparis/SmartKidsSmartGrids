from code.calculations.clus_cost_shared import calculateCostShared
from code.algorithms.cluster_alg import Clusalgo
from code.visualisation.visualize_clus_exp import visualize_exp
from code.visualisation.visualisation import visualize
from code.helpers.distributeLoop import iterateDistribution
from sys import argv
from code.classes.randomizer import Randomizer
from code.classes.grid import Grid

if __name__ == "__main__":
    
    # check for correct usage
    if len(argv) < 3:
        print('Usage: Python3 main.py [district number] [ALGORITHM(CW or SD)]')
        exit(1)
    
    district = argv[1]
    
    # check if district number is valid
    try:
        grid = Grid(district)
        grid.load_from_csv()
    
    except Exception:
        print('district not found')
        exit(2)

  # check if input is only letters, if so, capitalize input
    algorithm = argv[2]
    

    trying = True

    while trying:
        if algorithm.isalpha():
            algorithm = algorithm.upper()
        # if smartdistribution is asked for, run this alogrithm
        if algorithm in "SD":
            loops = 10
            grid = iterateDistribution(grid, loops)
            grid.printOutput()
            trying = False
        
        # if clusterwebz is asked for, run this algorithm
        elif algorithm in "CW":
            cluster_grid = Clusalgo(grid)
            cluster_grid.cluster_houses()
            cluster_grid.connect_clusters()
            cluster_grid.update_houses()
            
            total_shared = calculateCostShared(
                cluster_grid.houses, cluster_grid.batteries)
            
            print(f"\n Total costs: {total_shared}\n")
            visualize(cluster_grid)
            trying= False

        elif algorithm in "QUIT":
            break
        
        # if input not valid, ask the user again
        else:
            print("be more clear please\n")
            print("choose your algorithm: clusterWebz(CW), smartDistribution(SD) or type Q to quit\n")
            algorithm = input("make your choice: ")

        