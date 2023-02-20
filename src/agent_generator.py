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

def generate_agents(env: Network, num_agents: int, random_seed:int=0  ) -> List[Agent]:
    """
    Method to generate a list of agents for the simulation
    
    Parameters
    ----------
    
    env: environment for the agents to be generated in
    num_agents: number of agents to generate
    random_seed: random seed for the generation of the agents
    
    Returns
    -------
    return: list of agents
    """
    
    # Ask the user for the start positions
    # start_positions = ask_start_positions(env)
    
    # Generate the agents
    agents = [Agent(env, agent_id, start_pos) for agent_id, start_pos in generate_start_positions(env, num_agents)]
    # Return the agents
    return agents

def generate_start_positions(env: Network, num_agents: int, start_postitions=None, random_seed:int=0) -> List[tuple]:
    """
    Method to generate a list of start positions for the agents
    
    Parameters
    ----------
    
    env: environment for the agents to be generated in
    num_agents: number of agents to generate
    num_start_pos: number of start positions to generate
    random_seed: random seed for the generation of the agents
    
    Returns
    -------
    return: list of start positions
    """
    # Set the random seed
    random.seed(random_seed)
    
    # If the start positions are not given
    if start_postitions is None:
        # Generate the start positions
        start_positions = [(agent_id, 'Lake') for agent_id in range(num_agents)]
        return start_positions
    
    start_positions = []
    # Return the start positions
    return start_positions
    
def ask_start_positions(env: Network):
    """
    Method to ask the user for the start positions of the agents
    """
    
    # Get the list of nodes
    nodes = list(env.node_names)
    # Create TKinter window for the selection of the start positions
    root = tk.Tk()
    # Create the listbox
    listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
    # Add the nodes to the listbox
    for node in nodes:
        listbox.insert(tk.END, node)
    # Pack the listbox
    listbox.pack()
    # Create the button
    button = tk.Button(root, text='OK', command=root.destroy)
    # Pack the button
    button.pack()
    # Run the mainloop
    root.mainloop()
    
    # Get the selected nodes
    
    
    
    return None
        