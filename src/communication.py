"""
Module for enabling communication between agents in communication clusters
"""

from typing import List
from copy import copy

import src.debug.logger as logger
from src.agent import Agent
from src.network import Network

log = logger.get_logger(__name__)

def communicate(agents: List[Agent], network: Network, informed: bool=False):
    """
    Method for enabling communication between agents in communication clusters and allocating tasks
    
    Parameters
    -----------
    
    agents: List[Agent]
        List of agents in the communication cluster
    network: Network
        Network object (the environment)
    informed: bool, optional (default=False)
        Whether the agents are using informed task allocation or not
    
    """
    
    log.debug(f"Communication between {len(agents)} agents @ {agents[0].position}")
    
    ports = synchronise_port_labelling(agents, network)
    log.info(f'Port labels: {ports}')
    
    leader = establish_leader(agents)
    log.info(f'Leader: {leader}')

    allocate_tasks(agents, leader, ports, informed)
        

def synchronise_port_labelling(agents: List[Agent], network: Network):
    """
    Method for agents to synchronise port labelling
    
    Parameters
    ----------
    
    agents: List[Agent]
        List of agents in the communication cluster
    network: Network
        Network object (the environment)
    
    Description
    -----------
    
    In the real world, agents would have to synchronise their port labelling using some method,
    one such example might be using the bearing of each link relative to north to determine the labelling. Port labels could be
    labelled based on the bearing of the link relative to north, with the link with the smallest bearing being labelled 1, the
    second smallest being labelled 2, and so on. This would ensure that the port labelling is consistent across agents.
    
    True North is a common factor to all agents and so can be used to synchronise port labelling across agents in the network.
    
    """
    
    # Get the current node
    node = agents[0].position
    # Get the links for the current node
    # labels = network.water_network_model.get_links_for_node(node)
    labels = network.get_link_names(node)
    # Get the bearings for the links
    # bearings = network.water_network_model.get_bearings_for_node(node) - not an actual function as no concept of north currently exists
    # Sort the bearings
    # bearings.sort()
    return labels
    
def establish_leader(agents: List[Agent]):
    """
    Method to establish a leader agent for the communication cluster
    
    Parameters
    ----------
    
    agents: List[Agent]
        List of agents in the communication cluster
    
    Description
    -----------
    
    Given that each agent has a unique ID, the agent with the lowest ID can be selected as the leader.
    This requires that the agents are all in agreement regarding which agent has the lowest ID.
    
    - Begin pairwise comparison of agent IDs
    - The agent with the lowest ID will be selected as the leader of that pair of agents and the process will continue 
    until only one agent remains, this agent will be the leader of the communication cluster
    - This is a recursive function - in practice this would be done in parallel across all agents in the cluster though this simulation, agents would
    arbitrarily select another of agent to compare their ID with
    
    """
    
    # create a copy of the list of agents
    working_agents = copy(agents)
    
    if len(working_agents) == 1:
        # If there is only one agent left, it is the leader
        log.debug(f'Leader: {working_agents[0]}')
        leader = working_agents[0]
        del working_agents
        return leader
    # If there are more than one agent left, compare the first two agents
    elif working_agents[0].agent_id < working_agents[1].agent_id:
        # If the first agent has a lower ID than the second agent, remove the second agent from the list
        # log.debug(f'{agents[0]} has a lower ID than {agents[1]}')
        working_agents.pop(1)
        # Recursively call the function with the new list of agents
        return establish_leader(working_agents)

def allocate_tasks(agents, leader, ports, informed: bool = False):
    """
    Method to allocate tasks to agents in the communication cluster
    
    Parameters
    ----------
    
    agents: List[Agent]
        List of agents in the communication cluster
    leader: Agent
        Leader agent of the communication cluster
    ports: list
        List of port labels for the current node
    informed: bool, optional (default=False)
        Whether the agents are using informed task allocation or not
    
    """
    
    working_agents = copy(agents)
    working_ports = copy(ports)
        
    log.debug(f'Allocating tasks to {len(working_agents)} agents')
    
    # remove the leader from the list of agents
    # working_agents.remove(leader)
    
    # cast leader to an agent object
    try:
        lead_agent: Agent = leader
    except TypeError:
        log.error(f'Leader is not an Agent type')
        raise TypeError
    
    log.debug(f'Leader: {lead_agent}')
    log.debug(f'Agents: {working_agents}')
    
    if not informed:
        lead_agent.assign_tasks(agents=working_agents, ports=working_ports)
    else:
        lead_agent.assign_tasks_informed(agents=working_agents, ports=working_ports)

        
