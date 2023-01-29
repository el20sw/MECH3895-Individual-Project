# Import logger
import debug.logger as logger

### Import modules
from src.overwatch import OverWatch

### Pipe Network Simulation ###
class Simulation:
    def __init__(self, environment):
        """
        Class to simulate the pipe network environment
        :param environment: Environment to simulate
        """
        # Initialise the logger
        self.log = logger.get_logger(__name__)
        # Initialise the environment
        self.environment = environment
        # Initialise the agents
        self.agents = []
        self.num_agents = 0
        # Variables
        self.turns = 0
        self.pct_explored = 0
        self.visited_nodes = []
        # Initialise the overwatch
        self.ow = OverWatch(self.environment, self.agents)
        self.ow_agent_positions = {}
        self.ow_visited_junctions = []

    def add_agent(self, agent):
        """
        Method to add an agent to the simulation - can be used to add multiple agents
        :param agent: Agent/s to add
        :return: None
        """
        # if multiple agents are passed
        if isinstance(agent, list):
            for a in agent:
                self.agents.append(a)
                self.log.info(f"Agent {a.agent_id} added to simulation")
        # if a single agent is passed
        else:
            self.agents.append(agent)
            self.log.info(f"Agent {agent.agent_id} added to simulation")

        # Update the number of agents
        self.num_agents = len(self.agents)

    def run(self, max_turns=100):
        """
        Method to run the simulation
        :param max_turns: Maximum number of turns to run the simulation for
        :return: None
        """
        # Run the simulation for a maximum number of turns
        while self.turns < max_turns and self.pct_explored < 100:
            # Run one step of the simulation
            self.step()
            # Update the results
            self.update_results()
            # Increment the turn (local turn count)
            self.turns += 1
            # Log the turn
            self.log.info(f"Turn {self.turns} completed")
            # Log the agents position
            for agent in self.agents:
                self.log.info(f"Agent {agent.agent_id} is at node {agent.position}")

    def step(self):
        """
        Method to run one step of the simulation
        :return: None
        """
        # Loop through the agents
        for agent in self.agents:
            # Get the observation of the agent
            observation = agent.get_observation(self.environment)
            # TODO: Communicate with other agents
            # agent.communicate(self.environment)
            # TODO: Update the belief state of the agent
            # agent.update_belief_state(self.environment)
            # Get the action of the agent
            action = agent.get_action(observation)
            # Move the agent
            agent.move(self.environment, action)
            # Communicate with other agents
            agent.communicate(self.environment)

        # Update the overwatch
        self.ow.update()

    def update_results(self):
        """
        Method to update the results of the simulation - interface with overwatch
        :return: None
        """
        # Get the agent positions
        self.ow_agent_positions = self.ow.get_agent_positions()
        # Get the nodes that have been visited by all agents
        self.ow_visited_junctions = self.ow.get_visited_junctions()
        # Log the number of nodes explored
        self.log.info(f"{len(self.ow_visited_junctions)} nodes explored")

        # Get the percentage of nodes explored (from the overwatch)
        self.pct_explored = self.ow.get_pct_explored()
        # Log the percentage of nodes explored
        self.log.info(f"{self.pct_explored}% of nodes explored")


    def get_results(self):
        """
        Method to get the results of the simulation
        :return: Results of the simulation
        """
       # Packaged results
        results = {
            'num_agents': len(self.agents),
            'turns': self.turns,
            'visited_junctions': self.ow_visited_junctions,
            'pct_explored': self.pct_explored
        }

        return results

    def write_results_to_file(self, file_path='results/results.txt'):
        """
        Method to write the results of the simulation to a file
        :param file_path: Path to the file
        :return: None
        """
        # Get the results
        results = self.get_results()
        # Write the results to a file
        with open(file_path, 'w') as f:
            for key, value in results.items():
                f.write(f'{key}: {value}\n')
