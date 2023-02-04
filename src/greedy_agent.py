# Import modules
from copy import deepcopy
import src.debug.logger as logger

from typing import List
import random

# Import classes
from src.agent import Agent
from src.belief import Belief
from src.observation import Observation
from src.transmittable import Transmittable
from src.network import Network
from src.overwatch import Overwatch

### Greedy Agent Class ###
class GreedyAgent(Agent):
    # Initialise the agent
    def __init__(self, environment: Network, id, position, communication_range: int =-1, random_seed: int = 0):
        """
        Constructor for the GreedyAgent class
        :param environment: Enviroment the agent is operating in (Network)
        :param id: ID of the agent
        :param position: Position of the agent in the environment
        :param communication_range: Range of communication of the agent - default is -1 (infinite communication)
        """
    
        # Initialise the logger
        self._log = logger.get_logger(__name__)

        # Set the random seed
        random.seed(random_seed)
        self._log.debug(f"Agent {id} is using random seed {random_seed}")

        # Initialise the agent
        self._id = id
        self._position = position
        self._previous_position = None
        self._communication_range = communication_range
        self._visited_nodes = []

        # check if the position is in the network environment
        if self._position not in environment.node_names:
            raise ValueError(f'Position {self._position} is not in the network environment')

        # Check if the position is in the adjacency list
        if self._position not in environment.adj_list.keys():
            raise KeyError(f'Position {self._position} is not in adjacency list')

        # Create the agent's belief - takes the environment, the agent's id and the agent's position
        self._belief = Belief(environment, self._id, self._position)

    @property
    def id(self):
        """
        Getter for the agent's id
        :return: Agent's id
        """
        return self._id

    @property
    def position(self):
        """
        Getter for the agent's position
        :return: Agent's position
        """
        return self._position

    @property
    def previous_position(self):
        """
        Getter for the agent's previous position
        :return: Agent's previous position
        """
        return self._previous_position

    @property
    def communication_range(self):
        """
        Getter for the agent's communication range
        :return: Agent's communication range
        """
        return self._communication_range

    @property
    def belief(self):
        """
        Getter for the agent's belief
        :return: Agent's belief
        """
        return self._belief

    @property
    def observation(self):
        """
        Getter for the agent's observation
        :return: Agent's observation
        """
        return self._observation

    async def step(self, environment, overwatch):
        pass

    def move(self) -> None:
        """
        Method to move the agent in the environment
        :param action: Action to take - the new position of the agent
        :return: None
        """
        # update the previous position
        self._previous_position = self._position
        # update the agent's position
        self._position = self._action
        # log the agent's position
        self._log.debug(f'{self._id} moved to {self._position}')

    def observe(self, environment):
        """
        Method to observe the environment
        :param environment: Environment in which the agent is observing - the pipe network
        :return: Observation of the agent
        """
        
        # create an observation object
        observation = Observation(environment, self._position)
        # log the observation
        self._log.debug(f"Agent {self._id} is observing {observation}")
        # update the belief of the agent with the observation
        self._belief.update(observation)
        # update the visited nodes
        self._visited_nodes.append(self._position)

        self._observation =  observation

    def communicate(self, overwatch):
        """
        Method to communicate with other agents in the environment
        :param environment: Environment in which the agent is communicating - the pipe network
        :return: None
        """
        
        # query the overwatch for the agents in the agent's communication range
        agents_in_range = overwatch.get_agents_in_range(self._position, self._communication_range)
        # remove the agent's own id from the list of agents in range
        agents_in_range = [agent for agent in agents_in_range if agent.id != self._id]
        # log the agents in range
        self._log.debug(f"Agent {self._id} is communicating with {agents_in_range}")

        # if there are agents in range
        if agents_in_range:
            # create transmittable object with the agent's belief
            transmittable = Transmittable(self._belief)
            # log the transmittable
            self._log.debug(f"Agent {self._id} is transmitting {transmittable}")
            # send the transmittable to the agents in range - this is handled by the overwatch
            self._tx(self._id, transmittable, agents_in_range, overwatch)
            # request the transmittables from the agents in range - this is handled by the overwatch
            transmittables = self._rx(self._id, overwatch)
            # log the transmittables
            self._log.debug(f"Agent {self._id} is receiving {transmittables}")
            # update the agent's belief with the transmittables
            self._belief.update(*transmittables)

    def commsPart1(self, overwatch):
        """
        Method to send a communication to other agents in the environment
        :param overwatch: overwatcher facilitating communication
        :return: None
        """

        # query the overwatch for the agents in the agent's communication range
        agents_in_range = overwatch.get_agents_in_range(self._position, self._communication_range)
        # remove the agent's own id from the list of agents in range
        agents_in_range = [agent for agent in agents_in_range if agent.id != self._id]
        # log the agents in range
        self._log.debug(f"Agent {self._id} is communicating with {agents_in_range}")

        # if there are agents in range
        if agents_in_range:
            # create transmittable object with the agent's belief
            transmittable = Transmittable(self._belief)
            # log the transmittable
            self._log.debug(f"Agent {self._id} is transmitting {transmittable}")
            # send the transmittable to the agents in range - this is handled by the overwatch
            self._tx(self._id, transmittable, agents_in_range, overwatch)

    def commsPart2(self, overwatch):
        """
        Method to recieve communication from other agents in the environment
        :param overwatch: overwatcher facilitating communication
        :return: None
        """

        # request the transmittables from the agents in range - this is handled by the overwatch
        transmittables = self._rx(self._id, overwatch)
        # log the transmittables
        self._log.debug(f"Agent {self._id} is receiving {transmittables}")
        # update the agent's belief with the transmittables
        self.update_belief(*transmittables)
        # log the agent's belief
        self._log.debug(f'Agent {self._id} belief: {self._belief.nodes}')

    def send_communication(self, overwatch):
        """
        Method to send communication to the overwatch
        :param overwatch: Overwatcher
        :return: None
        """

        # query the overwatch for the agents in the agent's communication range
        self._agents_in_range = overwatch.get_agents_in_range(self._position, self._communication_range)
        # remove the agent's own id from the list of agents in range
        self._agents_in_range = [agent for agent in self._agents_in_range if agent.id != self._id]
        # log the agents in range
        self._log.debug(f"Agent {self._id} is communicating with {self._agents_in_range}")

        # if there are agents in range
        if self._agents_in_range:
            # create transmittable object with the agent's belief
            self._transmittable = Transmittable(self._belief)
            # log the transmittable
            self._log.debug(f"Agent {self._id} is transmitting {self._transmittable}")
            # send the transmittable to the agents in range - this is handled by the overwatch
            self._tx(self._id, self._transmittable, self._agents_in_range, overwatch)

    def receive_communication(self, overwatch) -> List[Transmittable]:
        """
        Method to receive communication from the overwatch
        :param overwatch: Overwatcher
        :return: Transmittables received
        """

        # request the transmittables from the agents in range - this is handled by the overwatch
        self._transmittables = self._rx(self._id, overwatch)
        # log the transmittables
        self._log.debug(f"Agent {self._id} is receiving {self._transmittables}")

        return self._transmittables

    def update_belief(self, *transmittables: Transmittable):
        """
        Method to update the agent's belief with the transmittables
        :param transmittables: Transmittables to update the belief with
        :return: None
        """

        # update the agent's belief with the transmittables
        self._belief.update(*transmittables)

    def _tx(self, id, transmittable, agents_in_range, overwatch: Overwatch):
        """
        Method to transmit a transmittable to the agents in range
        :param id: Id of the agent
        :param transmittable: Transmittable to transmit
        :param agents_in_range: Agents in range to transmit to
        :param overwatch: Overwatcher
        :return: None
        """

        # call the overwatch receive method
        overwatch.upload(id, transmittable, agents_in_range)

    def _rx(self, id, overwatch: Overwatch) -> List[Transmittable]:
        """
        Method to receive transmittables from the overwatch
        :param id: Id of the agent
        :param overwatch: Overwatcher
        :return: Transmittables received
        """
            
        # call the overwatch send method
        return overwatch.download(id)

    def action(self):
        """
        Method to get the action of the agent - update the action space
        :return: None
        """

        self._log.info(f"Agent {self._id} @ {self._position} is deciding on an action")

        # Get the action space - this is the list of possible actions (i.e. the nodes adjacent to the agent's current position)
        action_space = self._observation.state['neighbours']
        # log the action space
        self._log.debug(f"Agent {self._id} @ {self._position} action space: {action_space}")

        # get a random action from the action space
        action = self._greedy_action(action_space)

        self._action = action

    def _greedy_action(self, action_space):
        """
        Method to get a greedy action from the action space
        :param action_space: Action space
        :return: Greedy action
        """

        # get agent's position
        position = self._position

        # unvisited nodes
        unvisited_nodes = [node for node in self._belief.nodes if self._belief.nodes.get(node) == 1]
        # unvisited nodes in action space
        unvisited_nodes_action_space = []
        # check if any nodes in the action space are unvisited
        for neighbour in action_space:
            if neighbour in unvisited_nodes:
                unvisited_nodes_action_space.append(neighbour)

        if unvisited_nodes_action_space:
            action = random.choice(unvisited_nodes_action_space)
            self._log.info(f"Agent {self._id} is taking a random action {action} from the action space (unvisited nodes in action space)")
            return action

        # get the agent's adjacency list
        adjacency_list = self._build_agent_adjacency_list(action_space=action_space)
        # get the agent's node distances and the previous nodes to get there
        distances, previous_nodes = self._dijkstra(position, adjacency_list)
        # get the agent's nearest unvisited node
        try:
            nearest_unvisited_node = self._get_nearest_unvisited_node(distances, adjacency_list)
            # get the action to take to get to the nearest unvisited node
            action = self._get_action_closer_to_node(action_space, nearest_unvisited_node, previous_nodes)
            # log the action
            self._log.warning(f"Agent {self._id} is taking greedy action {action}")
        except Exception:
            # if there are no unvisited nodes, return a random action fronm the action space
            action = random.choice(action_space)
            # log the action
            self._log.info(f"Agent {self._id} is taking random action {action}")

        return action

    # NOTE: This does not include link lengths in the returned adjacency list
    def _build_agent_adjacency_list(self, action_space=None):
        """
        Method to build the adjacency list of the agent given the belief of the agent
        :return: Adjacency list of the agent (note: this does not include link lengths)
        """

        # get the links known to the agent
        links = self._belief.links
        # get the nodes known to the agent
        nodes = self._belief.nodes

        # create an adjacency dictionary
        adjacency_list = {}
        # for each link
        for link in links:
            # get the nodes of the link and the information of the link
            node_1, node_2, information = link
            # check if node 1 is in the adjacency list
            if node_1 not in adjacency_list:
                # if not, add it
                adjacency_list[node_1] = []
            # check if node 2 is in the adjacency list
            if node_2 not in adjacency_list:
                # if not, add it
                adjacency_list[node_2] = []
            # check if node 2 is in the adjacency list of node 1
            if node_2 not in adjacency_list[node_1]:
                # if not, add it
                adjacency_list[node_1].append(node_2)
            # check if node 1 is in the adjacency list of node 2
            if node_1 not in adjacency_list[node_2]:
                # if not, add it
                adjacency_list[node_2].append(node_1)

        # if the action space is not None
        if action_space:
            # add the action space to the adjacency list
            adjacency_list[self._position] = action_space

        return adjacency_list

    def _get_nearest_unvisited_node(self, degrees_of_seperation, adjacency_list):
        """
        Method to get the nearest unvisited node
        :param adjacency_list: Adjacency list of the agent
        :param degrees_of_seperation: Degrees of seperation from the agent's current position to the nodes in the adjacency list
        :return: Nearest unvisited node
        """

        # Get the nodes known to the agent
        nodes = self._belief.nodes
        # Get the visited nodes known by the agent
        visited_nodes = [i for i in nodes if nodes.get(i) == 0]
        # Get the unvisited nodes known by the agent
        unvisited_nodes = [i for i in nodes if nodes.get(i) == 1]
        # Get the occupied nodes known by the agent
        occupied_nodes = [i for i in nodes if nodes.get(i) == -10]

        # Get the nodes in the adjacency list
        adjacency_list_nodes = list(adjacency_list.keys())
        # Get the unvisited nodes in the adjacency list - this is the list of nodes that the agent can move to
        unvisited_nodes_in_adjacency_list = [i for i in adjacency_list_nodes if i in unvisited_nodes]
        # Get the occupied nodes in the adjacency list
        occupied_nodes_in_adjacency_list = [i for i in adjacency_list_nodes if i in occupied_nodes]

        # Check if there are unvisited nodes in the adjacency list
        if len(unvisited_nodes_in_adjacency_list) > 0:
            # If so, iterate through the degrees of seperation and find the nearest unvisited node
            for node in degrees_of_seperation:
                # check if the node is in the unvisited nodes in the adjacency list
                if node in unvisited_nodes_in_adjacency_list:
                    # if so, set the nearest unvisited node to this node
                    self._log.debug(f"Agent {self._id} has nearest unvisited node: {node}")
                    return node
        else:
            return Exception

    def _get_action_closer_to_node(self, action_space, dest_node, previous):
        """
        Method to get the action that gets the agent closer to a node
        :param action_space: Action space
        :param dest_node: Destination node
        :return: Action that gets the agent closer to the destination node
        """

        # get the agent's current position
        current_position = self._position
        # get the agent's final destination
        final_dest = deepcopy(dest_node)
        # check if the destination node is None
        if dest_node is None:
            # if so, return an Exception
            return Exception

        # check if the destination node is the agent's current position
        if dest_node == current_position:
            # if so, return an Exception
            return Exception

        # get the previous node in the shortest path to the destination node
        while previous[dest_node] != current_position:
            dest_node = previous[dest_node]
        # check if action is in the action space
        if dest_node in action_space:
            # if so, return the action
            self._log.debug(f"Agent {self._id} is taking action {dest_node} to get closer to node {final_dest}")
            return dest_node
        else:
            # if not, return an Exception
            return Exception

    def _dijkstra(self, position, adjacency_list):
        """
        Method to get the shortest path to all nodes from a given position

        source: adapted from - https://towardsdatascience.com/search-algorithm-dijkstras-algorithm-uniform-cost-search-with-python-ccbee250ba9

        :param position: Position to get the shortest path from
        :param adjacency_list: Adjacency list of the agent
        :return: Dictionary of distances from the position to all nodes
        """

        # create adjacency dictionary with costs = 1 for all links
        # NOTE: here is where you used the link lengths if desired or add them in the build_agent_adjacency_list method
        adjacency_dict = {}
        for node in adjacency_list:
            adjacency_dict[node] = {}
            for neighbour in adjacency_list[node]:
                adjacency_dict[node][neighbour] = 1

        # create a dictionary of distances from the position
        distances = {}
        # create a dictionary of previous nodes - this is used to reconstruct the path
        previous = {}
        # create a queue of nodes to evaluate
        queue = list(adjacency_dict.keys())
        # set the distance of the position to 0
        distances[position] = 0
        # set the distance of all other nodes to infinity
        for node in queue:
            if node != position:
                distances[node] = float('inf')
            previous[node] = None

        # while there is a queue
        while queue:
            # get the node in the queue with the smallest distance
            current_node = min(queue, key=lambda x: distances[x])
            # remove the current node from the unvisited nodes
            queue.remove(current_node)
            # for each neighbour of the current node
            for neighbour in adjacency_dict[current_node]:
                # get the distance to the neighbour
                distance = distances[current_node] + adjacency_dict[current_node][neighbour]
                # if the distance is smaller than the current distance to the neighbour
                if distance < distances[neighbour]:
                    # update the distance to the neighbour
                    distances[neighbour] = distance
                    # update the previous node of the neighbour
                    previous[neighbour] = current_node

        return distances, previous

    def _random_action(self, action_space):
        """
        Method to get a random action from the action space
        :param action_space: Action space - list of possible actions
        :return: Random action
        """
          
        # get a random action from the action space
        action = random.choice(action_space)
        # log the action
        self._log.info(f"Agent {self._id} is taking random action {action}")

        return action
