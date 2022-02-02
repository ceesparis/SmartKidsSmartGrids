## some quick instructions for how to run an experiment with the cluster algorithm!

## step 1: import clus_exp from this folder into main
You can import clus_exp.py as follows: 
from code.experiments.clus_exp import clus_experiment

## step 2: put code in main
You can call clus_exp() before anything else in your code.

## step 3: run main
If you run main now, it will first run clus_exp for half an hour. Results will be stored in a csv.file called cluster_results_district{district}range5.csv, where the district in brackets is the district you ran the experiment on. To change the district, go to experiment.py and change the number with which experiment is called. 

## step 4: visualize results
To visualize results import the following in main:
from visualize_clus_exp import visualize_exp
You can run visualize_clus_exp right after clus_exp. It takes as arguments the csv you just created and the district number. 