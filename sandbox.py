# import network
from src.network import Network

# Initialise network using networks/Net1.inp
net1 = Network('networks/Net1.inp')

# access the nodes and links
node_names = net1.node_names
link_names = net1.link_names

# access the frozen nodes and links
frozen_nodes = net1.frozen_nodes.frozen_node_keys
frozen_links = net1.frozen_links.frozen_link_keys