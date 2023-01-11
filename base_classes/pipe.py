# Class representing a pipe in the system (a pipe is a connection between two nodes)
class Pipe:
    # Constructor for the pipe class (takes a given length)
    def __init__(self, length):
        # TODO: Define a default value for the length of the pipe
        self.length = float(length)

    # Method to get the length of the pipe
    def get_length(self):
        return self.length

    # Method to set the length of the pipe
    def set_length(self, length):
        self.length = length

    # String representation of the pipe
    def __str__(self):
        return '{}'.format(self.length)

    # String representation of the pipe
    def __repr__(self):
        return '{}'.format(self.length)
