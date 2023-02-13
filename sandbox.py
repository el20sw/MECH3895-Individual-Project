# import logger
import logging
import src.debug.logger as logger

from src.simulation import Simulation
from src.network import Network
from src.agents.random_agent import RandomAgent
from src.agents.greedy_agent import GreedyAgent
from src.agents.behavioural_agent import BehaviouralAgent

from src.render import Render

logging.disable(logging.CRITICAL)

### Main Function ###
def main():
    ### Initialise the logger
    log = logger.setup_logger(file_name='logs/sandbox.log', level='DEBUG')
    # Initialise the simulation
    log.info('Initialising the simulation')
    # Create the environment layer
    env = Network('networks/Net2.inp')
    log.debug(f'Environment: {env}')
    # Create the agent layer
    agentA = BehaviouralAgent(env, 'A', '11', communication_range=-1, random_seed=0, first=True)
    agentB = BehaviouralAgent(env, 'B', '12', communication_range=-1, random_seed=0)
    agentC = BehaviouralAgent(env, 'C', '23', communication_range=-1, random_seed=0)
    log.debug(f'{agentA} @ {agentA.position}')
    # log.debug(f'{agentB} @ {agentB.position}')
    # Create the simulation layer
    agent_list = [agentA, agentB, agentC]
    simulation = Simulation(env)
    log.debug(f'Simulation: {simulation}')
    # Add agents to the simulation
    log.debug(f'Simulation Agents: {simulation.agents}')
    log.debug(f'Overwatch Agents: {simulation.overwatch.agents}')
    log.debug(f'Overwatch Agent Numbers: {simulation.overwatch.num_agents}')
    log.debug(f'Overwatch Agent Positions: {simulation.overwatch.agent_positions}')
    log.debug(f'Overwatch Comms Buffer: {simulation.overwatch.communication_buffer}')

    simulation.add_agent(agentA)
    simulation.add_agent(agentB)
    simulation.add_agent(agentC)

    log.debug(f'Simulation Agents: {simulation.agents}')
    log.debug(f'Overwatch Agents: {simulation.overwatch.agents}')
    log.debug(f'Overwatch Agent Numbers: {simulation.overwatch.num_agents}')
    log.debug(f'Overwatch Agent Positions: {simulation.overwatch.agent_positions}')
    log.debug(f'Overwatch Comms Buffer: {simulation.overwatch.communication_buffer}')

    # Run the simulation
    log.info('Running the simulation')
    simulation.run(max_turns=100)

    # Get the results
    # simulation._write_results('results/sandbox.json')
    simulation.save_results()

    # Render the network
    # env.plot_network(show=False, node_labels=True, link_labels=True)
    
    render = Render(simulation)
    render.render()

# call main function
if __name__ == '__main__':
    main()
    
