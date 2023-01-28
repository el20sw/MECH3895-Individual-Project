# Convert to dictionary
wn_dict = wntr.network.to_dict(wn)
print(wn_dict.keys())
# Remove 'version'and 'patterns' keys
wn_dict.pop('patterns')
wn_dict.pop('version')
# Get adjacency list from dictionary of nodes
adj_list = wn_dict['']

# Check if file exists
if os.path.exists('adj_list.txt'):
    # Delete file
    os.remove('adj_list.txt')
# Create file to write to
f = open('adj_list.txt', 'w')
# Write adjacency list to file
f.write(str(adj_list))


# Convert to graph
lengths = wn.query_link_attribute('length')
wG = wn.to_graph(wn, link_weight=lengths)
uG = nx.to_undirected(wG)

# Plot the network
# ax = wntr.graphics.plot_network(wn, title='Net3')
# plt.figure(1)
# plt.show()