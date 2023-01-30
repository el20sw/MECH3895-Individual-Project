# Import modules
import src.debug.logger as logger

### Transmittable Class ###
class Transmittable:
    """
    Transmittable Class
    ----------
    Class to create a transmittable object that are sent between agents in the environment.

    The class takes any number of objects as arguments and stores them in a list.
    :param *args: Objects to be transmitted
    """

    def __init__(self, *args):
        # Initialise the logger
        self.log = logger.get_logger(__name__)
        # Initialise the list of objects
        self.objects = []
        # Add objects to the list
        for obj in args:
            self.objects.append(obj)
        # Log the transmittable
        self.log.debug(f'Transmittable: {self}')

    def __str__(self):
        """
        String representation of the transmittable
        :return: String representation of the transmittable
        """
        return f'{self.objects}'

    def __repr__(self):
        """
        Representation of the transmittable
        :return: Representation of the transmittable
        """
        return f'{self.objects}'