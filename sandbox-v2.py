import wntr
from src.network import Network

env = Network('networks/Net6.inp')
wn = env.water_network_model

wntr.graphics.plot_network(wn, node_size=2, link_width=1, title='Net6', filename='networks/Net6.png')

