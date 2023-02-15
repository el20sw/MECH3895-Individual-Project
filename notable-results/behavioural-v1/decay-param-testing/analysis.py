"""
Script for analysing the results of the decay parameter testing experiment.
"""

from matplotlib import pyplot as plt
import pandas as pd

# get the results file
results_file = 'notable-results/behavioural-v1/decay-param-testing/results.csv'
# read the results file
df = pd.read_csv(results_file)
# plot the results - pct_explored vs turn for each decay paramete
# create a figure
fig, ax = plt.subplots()
# plot the results
for decay in df.columns[1:]:
    ax.plot(df['turn'], df[decay], label=decay)
    
# set the x and y labels
ax.set_xlabel('Turn')
ax.set_ylabel('Pct Explored')
# set the title
ax.set_title('Pct Explored vs Turn for Different Decay Parameters')
# set the legend
ax.legend()
# show the plot
plt.show()
