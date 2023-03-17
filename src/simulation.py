import os
import json
import datetime
import pandas as pd
from typing import List

import src.debug.logger as logger

from src.agent import Agent
from src.network import Network

import src.agent_generator as agent_generator
import src.communication as communication

### Simulation Class ###
class Simulation:
    """
    Simulation Class
    -----------------
    Class to simulate the pipe network environment and the agents within it
    
    Parameters
    ==========
    
    environment: Network object
        The network environment to simulate agents operating in
    num_agents: int
        The number of agents to simulate
    swarm: bool
        Whether the agents should communicate with each other
    swarm_config: dict, optional (default=None)
        Configuration for the swarm behaviour of the agents
    
    """

    def __init__(self, environment:Network, num_agents:int=1, swarm:bool=False, swarm_config=None) -> None:
        # Initialise the logger
        self._log = logger.get_logger(__name__)
        
        # Initialise the simulation
        self._environment = environment
        self._network_file = environment.path_to_file
        self._log.info(f'Environment: {self._environment}')
        self._num_nodes = environment._num_nodes
        self._max_turns = 100
        
        # create unique id for this simulation
        self._simulation_id = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # create/find results directory
        self._results_dir = 'results'
        # create subdirectory for this simulation
        self._results_subdir = f'{self._results_dir}/simulation_{self._simulation_id}'
        # create directory
        os.makedirs(self._results_subdir, exist_ok=True)
        
        # Initialise the swarm
        self._swarm_config = swarm_config
        if self._swarm_config is not None:
            self._swarm = True
            self._swarm_type = self._swarm_config['swarm_type']
            try:
                self._allocation_threshold = self._swarm_config['allocation_threshold']
            except KeyError:
                self._allocation_threshold = None
        else:
            self._swarm = False
            self._swarm_type = None
            self._allocation_threshold = None
        
        if self._swarm_type == 'informed':
            self._informed = True
        else:
            self._informed = False
            

        # Initialise the agents
        self._num_agents = num_agents
        self._agents = agent_generator.generate_agents(self._environment, self._num_agents, threshold=self._allocation_threshold)
        self._agent_clusters = []
        self._agent_positions = {}
        self._swarm = swarm
        self._start_positions = [agent.start_pos for agent in self._agents]
        # remove duplicates from start positions
        self._start_positions = list(dict.fromkeys(self._start_positions))
        
        # Variables
        self._turns = 0 
        self._pct_explored = 0
        self._visited_nodes = set()
        # self._results = {}
        
        # Initialise the random seed
        self._random_seed: int = 0
        
        # Initialise the results
        self._results = pd.DataFrame(columns=['turn', 'pct_explored'])
        self._results_agents = pd.DataFrame(columns=['agent_id', 'start_pos', 'path'])
        # Add agents to results agents
        self._results_agents['agent_id'] = [agent.agent_id for agent in self._agents]
        self._results_agents['start_pos'] = [agent.start_pos for agent in self._agents]
        
        # create file for results
        self._results_csv_file = f'{self._results_subdir}/results.csv'
        self._agent_results_csv_file = f'{self._results_subdir}/agent_results.csv'
        self._config_json_file = f'{self._results_subdir}/config.json'
        
        # create temporary file for image of network
        self._network_image_file = f'{self._results_subdir}/network.png'
        # save image of network
        self._environment.save_image(self._network_image_file)
        

    ### Methods ###
    def run(self, max_turns:int=100):
        """
        Method to run the simulation
        return: None
        """
        
        self._max_turns = max_turns
        
        # Run the simulation
        while True:
            if self._turns >= self._max_turns:
                break
            
            self.turn()
            
            
        # Save the results
        self._save_results()
    
    def turn(self):
        """
        Method to step the simulation forward one turn
        return: None
        """
        # Log the turn
        self._log.info(f'Turn: {self._turns}')
        # Update the agents
        self.comms_state()
        self.decide_state()
        self.action_state()
        # Update results
        self._update_results()
        # Update the turn
        self._turns += 1
    
    def comms_state(self):
        self._log.debug('Comms State')
        
        # If swarm, all agents communicate
        if not self._swarm:
            self._log.debug('Collaboration not enabled')
            return
        
        # Each agent pings
        for agent in self._agents:
            agent.ping(self._agents)
            # self._log.debug(f'{agent} has pinged')
            
        # Get the clusters
        self._agent_clusters = self._get_clusters()
        for cluster in self._agent_clusters:
            cluster_pos = set(agent.position for agent in cluster)
            self._log.debug(f'{cluster_pos} Cluster: {cluster}')
            
        # If there are clusters, agents in the same cluster communicate
        if self._agent_clusters:
            self._log.debug('Communicating')
            for cluster in self._agent_clusters:
                self._log.debug(f'Cluster: {cluster}')
                communication.communicate(cluster, self._environment, informed=self._informed)
                    
    def decide_state(self):
        self._log.debug('Decide State')
        
        # Each agent decides
        for agent in self._agents:
            agent.decide(self._swarm)
            self._log.debug(f'{agent} decided')
                    
    def action_state(self):
        self._log.debug('Action State')
        
        # Each agent moves
        for agent in self._agents:
            agent.move()
            self._log.debug(f'Agent {agent.agent_id} moved {agent.previous_node} -> {agent.position}')
            
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
    
    def _update_agent_positions(self):
        self._agent_positions = {}
        for agent in self._agents:
            self._agent_positions[agent.agent_id] = agent.position
            
    def _update_visited_nodes(self):
        for agent in self._agents:
            self._visited_nodes.add(agent.position)
            
        self._pct_explored = len(self._visited_nodes) / self._num_nodes * 100
        
    def _update_results_df(self):
        self._log.debug('Updating results')
        
        self._update_agent_positions()
        self._update_visited_nodes()
        
        self._results.loc[self._turns, 'turn'] = self._turns
        self._results.loc[self._turns, 'pct_explored'] = self._pct_explored
        self._log.debug(f"Turn {self._turns} added to results dataframe")
        self._log.debug(f"Percentage of nodes explored {self._pct_explored} added to results dataframe (num nodes: {self._num_nodes})")
    
    def _update_results(self):
        self._log.debug('Updating results')
        
        self._update_agent_positions()
        self._update_visited_nodes()
        self._update_results_df()
        
    def _save_results(self):
        self._log.debug('Saving results')

        self._results_agents['path'] = [agent.path for agent in self._agents]
        self._results_agents.to_csv(self._agent_results_csv_file, index=False)
        
        self._results.to_csv(self._results_csv_file, index=False)
        
        self._write_config()
        
    def _write_config(self):
        self._log.debug('Writing config')
        
        try:
            with open(self._config_json_file, 'w') as f:
                json.dump(self.params, f, indent=4)
                f.close()
        except Exception as e:
            self._log.error(f"Error writing config file: {e}")

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
        
    ### Attributes ###
    @property
    def environment(self) -> Network:
        """
        Returns the environment
        """
        return self._environment

    @property
    def agents(self) -> List[Agent]:
        """
        Returns the agents
        """
        return self._agents

    @property
    def num_agents(self) -> int:
        """
        Returns the number of agents
        """
        return self._num_agents

    @property
    def turns(self) -> int:
        """
        Returns the number of turns
        """
        return self._turns
    
    @property
    def max_turns(self) -> int:
        """
        Returns the maximum number of turns
        """
        return self._max_turns

    @property
    def pct_explored(self) -> float:
        """
        Returns the percentage of nodes explored
        """
        return self._pct_explored
    
    @property
    def random_seed(self) -> int:
        return self._random_seed
    
    @property
    def path_to_results_file(self):
        return self._results_csv_file
    
    @property
    def path_to_agents_results_file(self):
        return self._agent_results_csv_file
    
    @property
    def path_to_results_directory(self):
        """
        Path to the results directory
        """
        return self._results_subdir
    
    @property
    def params(self):
        """
        Returns the parameters of the simulation
        """
        return {
            'network_file': self._network_file,
            'num_agents': self._num_agents,
            'turns': self._max_turns,
            'swarm': self._swarm,
            'swarm_type': self._swarm_type,
            'allocation_threshold': self._allocation_threshold,
            'start_position': self._start_positions,
        }
    