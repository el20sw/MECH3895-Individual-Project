# Class representing a node in the system (a node is a point where pipes connect)
class Node:
    # Constructor for the node class (takes a given id)
    def __init__(self, id):
        self.id = id

    # Method to get the id of the node
    def get_id(self):
        return self.id

    # Method to set the id of the node
    def set_name(self, id):
        self.id = id

    # String representation of the node
    def __str__(self):
        return '{}'.format(self.id)

    # String representation of the node
    def __repr__(self):
        return '{}'.format(self.id)

