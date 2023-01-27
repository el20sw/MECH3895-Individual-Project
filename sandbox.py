### Import modules
import wntr
import matplotlib.pyplot as plt
import networkx as nx

# Create pipe network
path_to_file = 'networks/Net1.inp'
wn = wntr.network.WaterNetworkModel(path_to_file)

lengths = wn.query_link_attribute('length')
names = wn.query_link_attribute('name')

print(names)
print(lengths)

# Get the network as a dictionary
wn_dict = wntr.network.to_dict(wn)
# Write wn to json file using wntr function
wntr.network.write_json(wn, 'Net1.json')

# Get links
wn_links = wn_dict['links']
# Get nodes
wn_nodes = wn_dict['nodes']
# Get junctions
wn_junctions = [node for node in wn_nodes if node['node_type'] == 'Junction']

# Create adjacency list
adj_list = {}

# Iterate through links and add start_node to adjacency list and end_node to adjacency list
for link in wn_links:
    # Check if link is a pipe
    if link['link_type'] != 'Pipe':
        # If link is not a pipe, skip it
        continue
    # Get start and end nodes
    start_node = link['start_node_name']
    end_node = link['end_node_name']
    # Get link name
    link_name = link['name']
    # Add start and end nodes to adjacency list
    if start_node not in adj_list:
        adj_list[start_node] = {}
    if end_node not in adj_list:
        adj_list[end_node] = {}
    # Add link to adjacency list
    adj_list[start_node][end_node] = {
        'link_name': link_name,
        'link_length': link['length']
        }
    adj_list[end_node][start_node] = {
        'link_name': link_name,
        'link_length': link['length']
    }

# Create as undirected NetworkX graph
G = wntr.network.to_graph(wn)
uG = G.to_undirected()

# Get the connected nodes given the current node
def get_neighbours(current_node):
    return list(adj_list[current_node].keys())

# Get neighbours of a node using NetworkX
def get_neighbours_nx(current_node):
    return list(uG.neighbors(current_node))

# Write adjacency list to file
with open('adj_list.txt', 'w') as f:
    # New line for each node
    foo = str(adj_list).replace('}},', '}},\n')
    f.write(foo)
    f.close()

# Render the network
wntr.graphics.plot_network(wn, title=path_to_file, node_labels=True, link_labels=True)
plt.show()
