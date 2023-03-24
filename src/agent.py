"""
Agent module
============
Agent's operate in the network environment. The basic behaviour of the agent is to explore the network using the right hand wall rule
"""

import math
import statistics
from collections import Counter

import src.debug.logger as logger
from src.network import Network

class Agent:
    """
    Agent Class
    ===========
    
    Parameters
    ----------
    
    env : Network
        The network environment that the agent will operate in
    agent_id : int
        The id of the agent
    start_pos : int
        The starting position of the agent in the network environment
    threshold : str, optional (default=None)
        The threshold for the agent to use when allocating tasks in an informed manner
    
    """
    
    def __init__(self, env: Network, agent_id, start_pos, threshold=None) -> None:
        self._log = logger.get_logger(__name__)
        self.env = env
        self.G = env.water_network_model.to_graph().to_directed()
        
        self._agent_id = agent_id
        self._battery = 100
        self._current_node = start_pos
        self._previous_node = None
        self.link = None
        self._node_path = []
        self._link_path = []
        self._start_pos = start_pos
        
        self._agents_in_range = []
        self._task = None
        
        self._threshold = threshold
        
        self._log.debug(f"Agent {self._agent_id} created at node {self._current_node}")
    
    @property
    def agent_id(self):
        return self._agent_id
        
    @property
    def battery(self):
        return self._battery
        
    @property
    def position(self):
        return self._current_node
    
    @property
    def previous_node(self):
        return self._previous_node
    
    @property
    def node_path(self):
        return self._node_path
    
    @property
    def start_pos(self):
        return self._start_pos
    
    @property
    def agents_in_range(self):
        return self._agents_in_range
    
    @property
    def threshold(self):
        return self._threshold
    
    def __str__(self) -> str:
        return f"Agent {self._agent_id} at {self._current_node}"
    
    def __repr__(self) -> str:
        return f"Agent {self._agent_id} at {self._current_node}"
        
    def move(self):
        """
        Method for the agent to move in the environment
        
        Description
        ------------
        The agent moves from one node to another node in the environment.
        The agent's next node is determined by the link that it is currently traversing.
        """
        
        self._log.debug(f"{self} is moving along link {self.link}")
        
        self._previous_node = self._current_node
        self._node_path.append(self._current_node)
        self._link_path.append(self.link)
        self._current_node = self.env.get_node(self._previous_node, self.link)
        self._log.debug(f"Agent moved from node {self._previous_node} to node {self._current_node}")
        
    def decide(self, swarm:bool):
        """
        Method for the agent to decide what to do - based on task allocation
        
        Parameters
        ----------
        
        swarm : bool
            Boolean value to determine if the agent should follow the right hand traversal rule at each junction or instead
            use swarm behaviour where applicable.
        """
        
        if swarm:
            # If swarm behaviour is enabled, the agent will communicate with other agents in the same node
            if self.agents_in_range:
                self._log.debug(f"{self} has agents in range: {self.agents_in_range}")
                self._log.debug(f"{self} action determined by task allocation")
                self.link = self._task
                
            else:
                self._log.debug(f"{self} has no agents in range")
                self._log.debug(f"{self} action determined by right hand traversal rule")
                self.link = self.RH_Traversal()
        else:
            # If swarm behaviour is disabled, the agent will follow the right hand traversal rule
            self._log.debug(f"{self} action determined by right hand traversal rule")
            self.link = self.RH_Traversal()
        
    # def communicate(self):
    #     """
    #     Method for the agent to communicate with other agents
    #     """
    #     pass    
        
    def ping(self, agents):
        """
        Method for the agent to broadcast a ping to other agents in the same node
        
        Parameters
        ----------
        
        agents : list
            list of agents in the environment/simulation
            
        Description
        ------------
        
        Method to update the agents_in_range attribute - reflects how in the real world, at each junction in the pipe network,
        the agent would broadcast a ping to establish if there are any other agents in the same node.
        
        """
        
        # self._log.debug(f"{self} is pinging")
        
        self._agents_in_range = []
        # broadcast a ping to all agents in the same node and get the response if in range
        for agent in agents:
            # send ping
            if agent != self and agent.position == self._current_node:
                # get response
                self._agents_in_range.append(agent)
                
        # self._log.debug(f"{self} Pinged: {self._agents_in_range}")
        
    def RH_Traversal(self):
        """
        Method for the agent to follow the right hand wall rule - selects the next link to traverse
        """
        
        self._log.debug(f"{self} is following the right hand traversal rule")
        
        # Get the links for the current node - using the water network model
        # links = self.env.water_network_model.get_links_for_node(self._current_node)
        # Get the links for the current node - using the networkx graph adjacency list
        links = self.env.get_link_names(self._current_node)
        self._log.debug(f"Links for node {self._current_node}: {links}")
        # Get the degree of the current node
        degree = len(links)
        self._log.debug(f"Degree of node {self._current_node}: {degree}")
        # Get the index of the link that the agent came from
        try:
            self.env.get_link(self._previous_node, self._current_node)
            arrival_port = links.index(self.link)
            self._log.debug(f"Arrival port for node {self._current_node}: {arrival_port} ({links[arrival_port]})")
        except KeyError or ValueError:
            arrival_port = 0
            self._log.debug(f"(DEFAULT) Arrival port for node {self._current_node}: {arrival_port} ({links[arrival_port]})")   
          
        # Select the next link to follow - traverse the edge with port number (arrival_port + 1) % degree
        try:
            link = links[(arrival_port + 1) % degree]
        except ZeroDivisionError:
            raise ValueError(f"Node {self._current_node} has no links")
        self._task = link
        self._log.debug(f"Next link to traverse: {link}")
        
        return link
    
    def assign_tasks(self, agents, ports):
        """
        Method for the agent to assign tasks to other agents in the communication cluster
        
        Parameters
        ----------
        
        agent : Agent
            The agent to assign the task
        ports : list
            List of ports available for task assignment
        """
        
        self._log.debug(f"{self} is assigning tasks")
        
        # Get each agent's arrival port
        arrival_ports = self._get_arrival_ports(agents)
        # Get the number of ports available for task assignment
        num_ports = len(ports)
        self._log.debug(f"Ports: {ports}")
        self._log.debug(f"Number of ports: {num_ports}")
        self._log.debug(f'Arrival ports: {arrival_ports}')
        self._log.debug(f"Number of ports available for assignment: {num_ports - len(set(arrival_ports.values())) if num_ports > len(set(arrival_ports.values())) else 0}")
        # If number of ports is zero - raise unconnected junction error
        if num_ports == 0:
            raise ValueError(f"Junction {self._current_node} is unconnected")
        # If there is only one port, the junction is a dead-end: all agents are assigned the same port
        elif num_ports == 1:
            for agent in agents:
                self._log.debug(f"Assigning port {ports[0]} to agent {agent.agent_id}")
                self._agent_task_allocation(agent, ports[0])
        else:
            # Determine each agent's next port according to the right hand traversal rule
            next_ports = {}
            for agent in agents:
                i_next = self._RH_Traversal(arrival_ports[agent], len(ports))
                self._log.debug(f"Agent {agent.agent_id} RH-Traversal port: {i_next} ({ports[i_next]})")
                next_ports.update({agent: ports[i_next]})
            self._log.debug(f'All ports: {ports}')
            self._log.debug(f"Next ports: {next_ports}")

            # Distribute agents across ports
            # If number of ports available for assignment is less than the number of agents, assign agents to ports in a round-robin fashion
            if num_ports - len(set(arrival_ports.values())) < len(agents):
                self._log.debug("Number of assignable ports is less than number of agents")             
                for i, agent in enumerate(agents):
                    self._log.debug(f"Assigning port {ports[i % num_ports]} to agent {agent.agent_id}")
                    self._agent_task_allocation(agent, ports[i % num_ports])
            else:
                # If number of ports available for assignment is greater than the number of agents, assign agents to ports in a round-robin fashion
                self._log.debug("Number of assignable ports is greater than number of agents")
                for i, agent in enumerate(agents):
                    self._log.debug(f"Assigning port {ports[i % num_ports]} to agent {agent.agent_id}")
                    self._agent_task_allocation(agent, ports[i % num_ports])
                # If number of ports available for assignment is equal to the number of agents, assign agents to ports in a round-robin fashion
                self._log.debug("Number of assignable ports is equal to number of agents")
                for i, agent in enumerate(agents):
                    self._log.debug(f"Assigning port {ports[i % num_ports]} to agent {agent.agent_id}")
                    self._agent_task_allocation(agent, ports[i % num_ports])

    def assign_tasks_informed(self, agents, ports):
        """
        Method for the agent to assign tasks to other agents in the communication cluster. This is the informed version of the assign_tasks method. The score is
        determined by the number of agents that have arrived through a port.
        
        Parameters
        ----------
        
        agents : Agent
            The agents to assign tasks to
        ports : list
            List of ports available for task assignment
        
        """
        
        self._log.debug(f"{self} is assigning tasks using informed - {self._threshold} - task assignment")
        
        # Get each agent's arrival port
        arrival_ports = self._get_arrival_ports(agents)
        self._log.debug(f'Arrival ports: {arrival_ports}')
        # Convert arrival ports (index) to port (link) objects
        arrival_ports = {agent: ports[arrival_ports[agent]] for agent in agents}
        self._log.debug(f'Arrival ports (as links): {arrival_ports}')
        # Get the links at the current node
        links = self.env.get_links(self._current_node)
        self._log.debug(f"Links at node {self._current_node}: {links}")
        # Check that links is equal to the number of ports
        if len(links) != len(ports):
            raise ValueError(f"Number of links at node {self._current_node} does not match number of ports")

        # initialise the port score dictionary
        port_scores = {}
        for port in ports:
            # if port is an arrival port, the score is the number of agents that have arrived through that port
            if port in arrival_ports.values():
                port_scores.update({port: len([agent for agent in agents if arrival_ports[agent] == port])})
            else:
                port_scores.update({port: 0})
                
        self._log.debug(f"Port scores: {port_scores}")

        sorted_port_scores = sorted(port_scores.items(), key=lambda x: x[1])
        for port, score in sorted_port_scores:
            self._log.debug(f"Port {port} has score {score}")
            
        total_port_score = sum(port_scores.values())
        
        mean_port_score = total_port_score / len(ports)
        median_port_score = sorted_port_scores[math.floor(len(ports) / 2)][1]
        
        self._log.debug(f"Mean port score: {mean_port_score}")
        self._log.debug(f"Median port score: {median_port_score}")
        
        if self._threshold == 'mean':
            assignment = self._mean_allocation(agents, mean_port_score, port_scores)
        elif self._threshold == 'median':
            assignment = self._median_allocation(agents, median_port_score, port_scores)
        else:
            raise ValueError(f"Threshold {self._threshold} is not a valid threshold for informed task assignment")
        
        # Assign agents to ports
        for agent, port in assignment.items():
            self._agent_task_allocation(agent, port)

    def _get_arrival_ports(self, agents) -> dict:
        arrival_ports = {}
        # links = self.env.water_network_model.get_links_for_node(self._current_node)
        links = self.env.get_link_names(self._current_node)
        
        for agent in agents:
            self._log.debug(f"Getting arrival port for {agent}")
            try:
                link_name = self.env.get_link(agent.previous_node, agent.position)['link_name']
                arrival_port = links.index(link_name)
                self._log.debug(f"Arrival port for agent {agent.agent_id}: {arrival_port} ({links[arrival_port]})")
            except KeyError or ValueError:
                arrival_port = 0
                self._log.debug(f"(DEFAULT) Arrival port for agent {agent.agent_id}: {arrival_port} ({links[arrival_port]})")
            arrival_ports.update({agent: arrival_port})
            
        return arrival_ports

    def _RH_Traversal(self, arrival_port: int, degree: int) -> int:
        # Select the next link to follow - traverse the edge with port number (arrival_port + 1) % degree
        next = (arrival_port + 1) % degree
        return next
            
    def _agent_task_allocation(self, agent, port):
        """
        Method to assign a task to a single agent in the communication cluster
        """
        agent.receive_task(port)
        
    def receive_task(self, link):
        """
        Method for the agent to receive a task
        """
        self._log.debug(f"{self} received task {link}")
        self._task = link
            
    def _mean_allocation(self, agents, mean_port_score, port_scores):
        assignments = {agent: None for agent in agents}
        
        # If the port score is less than the mean port score, the port is considered to be underutilised
        underutilised_ports = [port for port, score in port_scores.items() if score < mean_port_score]
        self._log.debug(f"(MEAN) Underutilised ports: {underutilised_ports}")
        
        # If the port score is greater than the mean port score, the port is considered to be overutilised
        overutilised_ports = [port for port, score in port_scores.items() if score > mean_port_score]
        self._log.debug(f"(MEAN) Overutilised ports: {overutilised_ports}")
        
        # If the port score is equal to the mean port score, the port is considered to be balanced
        balanced_ports = [port for port, score in port_scores.items() if score == mean_port_score]
        self._log.debug(f"(MEAN) Balanced ports: {balanced_ports}")
        
        # Priority 1: Assign agents to underutilised ports
        if len(underutilised_ports) > 0:
            self._log.debug("(MEAN) Assigning agents to underutilised ports")
            for port in underutilised_ports:
                if len(agents) > 0:
                    agent = agents.pop(0)
                    assignments.update({agent: port})
                    self._log.debug(f"(MEAN) Assigning agent {agent.agent_id} to port {port}")
                else:
                    self._log.debug("(MEAN) No agents to assign")
                    
        # Priority 2: Assign agents to balanced ports
        if len(balanced_ports) > 0:
            self._log.debug("(MEAN) Assigning agents to balanced ports")
            for port in balanced_ports:
                if len(agents) > 0:
                    agent = agents.pop(0)
                    assignments.update({agent: port})
                    self._log.debug(f"(MEAN) Assigning agent {agent.agent_id} to port {port}")
                else:
                    self._log.debug("(MEAN) No agents to assign")
                    
        # Priority 3: Assign agents to overutilised ports
        if len(overutilised_ports) > 0:
            self._log.debug("(MEAN) Assigning agents to overutilised ports")
            for port in overutilised_ports:
                if len(agents) > 0:
                    agent = agents.pop(0)
                    assignments.update({agent: port})
                    self._log.debug(f"(MEAN) Assigning agent {agent.agent_id} to port {port}")
                else:
                    self._log.debug("(MEAN) No agents to assign")
                    
        # Priority 4: Assign remaining agents to ports with the lowest score
        if len(agents) > 0:
            self._log.debug("(MEAN) Assigning remaining agents to ports with lowest score")
            for agent in agents:
                port = sorted(port_scores.items(), key=lambda x: x[1])[0][0]
                assignments.update({agent: port})
                self._log.debug(f"(MEAN) Assigning agent {agent.agent_id} to port {port}")
                
        return assignments
    
    def _median_allocation(self, agents, median_port_score, port_scores):
        
        assignments = {agent: None for agent in agents}
        
        # If the port score is less than the median port score, the port is considered to be underutilised
        underutilised_ports = [port for port, score in port_scores.items() if score < median_port_score]
        self._log.debug(f"(MEDIAN) Underutilised ports: {underutilised_ports}")
        
        # If the port score is greater than the median port score, the port is considered to be overutilised
        overutilised_ports = [port for port, score in port_scores.items() if score > median_port_score]
        self._log.debug(f"(MEDIAN) Overutilised ports: {overutilised_ports}")
        
        # If the port score is equal to the median port score, the port is considered to be balanced
        balanced_ports = [port for port, score in port_scores.items() if score == median_port_score]
        self._log.debug(f"(MEDIAN) Balanced ports: {balanced_ports}")
        
        # Priority 1: Assign agents to underutilised ports
        if len(underutilised_ports) > 0:
            self._log.debug("(MEDIAN) Assigning agents to underutilised ports")
            for port in underutilised_ports:
                if len(agents) > 0:
                    agent = agents.pop(0)
                    assignments.update({agent: port})
                    self._log.debug(f"(MEDIAN) Assigning agent {agent.agent_id} to port {port}")
                else:
                    self._log.debug("(MEDIAN) No agents to assign")
                    
        # Priority 2: Assign agents to balanced ports
        if len(balanced_ports) > 0:
            self._log.debug("(MEDIAN) Assigning agents to balanced ports")
            for port in balanced_ports:
                if len(agents) > 0:
                    agent = agents.pop(0)
                    assignments.update({agent: port})
                    self._log.debug(f"(MEDIAN) Assigning agent {agent.agent_id} to port {port}")
                else:
                    self._log.debug("(MEDIAN) No agents to assign")
                    
        # Priority 3: Assign agents to overutilised ports
        if len(overutilised_ports) > 0:
            self._log.debug("(MEDIAN) Assigning agents to overutilised ports")
            for port in overutilised_ports:
                if len(agents) > 0:
                    agent = agents.pop(0)
                    assignments.update({agent: port})
                    self._log.debug(f"(MEDIAN) Assigning agent {agent.agent_id} to port {port}")
                else:
                    self._log.debug("(MEDIAN) No agents to assign")
                    
        # Priority 4: Assign remaining agents to ports with the lowest score
        if len(agents) > 0:
            self._log.debug("(MEDIAN) Assigning remaining agents to ports with lowest score")
            for agent in agents:
                port = sorted(port_scores.items(), key=lambda x: x[1])[0][0]
                assignments.update({agent: port})
                self._log.debug(f"(MEDIAN) Assigning agent {agent.agent_id} to port {port}")
                
        return assignments