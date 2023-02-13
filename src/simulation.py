# Import logger
import src.debug.logger as logger

from typing import List
import json
import os
import random

from src.agents.agent import Agent
from src.network import Network
from src.overwatch import Overwatch

### Simulation Class ###
class Simulation:
    """
    Simulation Class
    ----------
    Class to simulate the pipe network environment
    :param environment: Network object
    """

    def __init__(self, environment: Network):
        # Initialise the logger
        self._log = logger.get_logger(__name__)
        # Initialise the simulation
        self._environment = environment
        self._log.info(f'Environment: {self._environment}')
        self._num_nodes = environment._num_nodes

        # Initialise the agents
        self._agents: List[Agent] = []
        self._num_agents = 0

        # Variables
        self._turns = 0
        self._pct_explored = 0
        self._results = {}

        # Initialise the overwatch
        self._overwatch = Overwatch(self._environment, self._agents)
        
        # Initialise the random seed
        random.seed(0)

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

    @property
    def results(self):
        self._results_from_overwatch()
        return self._results

    @property
    def overwatch(self) -> Overwatch:
        return self._overwatch

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
                self._log.warning(f"Agent {a.agent_id} already in simulation")
                return
            if a in self._overwatch.agents:
                self._log.warning(f"Agent {a.agent_id} already in simulation")
                return
            # Add the agent to the simulation agent list
            self._agents.append(a)
            # Add the agent to the overwatch
            self._overwatch.add_agent(a)
            self._log.info(f"Agent {a.agent_id} added to simulation")
            # Update the pct_explored
            self._pct_explored = self._overwatch.pct_explored

        # Update the number of agents
        self._num_agents = len(self._agents)

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
            if self._turns == 0:
                # Log the agents positions
                for agent in self._agents:
                    self._log.debug(f"Agent {agent.agent_id} is at {agent.position}")
            # Run one step of the simulation
            self.step()
            # Get results from the overwatch
            self._results_from_overwatch()
            # Update the percentage of the environment explored
            self._pct_explored = self._overwatch.pct_explored
            if self._pct_explored == 100:
                # update overwatch
                self._overwatch.update(turns=self._turns)
                # write results to file
                self._overwatch.write_results()
                
                self._log.info(f"Simulation complete - {self._pct_explored}% of environment explored")

                self._log.debug(f'Nodes explored: {sorted(set(self._overwatch.visited_nodes))}')
                self._log.debug(f'All nodes: {sorted(self._overwatch.all_nodes)}')

                for agent in self._agents:
                    self._log.debug(f"Agent {agent.agent_id} path: {self._overwatch.agent_paths[agent.agent_id]}")
                    self._log.debug(f"Agent {agent.agent_id} path length: {len(self._overwatch.agent_paths[agent.agent_id]) - 1}")

                self._log.info(f'It took {self._num_agents} agent(s) {self._turns} to explore {self._num_nodes} nodes')

                break
            
            # Write the results to a file
            self._overwatch.write_results()

            # Log the percentage of the environment explored
            self._log.info(f"Percentage of environment explored: {self._pct_explored}%")
            
            # Log the agents positions
            for agent in self._agents:
                self._log.info(f"Agent {agent.agent_id}: {agent.previous_position} -> {agent.position}")

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

        # Log the turn beginning
        self._log.info(f"Turn {self._turns} - (Sim) {self.overwatch.turns} - (Overwatch) beginning")

        # iterate through agents and call observe method for each agent
        for agent in self._agents:
            agent.observe(self._environment)

        # iterate through agents and call communicate method for each agent
        # for agent in self._agents:
        #     agent.communicate(self._overwatch)

        # iterate through agents and call communicate method for each agent - 2 parts (send and recieve)
        for agent in self._agents:
            agent.comms_part1(self._overwatch)

        for agent in self._agents:
            agent.comms_part2(self._overwatch)

        # iterate through agents and call action method 
        for agent in self._agents:
            agent.action()

        # iterate through agents and call move method
        for agent in self._agents:
            agent.move()

        # Update the number of turns
        self._turns += 1

        # Update the overwatch
        self._overwatch.update(self._turns)

        # Log the turn ending
        self._log.info(f"Turn {self._turns} - (Sim) {self.overwatch.turns} - (Overwatch) ending")
            
    def save_results(self):
        """
        :py:meth:`save_results` method to save the results of the simulation
        Returns the path to the results file
        """
        
        path = self.overwatch._save_results()
        return path
        
            
    def get_random_positions(self, num_agents: int):
        """
        :py:meth:`get_random_positions` method to get random starting positions for
        the agents in the simulation
        """
        
        # Get the number of nodes in the environment
        num_nodes = self._environment.num_nodes
        # Get the nodes in the environment
        nodes = self._environment.node_names
        # Make sure that the number of agents is less than the number of nodes
        if num_agents > num_nodes:
            raise ValueError(f"Number of agents ({num_agents}) must be less than the number of nodes ({num_nodes})")
        # Get a random sample of nodes
        random_nodes = random.sample(nodes, num_agents)
        # Return the random nodes
        return random_nodes
    
    def _results_from_overwatch(self):
        """
        Method to get the results from the overwatch
        :return: None
        """
        # Get the results from the overwatch
        pct_explored = self._overwatch.pct_explored
        turns = self._overwatch.turns
        # Check that turns is equal to the number of turns logged by the simulation
        if turns != self._turns:
            self._log.warning(f"Number of turns in overwatch ({turns}) does not match number of turns in simulation ({self._turns})")
        
        self._results = {
            "pct_explored": pct_explored,
            "turns": turns,
            "num_agents": self._num_agents,
        }

    def _write_results(self, filename: str):
        """
        Method to write the results of the simulation to a JSON file
        :param filename: Name of the file to write to
        :return: None
        """

        # Get the results
        self._results_from_overwatch()

        # Check if the directory exists
        if not os.path.exists(os.path.dirname(filename)):
            # If it doesn't, create it
            os.makedirs(os.path.dirname(filename))
        
        # Try to write the adjacency list to a file
        try:
            with open(filename, 'w') as f:
                json.dump(self._results, f)
        # If there is an error, log it
        except Exception as e:
            self._log.error(f"Error writing adjacency list to file: {e}")
    