"""
Defines the LocalInformation class used in the KI framework, describes a local information layer.
"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from framework.data_types.information_structure import InformationStructure, Node

class LocalInformation:

    def __init__(self, structure_list:list):
        """
        Initializes the LocalInformation layer with a given size and a list of InformationStructure objects.
        Args:
            structure_list (list): List of InformationStructure objects.
        """
        self.structures = {}
        for structure in structure_list:
            if not isinstance(structure, InformationStructure):
                raise TypeError("All elements in structure_list must be of type InformationStructure.")
            # Assign the root node's ID as the key and the structure as the value
            if structure.get_root_node().id in self.structures:
                raise ValueError(f"Duplicate root node ID found: {structure.get_root_node().id}")
            self.structures[structure.get_root_node().id] = structure
        self.size = len(self.structures)
    
    def get_structure(self, root):
        """
        Returns the InformationStructure associated with the given root node ID.
        Args:
            root (Node): The root node whose structure is to be retrieved.
        
        Returns:
            InformationStructure: The structure associated with the root node.
        """
        if not isinstance(root, Node):
            raise TypeError("Root must be an instance of Node.")
        if root.id not in self.structures:
            raise KeyError(f"No structure found for root node ID: {root.id}")
        return self.structures[root.id]
    
    def is_root_node(self, node):
        """
        Checks if the given node is a root node for an InformationStructure in this layer.
        Args:
            node (Node): The node to check.
        Returns:
            bool: True if the node is a root node, False otherwise. 
        """
        if not isinstance(node, Node):
            raise TypeError("Node must be an instance of Node.")
        return node.id in self.structures
    
    def draw(self):
        """
        Draws all InformationStructures in the LocalInformation layer using matplotlib.
        """
        plt.figure(figsize=(10, 10))
        for i, (root_id, structure) in enumerate(self.structures.items()):
            plt.subplot(len(self.structures), 1, i + 1)
            plt.title(f"Information Structure with Root Node ID = {root_id}")
            nx.draw(structure.structure, with_labels=True, node_size=300, font_size=10, edge_color='gray')
        plt.show()
    
    def add_structure(self, new_structure:InformationStructure):
        """
        Adds a new InformationStructure to the LocalInformation layer.
        Args:
            new_structure (InformationStructure): The structure to be added.
        """
        self.structures[new_structure.get_root_node().id] = new_structure
        self.size += 1