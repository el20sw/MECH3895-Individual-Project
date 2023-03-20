import tkinter as tk
from tkinter import filedialog

import logging

from src.simulation import Simulation
from src.network import Network
from src.render import Render

logging.disable(logging.CRITICAL)

def create_simulation(network_file, number_of_agents:int, turn_limit:int, swarm:bool, render:bool, swarm_type):
    
    # if swarm_type is None, swarm is False
    if swarm_type is None:
        print(f"""\nRunning simulation with parameters:
        network_file={network_file},
        number_of_agents={number_of_agents},
        turn_limit={turn_limit},
        swarm={swarm},
        render={render}\n""")
        
        swarm_config = None
        
    # else if swarm_type is a string, it is naive
    elif isinstance(swarm_type, str):
        print(f"""\nRunning simulation with parameters:
        network_file={network_file},
        number_of_agents={number_of_agents},
        turn_limit={turn_limit},
        swarm={swarm}
        swarm_type={swarm_type}
        render={render}\n""")
        
        swarm_config = {'swarm': swarm, 'swarm_type': swarm_type}
    
    # else if swarm_type is a tuple, unpack it and print swarm_type and allocation_threshold
    elif isinstance(swarm_type, tuple):
        swarm_type, allocation_threshold = swarm_type
        print(f"""\nRunning simulation with parameters:
        network_file={network_file},
        number_of_agents={number_of_agents},
        turn_limit={turn_limit},
        swarm={swarm},
        swarm_type={swarm_type},
        allocation_threshold={allocation_threshold},
        render={render}\n""")
        
        swarm_config = {'swarm': swarm, 'swarm_type': swarm_type, 'allocation_threshold': allocation_threshold}
        
    else:
        print("Invalid Settings")
        return
            
    # Create network and simulation
    env = Network(network_file)
    simulation = Simulation(env, number_of_agents, swarm, swarm_config=swarm_config)
    
    # Run the simulation
    print("\nRunning simulation...")
    simulation.run(max_turns=turn_limit)
    
    # Create animation if render is True
    if render:
        print("\nRendering simulation...")
        r = Render(simulation)
        r.render()
    
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
    swarm_type = None
    if swarm:
        swarm_type = input("Enter swarm type (naive or informed): ") or "naive"
        # process swarm type input to be lowercase and remove whitespace
        swarm_type = swarm_type.lower().strip()
        # if swarm_type is informed, ask if the threshold should be median or mean
        if swarm_type == "informed":
            allocation_threshold = input("Enter swarm type (median or mean): ") or "median"
            # process input to be lowercase and remove whitespace
            allocation_threshold = allocation_threshold.lower().strip()
            # if allocation_threshold is not median or mean, set it to median
            if allocation_threshold != "median" and allocation_threshold != "mean":
                allocation_threshold = "median"
            # bundle swarm_type and allocation_threshold into a tuple
            swarm_type = (swarm_type, allocation_threshold)
    
    render_choice = input("Render? (y/n): ") or "n"
    render = True if render_choice.lower() == "y" else False

    create_simulation(network_file, number_of_agents, turn_limit, swarm, render, swarm_type)

    
        # print(f"""\nRunning simulation with parameters:
    #         network_file={network_file},
    #         number_of_agents={number_of_agents},
    #         turn_limit={turn_limit},
    #         swarm={swarm},
    #         render={render}\n""")
    