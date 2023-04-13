import os
import json
import uuid
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
        - swarm: bool (True if swarm is enabled, False otherwise)
        - swarm_type: str (type of swarm behaviour)
            - 'naive': naive swarm behaviour
            - 'informed': informed swarm behaviour
            - 'allocation_threshold': str (threshold for allocation of resources)
                - 'mean': uses the mean score as the threshold
                - 'median': uses the median score as the threshold
                
    start_positions: list of start positions, optional (default=None)
        list of start positions for the agents
        
    filepath: str, optional (default=None)
        filepath to save the results to
    
    """

    def __init__(self, environment:Network, num_agents:int=1, swarm:bool=False, swarm_config=None, start_positions=None, filepath=None) -> None:
        # Initialise the logger
        self._log = logger.get_logger(__name__)
        
        # Initialise the simulation
        self._environment = environment
        self._network_file = environment.path_to_file
        self._log.info(f'Environment: {self._environment}')
        self._num_nodes = environment._num_nodes
        self._graph_num_nodes = environment._g_num_nodes
        self._num_links = environment._num_links
        self._graph_num_links = environment._g_num_links
        self._max_turns = 100
        
        # create unique id for this simulation
        self._timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        self._unique_id = str(uuid.uuid4())[:8]
        self._simulation_id = f'{self._timestamp}_{self._unique_id}'
        
        # create/find results directory
        if filepath is not None:
            self._results_dir = filepath
        else:
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
        if start_positions is not None:
            self._log.info(f'Generating {self._num_agents} agents with given start positions: {start_positions}')
            self._agents = agent_generator.generate_agents(self._environment, self._num_agents, threshold=self._allocation_threshold, start_positions=start_positions)
        else:
            self._log.info(f'Generating {self._num_agents} agents')
            self._agents = agent_generator.generate_agents(self._environment, self._num_agents, threshold=self._allocation_threshold)

        self._agent_clusters = []
        self._agent_positions = {}
        self._swarm = swarm
        self._start_positions = [agent.start_pos for agent in self._agents]
        # remove duplicates from start positions
        self._start_positions = list(dict.fromkeys(self._start_positions))
        
        # Variables
        self._turns = 0 
        self._pct_nodes_explored = 0
        self._pct_links_explored = 0
        self._visited_nodes = set()
        self._visited_links = set()
        # self._results = {}
        
        # Initialise the random seed
        self._random_seed: int = 0
        
        # Initialise the results
        self._results = pd.DataFrame(columns=[
            'turn', 
            'pct_nodes_explored', 
            'pct_links_explored', 
            'node_novelty_score', 
            'link_novelty_score', 
            'abs_nodes_explored', 
            'abs_links_explored'
            ])
        
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
    def run(self, max_turns:int=100, run_until_complete:bool=False, metric:str='pct_links_explored'):
        """
        Method to run the simulation
        
        Parameters
        ----------
        max_turns: int, optional (default=100)
            Maximum number of turns to run the simulation for
            
        run_until_complete: bool, optional (default=False)
            If True, the simulation will run until all nodes have been explored or the maximum number of turns has been reached
            
        metric: str, optional (default='pct_links_explored')
            Metric to use to determine if the simulation has completed
            - 'pct_nodes_explored': percentage of nodes explored
            - 'pct_links_explored': percentage of links explored
            
        return: None
        """
        
        self._max_turns = max_turns
        
        # If run until complete is false, run for max turns
        if not run_until_complete:
            self._log.info(f'Running for {self._max_turns} turns')
            # Run the simulation
            while True:
                if self._turns >= self._max_turns:
                    break
                
                self.turn()
                
        else:
            self._log.info(f'Running until {metric} is 100% or {self._max_turns} turns')
            # Run the simulation
            while True:
                # Check if the metric is 100%
                if metric == 'pct_nodes_explored':
                    if self._pct_nodes_explored >= 100:
                        break
                elif metric == 'pct_links_explored':
                    if self._pct_links_explored >= 100:
                        break
                else:
                    raise ValueError(f'Invalid metric: {metric}')
                # Check if the max turns has been reached
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
            
        # Calculate the percentage of nodes explored
        # self._pct_nodes_explored = len(self._visited_nodes) / self._num_nodes * 100
        
        # Use the number of nodes in the graph rather than from the WNTR network as the 
        # WNTR network may have nodes that the agents cannot reach
        self._pct_nodes_explored = len(self._visited_nodes) / self._graph_num_nodes * 100
        
    def _update_visited_links(self):
        for agent in self._agents:
            self._visited_links.add(agent.link)
        
        # Calculate the percentage of links explored
        # self._pct_links_explored = len(self._visited_links) / self._num_links * 100
        
        # Use the number of links in the graph rather than from the WNTR network as the
        # WNTR network may have links that the agents cannot reach/use
        self._pct_links_explored = len(self._visited_links) / self._graph_num_links * 100
        
    def _node_novelty_score(self):
        # Get the number of new nodes visited this turn, new nodes are nodes that have not been previously visited by any agent
        new_nodes = set()
        for agent in self._agents:
            new_nodes.add(agent.position)
            
        # Get the proportion of new nodes not in the visited nodes set
        node_novelty_score = len(new_nodes - self._visited_nodes) / len(new_nodes)
        
        self._log.debug(f'Turn: {self._turns} - New nodes: {new_nodes}')
        self._log.debug(f'Turn: {self._turns} - Visited nodes: {self._visited_nodes}')
        self._log.debug(f'Turn: {self._turns} - Node Novelty score: {node_novelty_score}')
        
        return node_novelty_score
    
    def _link_novelty_score(self):
        # Get the number of new links visited this turn, new links are links that have not been previously visited by any agent
        new_links = set()
        for agent in self._agents:
            new_links.add(agent.link)
            
        # Get the proportion of new links not in the visited links set
        link_novelty_score = len(new_links - self._visited_links) / len(new_links)
        
        self._log.critical(f'Turn: {self._turns} - New links: {new_links}')
        self._log.critical(f'Turn: {self._turns} - Visited links: {self._visited_links}')
        self._log.critical(f'Turn: {self._turns} - Link Novelty score: {link_novelty_score}')
        
        return link_novelty_score
        
    def _update_results_df(self, **kwargs):
        self._log.debug('Updating results')
        
        # self._update_agent_positions()
        # self._update_visited_nodes()
        
        self._results.loc[self._turns, 'turn'] = self._turns
        self._results.loc[self._turns, 'pct_nodes_explored'] = self._pct_nodes_explored
        self._results.loc[self._turns, 'pct_links_explored'] = self._pct_links_explored
        self._results.loc[self._turns, 'abs_nodes_explored'] = len(self._visited_nodes)
        self._results.loc[self._turns, 'abs_links_explored'] = len(self._visited_links)
        
        self._log.debug(f"Turn {self._turns} added to results dataframe")
        self._log.debug(f"Percentage of nodes explored {self._pct_nodes_explored} added to results dataframe (num nodes: {self._num_nodes})")
        self._log.debug(f"Percentage of links explored {self._pct_links_explored} added to results dataframe (num links: {self._num_links})")
        self._log.debug(f"Absolute number of nodes explored {len(self._visited_nodes)} added to results dataframe")
        self._log.debug(f"Absolute number of links explored {len(self._visited_links)} added to results dataframe")
        
        # If novelty_score is in kwargs, add it to the results dataframe
        if 'node_novelty_score' in kwargs:
            self._results.loc[self._turns, 'node_novelty_score'] = kwargs['node_novelty_score']
            self._log.debug(f"Node Novelty score {kwargs['node_novelty_score']} added to results dataframe")
            
        if 'link_novelty_score' in kwargs:
            self._results.loc[self._turns, 'link_novelty_score'] = kwargs['link_novelty_score']
            self._log.debug(f"Link Novelty score {kwargs['link_novelty_score']} added to results dataframe")
    
    def _update_results(self):
        self._log.debug('Updating results')
        
        self._update_agent_positions()
        node_novelty_score = self._node_novelty_score()
        link_novelty_score = self._link_novelty_score()
        self._update_visited_nodes()
        self._update_visited_links()
        self._update_results_df(node_novelty_score=node_novelty_score, link_novelty_score=link_novelty_score)
        
    def _save_results(self):
        self._log.debug('Saving results')

        self._results_agents['path'] = [agent.node_path for agent in self._agents]
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
    def pct_nodes_explored(self) -> float:
        """
        Returns the percentage of nodes explored
        """
        return self._pct_nodes_explored
    
    @property
    def pct_links_explored(self) -> float:
        """
        Returns the percentage of links explored
        """
        return self._pct_links_explored
    
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
    