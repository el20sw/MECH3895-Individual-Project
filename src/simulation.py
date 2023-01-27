import wntr

### Pipe Network Simulation ###
class Simulation:
    def __init__(self, environment):
        """
        Class to simulate the pipe network environment
        :param environment: Environment to simulate
        """
        self.environment = environment
        # Initialise the agents
        self.agents = []
        # Variables
        self.turns = 0
        self.pct_explored = []

    def add_agent(self, agent):
        """
        Method to add an agent to the simulation
        :param agent: Agent to add
        :return: None
        """
        self.agents.append(agent)

    def run(self, max_turns=100):
        """
        Method to run the simulation
        :param max_turns: Maximum number of turns to run the simulation for
        :return: None
        """
        # Run the simulation for a maximum number of turns
        while self.turns < max_turns or self.pct_explored < 100:
            self.step()
            self.get_results()

    def step(self):
        """
        Method to run one step of the simulation
        :return: None
        """
        # Loop through the agents
        for agent in self.agents:
            # Get the observation of the agent
            observation = agent.get_observation(self.environment)
            # Get the action of the agent
            action = agent.get_action(observation)
            # Move the agent
            agent.move(self.environment, action)
            # Communicate with other agents
            agent.communicate(self.environment)
        # Increment the turn
        self.turns += 1

    def get_results(self):
        """
        Method to get the results of the simulation
        :return: Results of the simulation
        """
        results = {
            'num_agents': len(self.agents),
            'turns': self.turns,
            'pct_explored': self.pct_explored.append(len(set(self.agents.visited_nodes)) / len(self.environment.get_node_names()))
        }

        return results

    def write_results_to_file(self, file_path='Results/results.txt'):
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
                f.write(f'{key}: {value}')