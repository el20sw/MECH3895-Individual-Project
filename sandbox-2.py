import wntr
import networkx as nx
import matplotlib.pyplot as plt

from collections import defaultdict

from src.network import Network

class Graph:
    def __init__(self) -> None:
        self.graph = defaultdict(list)
        
    def addEdge(self, u, v):
        self.graph[u].append(v)
        
    def DFSUtil(self, v, visited):
        visited.add(v)
        print(v, end=' ')
        
        for neighbour in self.graph[v]:
            if neighbour not in visited:
                self.DFSUtil(neighbour, visited)
                
    def DFS(self, v):
        visited = set()
        self.DFSUtil(v, visited)
        
if __name__ == '__main__':
    # network = Network('networks/Net1.inp')
    # wn = wntr.network.WaterNetworkModel('networks/Net1.inp')
    # # network.plot_network(show=True, node_labels=True, link_labels=True)
    # # graph = network.adj_list
    # mG = wntr.network.to_graph(wn)
    # uG = mG.to_undirected()
    # pos = nx.spring_layout(uG, seed=20)
    # nx.draw(uG, pos=pos, with_labels=True)
    
    # g = Graph()
    # g.addEdge(10, 11)
    # g.addEdge(10, 9)
    # g.addEdge(11, 12)
    # g.addEdge(11, 21)
    # g.addEdge(12, 13)
    # g.addEdge(12, 22)
    # g.addEdge(12, 2)
    # g.addEdge(13, 22)
    # g.addEdge(21, 22)
    # g.addEdge(21, 31)
    # g.addEdge(22, 23)
    # g.addEdge(22, 32)
    # g.addEdge(31, 32)
      
    # print("Following is DFS from (starting from vertex 21)")
    # g.DFS(21)
    
    # plt.show()
    
    vh = 1
    vb = 0.5*vh
    
    print("score b =", vb)
    
    vg = 1
    ve = 0.5*vg
    vk = 0
    vj = 0.5*vk
    vi = -10 + 0.5*ve + 0.5*vj
    vd = 0.5*vi
    vf = 1 + 0.5*vd
    vc = 0.5*vf
    
    print("score c =", vc)
    
    vk = 0
    vj = 0.5*vk
    vg = 1
    ve = 0.5*vg
    vi = -10 + 0.5*ve + 0.5*vj
    vc = 0
    vf = 1 + 0.5*vc
    vd = 0.5*vf + 0.5*vi
    
    print("score d =", vd)
    
    vg = 1
    vk = 0
    vj = 0.5*vk
    vc = 0
    vf = 1 + 0.5*vc
    vd = 0.5*vf
    vi = -10 + 0.5*vj + 0.5*vd
    ve = 0.5*vg + 0.5*vi
    
    print("score e = ", ve)
    
    