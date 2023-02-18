# Import logger
import src.debug.logger as logger

from typing import List
import json
import os
import random

from src.agent import Agent
from src.network import Network

import src.agent_generator as agent_generator
import src.communication as communication

### Simulation Class ###
class Simulation:
    """
    Simulation Class
    ----------
    Class to simulate the pipe network environment
    :param environment: Network object
    """

    def __init__(self, environment:Network, num_agents:int=1) -> None:
        # Initialise the logger
        self._log = logger.get_logger(__name__)
        # Initialise the simulation
        self._environment = environment
        self._log.info(f'Environment: {self._environment}')
        self._num_nodes = environment._num_nodes
        self._max_turns = 100

        # Initialise the agents
        self._num_agents = num_agents
        self._agents = agent_generator.generate_agents(self._environment, self._num_agents)
        self._agent_clusters = []

        # Variables
        self._turns = 0 
        self._pct_explored = 0
        self._results = {}

        # Initialise the overwatch
        # self._overwatch = Overwatch(self._environment, self._agents)
        
        # Initialise the random seed
        self._random_seed: int = 0

    ### Methods ###
    
    def comms_state(self):
        # Each agent pings
        for agent in self._agents:
            agent.ping(self._agents)
            self._log.debug(f'{agent} has pinged')
            
        # Get the clusters
        self._agent_clusters = self._get_clusters()
        for cluster in self._agent_clusters:
            self._log.debug(f'Cluster: {cluster}')
            
        # If there are clusters, agents in the same cluster communicate
        if self._agent_clusters:
            for cluster in self._agent_clusters:
                communication.communicate(cluster, self._environment)
                    
    def decide_state(self):
        # Each agent decides
        # for agent in self._agents:
        #     agent.decide()
        #     self._log.debug(f'{agent} decided')
        pass
                    
    def action_state(self):
        # Each agent moves
        for agent in self._agents:
            agent.move()
            self._log.debug(f'{agent} moved')
            
    def _get_clusters(self):
        # Get the clusters
        clusters = []
        # Use each agents ping list to get the clusters
        for agent in self._agents:
            # Check if the agent is in a cluster
            if all([agent not in cluster for cluster in clusters]):
                # If not, create a new cluster
                clusters.append([agent])
                # Add the agents in the ping list to the cluster
                for ping in agent.agents_in_range:
                    clusters[-1].append(ping)
                    
        # Remove any clusters with only one agent
        clusters = [cluster for cluster in clusters if len(cluster) > 1]

        # Return the clusters
        return clusters
            
            

    # def _write_results(self, filename: str):
    #     """
    #     Method to write the results of the simulation to a JSON file
    #     :param filename: Name of the file to write to
    #     :return: None
    #     """

    #     # Get the results
    #     self._results_from_overwatch()

    #     # Check if the directory exists
    #     if not os.path.exists(os.path.dirname(filename)):
    #         # If it doesn't, create it
    #         os.makedirs(os.path.dirname(filename))
        
    #     # Try to write the adjacency list to a file
    #     try:
    #         with open(filename, 'w') as f:
    #             json.dump(self._results, f)
    #     # If there is an error, log it
    #     except Exception as e:
    #         self._log.error(f"Error writing adjacency list to file: {e}")
            
    # def _params_to_overwatch(self):
    #     """
    #     Method to pass the parameters of the simulation to the overwatch
    #     :return: None
    #     """
    #     # Get the parameters of the simulation
    #     params = self.params
    #     # Pass the parameters to the overwatch
    #     self._overwatch._sim_params = params
        
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
    def max_turns(self) -> int:
        return self._max_turns

    @property
    def pct_explored(self) -> float:
        return self._pct_explored

    # @property
    # def results(self):
    #     self._results_from_overwatch()
    #     return self._results

    # @property
    # def overwatch(self) -> Overwatch:
    #     return self._overwatch
    
    @property
    def random_seed(self) -> int:
        return self._random_seed
    
    @property
    def params(self):
        """
        Simulation parameters
        """
        return {
            'random_seed': self._random_seed,
            'max_turns': self._max_turns,
        }
    