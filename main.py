import tkinter as tk
from tkinter import filedialog

import logging

from src.simulation import Simulation
from src.network import Network
from src.agent import Agent
from src.render import Render

logging.disable(logging.CRITICAL)

def create_simulation(network_file, number_of_agents:int, turn_limit:int, swarm:bool):
    # code for creating simulation with the given parameters
    print(f"""\nRunning simulation with parameters:
            network_file={network_file},
            number_of_agents={number_of_agents},
            turn_limit={turn_limit},
            swarm={swarm}\n""")
    
    env = Network(network_file)
    simulation = Simulation(env, number_of_agents, swarm)
    
    # Run the simulation
    print("\nRunning simulation...")
    simulation.run(max_turns=turn_limit)
    
    # Create animation
    render = Render(simulation)
    render.render()
    
    print("\nSaving results...")
    print(f"\nResults found at: {simulation.path_to_results_directory}")
    
def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Network files", "*.inp")])
    return file_path
    
if __name__ == "__main__":
    
    network_file = input("Enter path to network file (or press enter to select a file): ") or select_file()
    number_of_agents = int(input("Enter number of agents: ") or 10)
    turn_limit = int(input("Enter maximum number of turns: ") or 100)
    swarm_choice = input("Swarm? (y/n): ") or "n"
    swarm = True if swarm_choice.lower() == "y" else False
    
    create_simulation(network_file, number_of_agents, turn_limit, swarm)
    