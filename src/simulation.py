# Import logger
import src.debug.logger as logger

from typing import List
import json

from src.agent import Agent
from src.network import Network
from src.overwatch import Overwatch

### Simulation Class ###
class Simulation:
    """
    Simulation Class
    ----------
    Class to simulate the pipe network environment
    """

    def __init__(self, environment: Network):
        # Initialise the logger
        self._log = logger.get_logger(__name__)
        # Initialise the simulation
        self._environment = environment
        self._log.info(f'Environment: {self._environment}')

        # Initialise the agents
        self._agents: List[Agent] = []
        self._num_agents = 0

        # Variables
        self._turns = 0
        self._pct_explored = 0

        # Initialise the overwatch
        self._ow = Overwatch(self._environment, self._agents)

    ### Attributes ###
    @property
    def environment(self) -> Network:
        return self._environment

    @property
    def agents(self) -> List[Agent]:
        return self._agents

    @property
    def num_agents(self) -> int:
        return self._num_agents

    @property
    def turns(self) -> int:
        return self._turns

    @property
    def pct_explored(self) -> float:
        return self._pct_explored

    ### Methods ###
    def add_agent(self, *agent : Agent):
        """
        Method to add an agent to the simulation - can be used to add multiple agents
        :param agent: Agent/s to add
        :return: None
        """
        
        # check if agent is aleady in the simulation
        for a in agent:
            if a in self._agents:
                self._log.warning(f"Agent {a.id} already in simulation")
                return
            # Add the agent
            self._agents.append(a)
            self._log.info(f"Agent {a.id} added to simulation")

        # Update the number of agents
        self._num_agents = len(self._agents)

        # Update the overwatch
        self._ow.agents = self._agents

    def remove_agent(self, agent : Agent):
        """
        Method to remove an agent from the simulation
        :param agent: Agent to remove
        :return: None
        """
        # Remove the agent
        self._agents.remove(agent)
        # Update the number of agents
        self._num_agents = len(self._agents)

    def run(self, max_turns=100):
        """
        Method to run the simulation
        :param max_turns: Maximum number of turns to run the simulation for
        :return: None
        """
        # Run the simulation for a maximum number of turns
        while self._turns < max_turns and self._pct_explored < 100:
            # Run one step of the simulation
            self.step()
            # Increment the turn
            self._turns += 1
            # Log the turn
            self._log.info(f"Turn {self._turns} complete")
            # Log the percentage of the environment explored
            self._log.info(f"Percentage of environment explored: {self._pct_explored}%")
            # Log the agents positions
            for agent in self._agents:
                self._log.info(f"Agent {agent.id} is at {agent.position}")

    def step(self):
        """
        Method to run one step of the simulation - this is a turn

        Turns are run in the following order:
        1. Agents observe the environment
            1.1. Agents update their knowledge of the environment (based on local observations)
        2. Agents communicate with each other (if they are in range)
            2.1. Agents update their knowledge of the environment (based on communication)
        3. Agents determine what action they will take next
        4. Agents move to their new position

        :return: None
        """
        # Run one step for each agent
        for agent in self._agents:
            agent.step()

        # Update the overwatch
        self._ow.update()

    def _update(self):
        """
        Method to update the simulation
        :return: None
        """
        # Update the overwatch
        self._ow.update()

        # Update the percentage of the environment explored
        self._pct_explored = self._ow.pct_explored
        # Update the number of agents
        self._num_agents = len(self._agents)

    def get_results(self):
        """
        Method to get the results of the simulation
        :return: Dictionary of results
        """

        # Update the simulation
        self._update()

        results = {
            'num_agents': self._num_agents,
            'turns': self._turns,
            'visited_nodes': self._ow.visited_nodes,
            'pct_explored': self._pct_explored
        }

        return results

    def write_results(self, filename: str):
        """
        Method to write the results of the simulation to a JSON file
        :param filename: Name of the file to write to
        :return: None
        """

        # Get the results
        results = self.get_results()

        # Write the results to a JSON file
        with open(filename, 'w') as f:
            json.dump(results, f)
