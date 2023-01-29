# Import logger
import debug.logger as logger

### OverWatch Class ###
class OverWatch:
    def __init__(self, environment, agents):
        """
        Class to deal with meta-data
        :param environment: Environment in which the agents are operating - the pipe network
        :param agents: Agents in the environment
        """
        self.environment = environment
        self.agents = agents
        self.num_agents = len(agents)
        # Initialise the logger
        self.log = logger.setup_logger(__name__, 'logs/overwatch.log')
        # Variables
        self.turns = 0
        self.pct_explored = 0
        self.visited_junctions = []
        self.agent_positions = {}
        self.all_junctions = self.environment.junction_names

    def update(self):
        """
        Method to update the overwatch
        :return: None
        """
        # Update the number of turns
        self.turns += 1
        self.log.info(f"Turn {self.turns}")
        # Update the percentage of nodes explored
        self.pct_explored = self.get_pct_explored()
        self.log.info(f"Percentage of nodes explored: {self.pct_explored}")
        # Update the agent positions
        self.agent_positions = self.get_agent_positions()
        self.log.info(f"Agent positions: {self.agent_positions}")
        # Update the visited nodes
        self.visited_junctions = self.get_visited_junctions()
        self.log.info(f"Visited nodes: {self.visited_junctions}")

    def get_agent_positions(self):
        """
        Method to get the positions of the agents
        :return: Dictionary of agent positions
        """
        # Get the positions of the agents
        for agent in self.agents:
            self.agent_positions[agent.agent_id] = agent.position
        # Return the dictionary
        return self.agent_positions

    def get_visited_junctions(self):
        """
        Method to get the unique visited nodes of the agents
        :return: Dictionary of unique visited nodes
        """
        # Get the unique visited nodes of the agents
        for agent in self.agents:
            self.visited_junctions.extend(agent.visited_junctions)
        self.visited_junctions = list(set(self.visited_junctions))
        # Return the dictionary
        return self.visited_junctions

    def get_pct_explored(self):
        """
        Method to get the percentage of nodes explored
        :return: Percentage of nodes explored
        """
        # Get the percentage of nodes explored
        self.pct_explored = (len(self.visited_junctions) / len(self.all_junctions)) * 100
        # Return the percentage
        return self.pct_explored