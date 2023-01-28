### Import modules
import numpy as np
from base_classes.agent import Agent

### Random Agent Class ###
class RandomAgent(Agent):
    # Constructor for the simple agent class
    def __init__(self, environment, agent_id, position, communication_range=100):
        # Inherit the constructor from the base class
        super().__init__(environment, agent_id, position, communication_range)

    def move(self, environment, action):
        # Inherit the move method from the base class
        super().move(environment, action)

    def communicate(self, environment):
        # Inherit the communicate method from the base class
        super().communicate(environment)

    def get_observation(self, environment, other_agents=None):
        # Inherit the get_observation method from the base class
        super().get_observation(environment, other_agents)

    def get_action(self, observation):
        # Inherit the get_action method from the base class
        super().get_action(observation)

    def random_behaviour(self, environment):
        # Get the current position of the agent
        current_position = self.position
        # Get the adjacent nodes to the current position
        adjacent_nodes = environment.get_adj_list()[current_position]
        # Choose a random node from the adjacent nodes
        random_node = np.random.choice(adjacent_nodes)
        # Return the random node
        return random_node

    def get_visited_nodes(self):
        return self.visited_nodes()
