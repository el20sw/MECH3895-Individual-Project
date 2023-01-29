class FrozenNodes:
    """
    A class to hold the node keys of the pipe network and keep them frozen
    :param node_keys: List of node keys
    """
    
    def __init__(self, node_keys):
        self._node_keys = node_keys
        self._frozen_node_keys = frozenset(self._node_keys)
    
    @property
    def node_keys(self) -> list:
        return self._node_keys
    
    @property
    def frozen_node_keys(self) -> frozenset:
        return self._frozen_node_keys

class FrozenLinks:
    """
    A class to hold the link keys of the pipe network and keep them frozen
    :param link_keys: List of link keys
    """
    
    def __init__(self, link_keys):
        self._link_keys = link_keys
        self._frozen_link_keys = frozenset(self._link_keys)
    
    @property
    def link_keys(self) -> list:
        return self._link_keys
    
    @property
    def frozen_link_keys(self) -> frozenset:
        return self._frozen_link_keys
