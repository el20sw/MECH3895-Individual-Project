import platform
import subprocess
import random
import tkinter as tk
from tkinter import filedialog

# supress all logging
import logging
logging.disable(logging.CRITICAL)

from src.simulation import Simulation
from src.network import Network
from src.agents import random_agent, greedy_agent, behavioural_agent
from src.render import Render

def create_simulation(agent_type,
                      num_agents,
                      start_position,
                      comm_range,
                      network_file,
                      turn_limit,):
    
    # set random seed
    random.seed(0)
    
    AGENT_CLASSES = {
        "random": random_agent.RandomAgent,
        "greedy": greedy_agent.GreedyAgent,
        "behavioural": behavioural_agent.BehaviouralAgent
    }
    
    # code for creating simulation with the given parameters
    print(f"""\nRunning simulation with parameters:
          agent_type={agent_type}, 
          num_agents={num_agents}, 
          start_positions={start_position}, 
          comm_range={comm_range}, 
          network_file={network_file},
          turn_limit={turn_limit}\n""")
    
    # Create the environment layer
    env = Network(network_file)
    # Create the simulation layer
    simulation = Simulation(env)
    # Create the agent layer
    agent_class = AGENT_CLASSES[agent_type]
    if not start_position:
        # Custom starting positions not implemented yet
        pass
    agent_positions = simulation.get_random_positions(num_agents)
    # Add agents to the simulation
    for i in range(num_agents):
        # convert i to hex
        i_hex = hex(i)
        if i == 0 and agent_type == "behavioural":
            agent = agent_class(env, str(i_hex), agent_positions[i], communication_range=comm_range, first=True)
            print(f"Agent {i} created at position {agent_positions[i]}, communication range {comm_range}, first=True")
        else:
            agent = agent_class(env, str(i_hex), agent_positions[i], communication_range=comm_range)
            print(f"Agent {i} created at position {agent_positions[i]}, communication range {comm_range}")
        simulation.add_agent(agent)
        
    # Run the simulation
    print("\nRunning simulation...")
    simulation.run(max_turns=turn_limit)
    
    # Save the results
    print("\nSaving results...")
    path = simulation.save_results()
    # Create animation
    render = Render(simulation)
    render.render()
    
    print(f"\nResults found at: {path}")
    
def gui():
    # Create the GUI - wip
    root = tk.Tk()
    root.title("Simulation Settings")
    
    # Create the widgets
    # Agent type - listbox with options random, greedy, behavioural
    label_agent_type = tk.Label(root, text="Agent Type")
    listbox_agent_type = tk.Listbox(root, selectmode="single")
    listbox_agent_type.insert(1, "random")
    listbox_agent_type.insert(2, "greedy")
    listbox_agent_type.insert(3, "behavioural")
    listbox_agent_type.select_set(0)
    entry_agent_type_i = listbox_agent_type.curselection()
    
    label_num_agents = tk.Label(root, text="Number of Agents")
    entry_num_agents = tk.Entry(root)
    
    args = (entry_agent_type_i, entry_num_agents)
    
    def submit(*args):
        for arg in args:
            print(arg.get())
        root.destroy()
    
    submit_button = tk.Button(root, text="Submit", command=lambda: submit(*args))
    
    label_agent_type.pack()
    listbox_agent_type.pack()
    
    label_num_agents.pack()
    entry_num_agents.pack()
    
    submit_button.pack()
    
    root.mainloop()
    
def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Network files", "*.inp")])
    return file_path
    
if __name__ == "__main__":
    os = platform.system()
    # not working
    # if os == "Windows":
    #     subprocess.run(["cmd.exe", "/K", "python -i"])
    # elif os == "Linux":
    #     subprocess.run(["gnome-terminal", "-x", "python -i"])
    # else:
    #     print("OS not supported")
    #     exit(1)
        
    agent_type = input("Enter agent type (random, greedy, behavioural): ") or "random"
    num_agents = int(input("Enter number of agents: ") or 4)
    start_positions = bool(input("Random starting positions? (True/False): ") or True)
    comm_range = int(input("Enter communication range: ") or -1)
    network_file = input("Enter path to network file (or press enter to select a file): ") or select_file()
    turn_limit = int(input("Enter maximum number of turns: ") or 100)
    
    create_simulation(agent_type, num_agents, start_positions, comm_range, network_file, turn_limit)
    