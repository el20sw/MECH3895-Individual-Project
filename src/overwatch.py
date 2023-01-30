# Import logger
import src.debug.logger as logger

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

    def __init__(self, environment: Network, *agents: Agent):
        # Initialise the logger
        self.log = logger.get_logger(__name__)
        # Initialise the overwatch
        self.environment = environment
        self.agents = agents
        self.num_agents = len(agents)
        self.agent_positions = {}
        self.visited_nodes = []
        self.all_nodes = self.environment.node_names
        self.turns = 0
        self.pct_explored = 0

    def update(self):
        """
        Method to update the overwatch
        :return: None
        """
        # Update the number of turns
        self.turns += 1
        self.log.info(f"Turn {self.turns}")
        # Update the percentage of nodes explored
        self.pct_explored = self.get_pct_explored()
        self.log.info(f"Percentage of nodes explored: {self.pct_explored}")
        # Update the agent positions
        self.agent_positions = self.get_agent_positions()
        self.log.info(f"Agent positions: {self.agent_positions}")
        # Update the visited nodes
        self.visited_junctions = self.get_visited_nodes()
        self.log.info(f"Visited nodes: {self.visited_junctions}")

    def get_agent_positions(self):
        """
        Method to get the positions of the agents
        :return: Dictionary of agent positions
        """
        # Get the positions of the agents
        for agent in self.agents:
            self.agent_positions[agent.id] = agent.position
        # Return the dictionary
        return self.agent_positions

    def get_visited_nodes(self):
        """
        Method to get the unique visited nodes of the agents
        :return: Dictionary of unique visited nodes
        """
        # Get the unique visited nodes of the agents
        for agent in self.agents:
            self.visited_nodes.extend(agent.visited_nodes)
        # Return the dictionary
        return self.visited_nodes

    def get_pct_explored(self):
        """
        Method to get the percentage of nodes explored
        :return: Percentage of nodes explored
        """
        # Get the percentage of nodes explored
        pct_explored = len(set(self.visited_nodes)) / len(self.all_nodes) * 100
        # Return the percentage
        return pct_explored
