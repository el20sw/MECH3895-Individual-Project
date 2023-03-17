"""
Module for the generation and insertion of agents into the simulation.
"""

from typing import List
import random

import tkinter as tk
import wntr

import src.debug.logger as logger
from src.agent import Agent
from src.network import Network

log = logger.get_logger(__name__)

def generate_agents(env: Network, num_agents: int, threshold=None, random_seed:int=0) -> List[Agent]:
    """
    Method to generate a list of agents for the simulation
    
    Parameters
    ----------
    
    env: Network
        environment for the agents to be generated in
    num_agents: int
        number of agents to generate
    threshold: str, optional (default=None)
        threshold for the agents to use when allocating tasks in an informed way
    random_seed: int, optional (default=0)
        random seed for the generation of the agents
    
    Returns
    -------
    return: list of agents
    """
    
    # Ask the user for the start positions
    # start_positions = ask_start_positions(env)
    
    print("Creating agents...")
    
    if isinstance(threshold, str):
        # process the threshold string
        threshold = threshold.lower().strip()
    
    # Generate the agents
    agents = [Agent(env, agent_id, start_pos, threshold) for agent_id, start_pos in generate_start_positions(env, num_agents)]
    # Return the agents
    return agents

def generate_start_positions(env: Network, num_agents: int, random_seed:int=0) -> List[tuple]:
    """
    Method to generate a list of start positions for the agents
    
    Parameters
    ----------
    
    env: Network
        environment for the agents to be generated in
    num_agents: int
        number of agents to generate
    random_seed: int, optional (default=0)
        random seed for the generation of the agents
    
    Returns
    -------
    list of agent start positions
    """
    # Set the random seed
    random.seed(random_seed)
    
    # ask for start positions
    start_positions = ask_start_positions(env)
    
    # If start positions is None, raise an error
    if start_positions is None:
        raise ValueError("Start positions are not valid")
    
    # Assign the start positions to the agents - round robin style so agents are evenly distributed across the start positions
    start_positions = [(agent_id, start_positions[agent_id % len(start_positions)]) for agent_id in range(num_agents)]
    
    print(f"Got start positions...")
    
    return start_positions
    
    
def ask_start_positions(env: Network):
    """
    Method to ask the user for the start positions of the agents
    
    Parameters
    ----------
    
    env: Network
        environment for the agents to be generated in
        
    Returns
    -------
    list of start positions
    """
    
    # Ask the user for the start positions
    num_start_pos = int(input("Enter number of start positions: "))
    start_positions = []
    for i in range(num_start_pos):
        start_pos = input(f"Enter start position {i+1}: ")
        start_positions.append(start_pos)
    
    # Check that the start positions are valid
    for start_pos in start_positions:
        if start_pos not in env.node_names:
            log.critical(f"Start position {start_pos} is not a valid node in the network")
            raise ValueError(f"Start position {start_pos} is not a valid node in the network")
    
    return start_positions
        