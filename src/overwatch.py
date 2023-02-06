# Import logger
import src.debug.logger as logger

from typing import Any, List, Tuple

from src.network import Network
from src.agent import Agent
from src.transmittable import Transmittable

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
        self._agent_paths = {}
        self._visited_nodes = []
        self._all_nodes = self._environment.node_names
        self._turns = 0
        self._pct_explored = 0

        # Communication variables
        self._transmittables = []
        # create dictionary of agents (keys) and empty values in preparation for communication - each turn the dictionary will be updated with the transmittables to be sent to each agent
        self._communication_buffer: dict = {agent.agent_id: [] for agent in self._agents}

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
    def agent_paths(self) -> dict:
        return self._agent_paths

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

    @property
    def communication_buffer(self) -> dict:
        return self._communication_buffer

    ### Methods ###
    def add_agent(self, agent: Agent):
        """
        Method for the overwatch to accept an agent
        :param agent: Agent to be added
        :return: None
        """

        # Check if the agent is already in the list of agents
        if agent not in self._agents:
            # Add the agent to the list of agents
            self._agents.append(agent)
            
        # Update the number of agents
        self._num_agents = len(self._agents)
        # Update the agent positions
        self._agent_positions[agent.agent_id] = agent.position
        self._agent_paths[agent.agent_id] = [agent.position]
        # Update the communication buffer
        self._communication_buffer[agent.agent_id] = []

    def update(self, turns=None):
        """
        Method to update the overwatch
        :return: None
        """
        # Update the number of turns
        if turns is not None:
            self._turns = turns
            self._log.debug(f"Turn {self._turns}")
        # Update the agent positions
        self._agent_positions = self.update_agent_positions()
        self._log.debug(f"Agent positions: {self._agent_positions}")
        # Update the visited nodes
        self._visited_nodes = self.update_visited_nodes()
        self._log.debug(f"Visited nodes: {self._visited_nodes}")
        # Update the percentage of nodes explored
        self._pct_explored = self.update_pct_explored()
        self._log.debug(f"Percentage of nodes explored: {self._pct_explored}")

    def update_agent_positions(self):
        """
        Method to get the positions of the agents
        :return: Dictionary of agent positions
        """
        # Get the positions of the agents
        for agent in self._agents:
            self._agent_positions[agent.agent_id] = agent.position
            self._agent_paths[agent.agent_id].append(agent.position)
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

    def download(self, rx_agent) -> List[Transmittable]:
        """
        Method to send transmittable to recieving agents
        :param rx_agent: ID of the agent to receive the transmittable
        :return: transmittable to be sent
        """

        # If rx_agent is Agent, get the ID
        if isinstance(rx_agent, Agent):
            rx_agent_id = rx_agent.agent_id
        # Otherwise, assume rx_agent is an ID
        else:
            rx_agent_id = rx_agent

        # Get the transmittable from the communication buffer
        transmittable = self._communication_buffer[rx_agent_id]
        # log the transmittable
        self._log.debug(f"Transmittable to be sent to agent {rx_agent_id}: {transmittable}")
        # Clear the communication buffer for the agent
        self._communication_buffer[rx_agent_id] = []
        # log the communication buffer
        self._log.debug(f"Communication buffer: {self._communication_buffer}")
        # Return the transmittable
        return transmittable

    def upload(self, agent_id, transmittable: Transmittable, agents_in_range):
        """
        Method to get transmittable from sending agent
        :param agent_id: ID of the agent
        :param transmittable: Transmittable to be received
        :param agents_in_range: IDs of the agents in range
        """
        
        # Extract the agent from the agents list using the agent ID
        agent = [agent for agent in self._agents if agent.agent_id == agent_id][0]
        # Get the transmittable from the agent
        tx_transmittable = transmittable
        
        # Get the agents in range
        rx_agents = agents_in_range

        for agent in rx_agents:
            # if the transmittable is a list, for each transmittable in the list, add it to the communication buffer
            if isinstance(tx_transmittable, list):
                for transmittable in tx_transmittable:
                    self._communication_buffer[agent.id].append(transmittable)
                    self._log.debug(f"{transmittable} from {agent_id} added to agent {agent.id} communication buffer")
            else:
                # add transmittable to the communication dictionary
                self._communication_buffer[agent.id].append(tx_transmittable)
                self._log.debug(f"{transmittable} from {agent_id} added to agent {agent.id} communication buffer")

        # log the communication buffer
        self._log.debug(f"Communication buffer: {self._communication_buffer}")

    def _clear_comms_buffer(self):
        """
        Method to clear the communication buffer
        :return: None
        """
        # Clear the communication buffer
        self._communication_buffer = {agent.agent_id: [] for agent in self._agents}
         
    def get_agents_in_range(self, position, communication_range=-1):
        """
        Method to get the agents in range of an agents position
        :param position: The position of the agent
        :param communication_range: The communication range of the agent - number of nodes away; -1 for infinite range
        :return: IDs of the agents in range
        """
        if communication_range == -1:
            return self._agents
        elif communication_range == 0:
            return []
