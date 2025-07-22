"""
Defines the basic Node and information structure class used in the KI framework.
"""
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

class Node:
    def __init__(self, id:int, value=None, data_status=False):
        """
        Initializes a Node with a value and an optional data status.
        Args:
            id (int): Unique identifier for the node.
            value (double): The value of the node.
            data_status (bool): Indicates if the node's data is known or not.
        """
        self.id = id
        self.value = value
        if self.value is not None:
            self.data_status = True
        else:
            self.data_status = False

class InformationStructure:
    
    def __init__(self, node_list=None, edges=None, root=None):
        """
        Initializes the InformationStructure as a graph with nodes, edges, and a defined root node.
        Args:
            node_list (list): List of nodes in the structure.
            edges (list): List of edges connecting the nodes, uses node ids to denote edges.
            root (node): The root node of the structure.
        """
        self.node_list = node_list if node_list is not None else []
        self.node_id_list = [node.id for node in self.node_list] if node_list else []
        self.edges = edges if edges is not None else []
        self.root = root
        self.structure = nx.Graph()
        self.structure.add_nodes_from(node.id for node in self.node_list)
        self.structure.add_edges_from(self.edges)
        if self.root and self.root not in self.node_list:
            raise ValueError("Root node must be in the node list.")
        
    def empty(self):
        """
        Checks if the structure is empty.
        Returns:
            bool: True if the structure is empty, False otherwise.
        """
        return len(self.node_list) == 0

    def contains_node(self, node:Node):
        """
        Checks if a node is part of the information structure.
        Args:
            node (Node): The node to check.
        Returns:
            bool: True if the node is part of the structure, False otherwise.
        """
        return node.id in self.node_id_list
    
    def draw(self):
        """
        Draws the information structure using matplotlib, displaying nodes, edges, and designating the root node.
        """
        plt.title(f"Information Structure, Root Node = {self.root.id}" if self.root else "Information Structure")
        nx.draw_spring(self.structure, with_labels=True, node_size=700, font_size=10, edge_color='gray')
        plt.show()

    def get_root_node(self):
        """
        Returns the root node of the information structure.
        """
        return self.root

    def add_node(self, node:Node, edge=None):
        """
        Adds a node to the information structure. If a specific edge is provided, it connects the new node to an existing node.
        If no edge is provided, the node is added to the structure without any connections.
        If the structure is empty, the new node becomes the root node.
        If an edge is provided and the node is not already in the structure, it adds the node and connects it to the specified edge.
        Args:
            node (Node): The node to be added.
            edge (tuple): (Optional) A tuple representing the edge to be added, connecting the new node to an existing node.
        """

        if not isinstance(node, Node):
            raise TypeError("node must be an instance of Node.")
        if edge is not None and not isinstance(edge, tuple):
            raise TypeError("edge must be a tuple representing the edge to be added.")
        if edge is not None and len(edge) != 2:
            raise ValueError("edge must be a tuple of length 2, representing the source and target node ids.")
        
        # If the architecture is empty, set the new node as the root
        if self.empty():
            self.root = node
            self.node_list.append(node)
            self.node_id_list.append(node.id)
            self.structure.add_node(node.id)
        else:
            # Add the new node to the structure
            self.node_list.append(node)
            self.node_id_list.append(node.id)
            self.structure.add_node(node.id)
            # Add the edge to the structure if it is provided
            if edge is not None:
                self.structure.add_edge(edge[0], edge[1])
                self.edges.append(edge)
        

    def add_edge(self, edge:tuple):
        """
        Adds an edge to the information structure.
        Args:
            edge (tuple(str, str)): A tuple representing the edge to be added, connecting two nodes.
        """
        if not isinstance(edge, tuple) or len(edge) != 2:
            raise ValueError("edge must be a tuple of length 2, representing the source and target node ids.")
        if edge[0] not in self.node_id_list or edge[1] not in self.node_id_list:
            raise ValueError("Both nodes in the edge must be present in the node list.")
        self.structure.add_edge(edge[0], edge[1])
        self.edges.append((edge[0], edge[1]))

    def compose(self, other):
        """
        Adds the edges and nodes of another InformationStructure to this one, effectively composing them.
        Args:
            other (InformationStructure): The other information structure to compose with
        """
        if not isinstance(other, InformationStructure):
            raise TypeError("other must be an instance of InformationStructure.")
        new_graph = nx.compose(other.structure, self.structure)
        self.node_list = new_graph.nodes
        self.edges = new_graph.edges
        self.structure = new_graph
    
    def compare_structure(self, other):
        """
        Compares the current information structure with another one.
        Args:
            other (InformationStructure): The other information structure to compare with.
        Returns:
            bool: True if the structures are identical, False otherwise.
        """
        if not isinstance(other, InformationStructure):
            raise TypeError("other must be an instance of InformationStructure.")
        return nx.is_isomorphic(self.structure, other.structure)
