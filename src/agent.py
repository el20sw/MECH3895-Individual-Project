"""
Agent module
============
Agent's operate in the network environment. The basic behaviour of the agent is to explore the network using the right hand wall rule
"""
import src.debug.logger as logger
from src.network import Network

class Agent:
    
    def __init__(self, env: Network, start_pos) -> None:
        self._log = logger.get_logger(__name__)
        self.env = env
        self.battery = 100
        self.current_node = start_pos
        self.previous_node = None
        self.link = None
        
        self.path = [self.current_node]
        
    def move(self):
        """
        Method for the agent to move in the environment
        """
        self.previous_node = self.current_node
        self.path.append(self.current_node)
        self.current_node = self.env.get_node(self.current_node, self.link)
        self._log.debug(f"Agent moved from {self.previous_node} to {self.current_node}")
        
    def RHW(self):
        """
        Method for the agent to follow the right hand wall rule - selects the next link to traverse
        """
        
        # Get the links for the current node
        links = self.env.water_network_model.get_links_for_node(self.current_node)
        self._log.debug(f"Links for node {self.current_node}: {links}")
        # Get the degree of the current node
        degree = len(links)
        self._log.debug(f"Degree of node {self.current_node}: {degree}")
        # Get the index of the link that the agent came from
        try:
            self.env.get_link(self.previous_node, self.current_node)
            arrival_port = links.index(self.link)
        except KeyError or ValueError:
            arrival_port = 0

        self._log.debug(f"Arrival port for node {self.current_node}: {arrival_port}")    
          
        # Select the next link to follow - traverse the edge with port number (arrival_port + 1) % degree
        self.link = links[(arrival_port + 1) % degree]
        self._log.debug(f"Next link to traverse: {self.link}")