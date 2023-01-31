# Import logger
import src.debug.logger as logger

from typing import List

from src.network import Network
from src.agent import Agent

### Overwatch Class ###
class Overwatch:
    """
    Overwatch Class
    ----------
    Class to create an overwatch agent to monitor the environment and in certain cases facilitate actions.
    The class will deal with the following:
        - Monitoring the simulation
        - Facilitating actions in the simulation such as communication between agents
        
    """

    def __init__(self, environment: Network, agents: List[Agent]):
        # Initialise the logger
        self._log = logger.get_logger(__name__)
        # Initialise the overwatch
        self._environment = environment
        self._agents = agents
        self._num_agents = len(agents)
        self._agent_positions = {}
        self._visited_nodes = []
        self._all_nodes = self._environment.node_names
        self._turns = 0
        self._pct_explored = 0

    ### Attributes ###
    @property
    def environment(self) -> Network:
        return self._environment

    @property
    def agents(self) -> List[Agent]:
        return self._agents

    @agents.setter
    def agents(self, agents: List[Agent]):
        self._agents = agents

    @property
    def num_agents(self) -> int:
        return self._num_agents

    @property
    def agent_positions(self) -> dict:
        return self._agent_positions

    @property
    def visited_nodes(self) -> list:
        return self._visited_nodes

    @property
    def all_nodes(self) -> list:
        return self._all_nodes

    @property
    def turns(self) -> int:
        return self._turns

    @property
    def pct_explored(self) -> float:
        return self._pct_explored

    ### Methods ###
    def update(self):
        """
        Method to update the overwatch
        :return: None
        """
        # Update the number of turns
        self._turns += 1
        self._log.info(f"Turn {self._turns}")
        # Update the percentage of nodes explored
        self._pct_explored = self.update_pct_explored()
        self._log.info(f"Percentage of nodes explored: {self._pct_explored}")
        # Update the agent positions
        self._agent_positions = self.update_agent_positions()
        self._log.info(f"Agent positions: {self._agent_positions}")
        # Update the visited nodes
        self._visited_nodes = self.update_visited_nodes()
        self._log.info(f"Visited nodes: {self._visited_nodes}")

    def update_agent_positions(self):
        """
        Method to get the positions of the agents
        :return: Dictionary of agent positions
        """
        # Get the positions of the agents
        for agent in self._agents:
            self._agent_positions[agent.id] = agent.position
        # Return the dictionary
        return self._agent_positions

    def update_visited_nodes(self):
        """
        Method to get the unique visited nodes of the agents
        :return: Dictionary of unique visited nodes
        """
        # Get the unique visited nodes of the agents
        for agent in self._agents:
            self._visited_nodes.extend(agent.visited_nodes)
        # Return the dictionary
        return self._visited_nodes

    def update_pct_explored(self):
        """
        Method to get the percentage of nodes explored
        :return: Percentage of nodes explored
        """
        # Get the percentage of nodes explored
        pct_explored = len(set(self._visited_nodes)) / len(self._all_nodes) * 100
        # Return the percentage
        return pct_explored

    def facilitate_communication(self):
        """
        Method to facilitate communication between agents
        """
        pass

    def send(self, rx_agents):
        """
        Method to send transmittable to recieving agents
        """
        pass

    def receive(self, tx_agent):
        """
        Method to get transmittable from sending agent"""
        pass

    def get_agents_in_range(self, position, communication_range):
        """
        Method to get the agents in range of an agents position
        :param position: The position of the agent
        :param communication_range: The communication range of the agent
        :return: IDs of the agents in range
        """
