"""
Agent module
============
Agent's operate in the network environment. The basic behaviour of the agent is to explore the network using the right hand wall rule
"""
from collections import Counter

import src.debug.logger as logger
from src.network import Network

class Agent:
    
    def __init__(self, env: Network, agent_id, start_pos) -> None:
        self._log = logger.get_logger(__name__)
        self.env = env
        self.G = env.water_network_model.to_graph().to_directed()
        
        self._agent_id = agent_id
        self._battery = 100
        self._current_node = start_pos
        self._previous_node = None
        self.link = None
        self._path = []
        self._start_pos = start_pos
        
        self._agents_in_range = []
        self._task = None
        
        self._log.debug(f"Agent {self._agent_id} created")
    
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
    def path(self):
        return self._path
    
    @property
    def start_pos(self):
        return self._start_pos
    
    @property
    def agents_in_range(self):
        return self._agents_in_range
    
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
        self._path.append(self._current_node)
        self._current_node = self.env.get_node(self._previous_node, self.link)
        self._log.debug(f"Agent moved from node {self._previous_node} to node {self._current_node}")
        
    def decide(self, swarm:bool):
        """
        Method for the agent to decide what to do - based on task allocation
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
        - param: list of agents in the environment/simulation
        - update: the agents_in_range attribute
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
            self._log.debug(f"Arrival port for node {self._current_node}: {arrival_port}")
        except KeyError or ValueError:
            arrival_port = 0
            self._log.warning(f"Arrival port for node {self._current_node}: {arrival_port}")   
          
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
            raise ValueError("Junction is unconnected")
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

    def _get_arrival_ports(self, agents) -> dict:
        arrival_ports = {}
        links = self.env.water_network_model.get_links_for_node(self._current_node)
        
        for agent in agents:
            self._log.debug(f"Getting arrival port for {agent}")
            try:
                link_name = self.env.get_link(agent.previous_node, agent.position)['link_name']
                arrival_port = links.index(link_name)
                self._log.debug(f"Arrival port for agent {agent.agent_id}: {arrival_port}")
            except KeyError or ValueError:
                arrival_port = 0
                self._log.warning(f"Arrival port for agent {agent.agent_id}: {arrival_port}")
            arrival_ports.update({agent: arrival_port})
            
        return arrival_ports

    def r_assign_tasks(self, agents, ports):
        """
        Method for the agent to assign tasks to other agents in the communication cluster
        
        Parameters
        ----------
        agent : Agent
            The agent to assign the task
        ports : list
            List of ports available for task assignment
        """
        
        self._log.debug(f"Assigning tasks to agents in the communication cluster")
        self._log.debug(f"Ports available for task assignment: {ports}")
        self._log.debug(f"Agents in the communication cluster: {agents}")
        
        arrival_ports = {}
        allocated_ports = {}
        
        # Check if the number of ports is greater than one
        if len(ports) < 2:
            if len(ports) == 0:
                self._log.warning("No ports available for task assignment")
            # All agents in the cluster are assigned to the same port
            self._log.debug(f"Only one port available: {ports[0]}")
            for agent in agents:
                self._agent_task_allocation(agent, ports[0])
            return
        
        # Get the agent's arrival port
        else:
            for agent in agents:
                self._log.debug(f"Getting arrival port for {agent}")
                try:
                    arrival_port = self.env.get_link(agent.previous_node, agent.position)
                    self._log.debug(f"Arrival port for agent {agent.agent_id}: {arrival_port}")
                except KeyError or ValueError:
                    arrival_port = 0
                    self._log.warning(f"Arrival port for agent {agent.agent_id}: {arrival_port}")
            
                # Add the arrival port to the list of arrival ports
                arrival_ports.update({agent: arrival_port})
                self._log.debug(f"Arrival ports: {arrival_ports}")
                # Get the label of the arrival port
                arrival_port_label = ports[arrival_port]
                self._log.debug(f"Arrival port label: {arrival_port_label}")
                
        # Get the number of agents in the cluster
        num_agents = len(agents)
        # Get the number of ports available for task assignment
        num_ports = len(ports)
        # Get the number of ports that are not occupied
        num_free_ports = num_ports - len(arrival_ports)
        
        # get each agents next link to traverse based on the right hand traversal rule
        for agent in agents:
            # Get the agent's arrival port
            arrival_port = arrival_ports.get(agent, 0)
            # Get the agent's next link to traverse
            next = self._RH_Traversal(arrival_port=arrival_port, degree=num_ports)
            self._log.debug(f"Next link to traverse for agent {agent.agent_id}: {next}")
            # Get the label of the next link to traverse
            next_label = ports[next]
            self._log.debug(f"Next link label for agent {agent.agent_id}: {next_label}")
            # Add to the dict of allocated ports
            allocated_ports.update({agent: next_label})
            
        self._log.debug(f"Allocated ports: {allocated_ports}")
        
        # Check if any of the ports are conflicted
        if len(allocated_ports) != len(set(allocated_ports.values())):
            # Get the ports that are conflicted
            conflicted_ports = [port for port, count in Counter(allocated_ports.values()).items() if count > 1]
            self._log.debug(f"Conflicted ports: {conflicted_ports}")
            # Get the agents that are assigned to the conflicted ports
            conflicted_agents = [agent for agent, port in allocated_ports.items() if port in conflicted_ports]
            # If there are any free ports, assign the conflicted agents to the free ports
            if num_free_ports > 0:
                # Get the free ports
                free_ports = [port for port in ports if port not in arrival_ports.values()]
                self._log.debug(f"Free ports: {free_ports}")
                # Assign the conflicted agents to the free ports
                for agent in conflicted_agents:
                    pass
            
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
            
        
        