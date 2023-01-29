# Import modules
import debug.logger as logger
from src.belief import Belief

### Transmittable Class ###
class Transmittable:
    """
    Transmittable Class
    ----------
    Class to create a transmittable object.
    This class is used to create the transmittable objects that are sent between agents in the environment.

    The transmittable objects are used to update the belief states of the agents in the environment and 
    are formed of the belief states of the other agents in communication range.

    :param belief: Belief state of the agent
    """

    def __init__(self, belief : Belief) -> None:
        self.belief = belief

    def to_transmittable(self) -> dict:
        """
        Convert the transmittable object to a dictionary
        :return: Dictionary representation of the transmittable object
        """
        return self.belief.__dict__

    @classmethod
    def from_transmittable(cls, transmittable_data):
        """
        Convert the transmittable data back into a belief state object
        :param transmittable_data: Dictionary representation of the transmittable object
        :return: Belief state object
        """
        return cls(Belief.from_dict(transmittable_data))