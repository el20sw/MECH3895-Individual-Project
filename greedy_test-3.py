# import logger
import src.debug.logger as logger

log = logger.setup_logger(file_name=f'logs/greedy_test-3.log', level='DEBUG')

from src.greedy_agent import GreedyAgent
from src.network import Network
from src.overwatch import Overwatch

# set up basic simulation
env = Network('networks/Net1.inp')
agent = GreedyAgent(env, 'A', '9', communication_range=-1, random_seed=0)
overwatch = Overwatch(env, [agent])

# have agent move in the network
agent.observe(env)
agent.commsPart1(env)
agent.commsPart2(env)
agent.action()
agent.move()
