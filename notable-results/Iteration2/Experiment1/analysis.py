# Script to analyse the results of the experiment
# Path: notable-results/Iteration2/Experiment1/analysis.py

from matplotlib import pyplot as plt
import pandas as pd
# import scipy.ndimage

try:
    no_swarm_results = pd.read_csv("notable-results/Iteration2/Experiment1/simulation_20230302_154615/results.csv")
except FileNotFoundError:
    print("Results not found.")
    exit(1)
    
try:
    swarm_results = pd.read_csv("notable-results/Iteration2/Experiment1/simulation_20230302_154710/results.csv")
except FileNotFoundError:
    print("Results not found.")
    exit(1)
    
# Plot the results as pct_explored vs turn

# create figure
fig, ax = plt.subplots()

# plot no_swarm_results as smooth curve
# ax.plot(no_swarm_results["turn"], scipy.ndimage.gaussian_filter1d(no_swarm_results["pct_explored"], 5), label="No Swarm")
ax.plot(no_swarm_results["turn"], no_swarm_results["pct_explored"], label="No Swarm")

# plot swarm_results
# ax.plot(swarm_results["turn"], scipy.ndimage.gaussian_filter1d(swarm_results["pct_explored"], 5), label="Swarm")
ax.plot(swarm_results["turn"], swarm_results["pct_explored"], label="Swarm")

# set labels
ax.set_xlabel("Turn")
ax.set_ylabel("Pct Explored")

# set title
ax.set_title("Pct Explored vs Turn")

# set legend
ax.legend()

# save figure
fig.savefig("notable-results/Iteration2/Experiment1/analysis.png")
