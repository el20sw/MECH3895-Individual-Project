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

def generate_agents(env: Network, num_agents: int, num_start_pos:int=1, random_seed:int=0) -> List[Agent]:
    """
    Method to generate a list of agents for the simulation
    
    Parameters
    ----------
    
    env: environment for the agents to be generated in
    num_agents: number of agents to generate
    num_start_pos: number of start positions to generate
    random_seed: random seed for the generation of the agents
    
    Returns
    -------
    return: list of agents
    """   
    
    # Generate the agents
    agents = [Agent(env, agent_id, start_pos) for agent_id, start_pos in generate_start_positions(env, num_agents, num_start_pos, random_seed)]
    # Return the agents
    return agents

def generate_start_positions(env: Network, num_agents: int, num_start_pos:int=1, random_seed:int=0) -> List[tuple]:
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
    
    # # Create TKinter containing the map of the network and a selection of start positions
    # root = tk.Tk()
    # root.title("Select Start Positions")
    # root.geometry("800x600")
    # root.resizable(False, False)
    # # Create the canvas
    # canvas = tk.Canvas(root, width=800, height=600)
    # canvas.pack()
    # # Create the map image
    # wntr.graphics.plot_network(env.water_network_model, node_size=5, node_labels=True, filename="temp/map.png")
    # # Create the map
    # map = tk.PhotoImage(file="temp/map.png")
    # canvas.create_image(0, 0, anchor=tk.NW, image=map)
    # # Create the start positions
    # start_positions = []
    
    # Generate the start positions
    start_positions = [(agent_id, 'Lake') for agent_id in range(num_agents)]
    # Return the start positions
    return start_positions