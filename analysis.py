from matplotlib import pyplot as plt
import pandas as pd

try:
    no_swarm_results = pd.read_csv("notable-results/Iteration3/Experiment1/simulation_20230302_154615/results.csv")
except FileNotFoundError:
    print("Results not found.")
    exit(1)
    
try:
    swarm_results = pd.read_csv("notable-results/Iteration3/Experiment1/simulation_20230302_154710/results.csv")
except FileNotFoundError:
    print("Results not found.")
    exit(1)
    
try:
    mean_informed_swarm_results = pd.read_csv("notable-results/Iteration3/Experiment1/simulation_20230304_144339/results.csv")
except FileNotFoundError:
    print("Results not found.")
    exit(1)
    
try:
    # median_informed_swarm_results = pd.read_csv("results/simulation_20230304_144905/results.csv")
    median_informed_swarm_results = pd.read_csv("notable-results/Iteration3/Experiment1/simulation_20230304_145155/results.csv")
except FileNotFoundError:
    print("Results not found.")
    exit(1)
    
# create figure
fig, ax = plt.subplots()

# plot no_swarm_results as smooth curve
# ax.plot(no_swarm_results["turn"], scipy.ndimage.gaussian_filter1d(no_swarm_results["pct_explored"], 5), label="No Swarm")
ax.plot(no_swarm_results["turn"], no_swarm_results["pct_explored"], label="No Swarm")

# plot swarm_results
# ax.plot(swarm_results["turn"], scipy.ndimage.gaussian_filter1d(swarm_results["pct_explored"], 5), label="Swarm")
ax.plot(swarm_results["turn"], swarm_results["pct_explored"], label="Swarm")

# plot mean_informed_swarm_results
ax.plot(mean_informed_swarm_results["turn"], mean_informed_swarm_results["pct_explored"], label="Mean Informed Swarm")

# plot median_informed_swarm_results
ax.plot(median_informed_swarm_results["turn"], median_informed_swarm_results["pct_explored"], label="Median Informed Swarm") 

# set labels
ax.set_xlabel("Turn")
ax.set_ylabel("Pct Explored")

# set title
ax.set_title("Pct Explored vs Turn")

# set legend
ax.legend()

# show figure
plt.show()