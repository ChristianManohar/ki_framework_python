"""
Defines the Local Knowledge layer in the KI framework
"""

import networkx as nx
import matplotlib.pyplot as plt
import queue
from framework.data_types.information_structure import InformationStructure, Node
from framework.local_information import LocalInformation

class LocalKnowledge:
    def __init__(self, structure=None, root=None):
        """
        Initializes the Local Knowledge layer for a single agent.
        Member variables:
            - structure (InformationStructure): The information structure grown by the agent.
            - root (Node): The root node of the information structure grown by the agent.
            - roots (list[Node]): List of root nodes of the information layer.
        """
        self.structure = structure
        self.root = root
        self.roots = []
    
    def add_structure(self, new_structure:InformationStructure):
        """
        Adds an InformationStructure to the Local Knowledge layer.
        Args:
            structure (InformationStructure): The information structure to be added.
            root (Node): 
        """
        if not isinstance(new_structure, InformationStructure):
            raise TypeError("structure must be an instance of InformationStructure.")
        if self.structure is None:
            self.structure = new_structure
            self.root = new_structure.get_root_node()
        else:
            self.structure.compose(new_structure)
    
    def contains_node(self, node:Node):
        """
        Checks if a node is part of the Local Knowledge layer's information structure.
        Args:
            node (Node): The node to check.
        Returns:
            bool: True if the node is part of the structure, False otherwise.
        """
        if not isinstance(node, Node):
            raise TypeError("node must be an instance of Node.")
        if self.structure is None:
            return False
        return node.id == self.root.id
    
    def draw(self):
        """
        Draws the information structure of the Local Knowledge layer using matplotlib.
        """
        if self.structure is None:
            print("No structure to draw.")
            return
        plt.title(f"Knowledge Structure, Root Node = {self.root.id}" if self.root else "Knowledge Structure")
        nx.draw(self.structure.structure, with_labels=True, node_size=700, font_size=10, edge_color='gray')
        plt.show()
    
    def expand(self, agent:LocalInformation, root:Node):
        """
        Expands the Local Knowledge layer by adding new structures from another agent.
        Args:
            agent (LocalInformation): The agent whos information structures are to be added.
            root (Node): Initial root node for the expansion.
        """
        if not isinstance(agent, LocalInformation):
            raise TypeError("agent must be an instance of LocalInformation.")
        node_queue = queue.Queue()
        self.root = root
        self.roots.append(root)
        node_queue.put(root)
        while not node_queue.empty():
            curr = node_queue.get()
            supporting_structure = agent.get_structure(curr)
            self.add_structure(supporting_structure)

            # Check if any nodes in the supporting structure are root nodes for other structures in the agent's information layer
            # If they are, add them to the Local Knowledge layer's roots and queue them for further expansion
            for node in supporting_structure.node_list:
                if agent.is_root_node(node) and node.id not in [n.id for n in self.roots]:
                    self.roots.append(node)
                    node_queue.put(node)