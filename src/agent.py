"""
Agent module
============
Agent's operate in the network environment. The basic behaviour of the agent is to explore the network using the right hand wall rule
"""
import src.debug.logger as logger
from src.network import Network
from src.observation import Observation

class Agent:
    
    def __init__(self, env: Network, agent_id, start_pos) -> None:
        self._log = logger.get_logger(__name__)
        self.env = env
        self.G = env.water_network_model.to_graph().to_directed()
        
        self._agent_id = agent_id
        self._battery = 100
        self._current_node = start_pos
        self._previous_node = None
        self.link = None
        self._path = [self._current_node]
        
        self._agents_in_range = []
    
    @property
    def agent_id(self):
        return self._agent_id
        
    @property
    def battery(self):
        return self._battery
        
    @property
    def position(self):
        return self._current_node
    
    @property
    def previous_node(self):
        return self._previous_node
    
    @property
    def path(self):
        return self._path
    
    @property
    def agents_in_range(self):
        return self._agents_in_range
    
    def __str__(self) -> str:
        return f"Agent {self._agent_id} at {self._current_node}"
    
    def __repr__(self) -> str:
        return f"Agent {self._agent_id} at {self._current_node}"
        
    def move(self):
        """
        Method for the agent to move in the environment
        """
        self._previous_node = self._current_node
        self._path.append(self._current_node)
        self._current_node = self.env.get_node(self._current_node, self.link)
        self._log.debug(f"Agent moved from {self._previous_node} to {self._current_node}")
        
    def communicate(self):
        """
        Method for the agent to communicate with other agents
        """
        
        # get the agents in the same node
        agents_in_range = self._agents_in_range
        # check if agents are in the same node
        if not agents_in_range:
            # No agents in range
            self._log.debug(f"{self} No agents in range")
        else:
            # Agents in range
            self._log.debug(f"{self} Agents in range: {agents_in_range}")
            # 
        
        
    def ping(self, agents):
        """
        Method for the agent to broadcast a ping to other agents in the same node
        - param: list of agents in the environment/simulation
        - update: the agents_in_range attribute
        """
        
        self._agents_in_range = []
        # broadcast a ping to all agents in the same node and get the response if in range
        for agent in agents:
            # send ping
            if agent != self and agent.position == self._current_node:
                # get response
                self._agents_in_range.append(agent)
                
        self._log.debug(f"{self} Pinged: {self._agents_in_range}")
        
        
    def RH_Traversal(self):
        """
        Method for the agent to follow the right hand wall rule - selects the next link to traverse
        """
        
        # Get the links for the current node
        links = self.env.water_network_model.get_links_for_node(self._current_node)
        self._log.debug(f"Links for node {self._current_node}: {links}")
        # Get the degree of the current node
        degree = len(links)
        self._log.debug(f"Degree of node {self._current_node}: {degree}")
        # Get the index of the link that the agent came from
        try:
            self.env.get_link(self._previous_node, self._current_node)
            arrival_port = links.index(self.link)
        except KeyError or ValueError:
            arrival_port = 0

        self._log.debug(f"Arrival port for node {self._current_node}: {arrival_port}")    
          
        # Select the next link to follow - traverse the edge with port number (arrival_port + 1) % degree
        link = links[(arrival_port + 1) % degree]
        self.link = link
        self._log.debug(f"Next link to traverse: {link}")
        
        return link