"""
Defines the GlobalKnowledge layer used in the KI framework, which extracts information from the 
GlobalInformation layer, and draws connections only between nodes present in the GlobalKnowledge layer.
"""
from framework.data_types.information_structure import InformationStructure, Node
from framework.local_information import LocalInformation
from framework.local_knowledge import LocalKnowledge
from framework.global_information import GlobalInformation
import networkx as nx
import matplotlib.pyplot as plt


class GlobalKnowledge:
    def __init__(self, init_nodes: list[Node]):
        """
        Initializes the Global Knowledge layer with a list of initial nodes.
        Args:
            init_nodes (list[Node]): List of Node objects to initialize the global knowledge layer. Nodes can be empty or have values.
        Member variables:
            - structure (InformationStructure): The information structure representing the global knowledge layer.
            - node_list (list[Node]): List of nodes in the global knowledge layer.
        """

        if not isinstance(init_nodes, list):
            raise TypeError("init_nodes must be a list of Node objects.")
        self.node_list = init_nodes
        self.node_id_list = [node.id for node in self.node_list]
        # Create an InformationStructure with the provided nodes and no edges or root.
        # Edges will be add later when the GlobalKnowledge layer is examined by the agent.
        self.structure = InformationStructure(node_list=self.node_list, edges=[], root=None)

    def find_connections(self, node: Node, global_info: GlobalInformation) -> list[Node]:
        """
        Finds connections for a given node in the GlobalInformation layer.
        Args:
            node (Node): The node for which connections are to be found.
            global_info (GlobalInformation): The GlobalInformation layer to search for connections.
        Returns:
            list[Node]: List of nodes that are connected to the given node in the GlobalInformation layer.
        """
        connections = []
        for structure in global_info.structures.values():
            if structure.contains_node(node):
                # If the node is found in the structure, return all connected nodes.
                for n in structure.node_list:
                    # Excluding the node itself, add a node to connections if it is part of the global knowledge layer.
                    # This ensures that we only consider nodes that are part of the global knowledge layer.
                    if n.id != node.id and n.id in self.node_id_list:
                        connections.append(n)
                return connections
        # If no connections are found, return an empty list.
        return []

    def add_edges(self, global_info: GlobalInformation):
        """
        Adds edges to the GlobalKnowledge layer based on the connections found in the GlobalInformation layer.
        Args:
            global_info (GlobalInformation): The GlobalInformation layer to extract connections from.
        """
        for node in self.node_list:
            connections = self.find_connections(node=node, global_info=global_info)
            for c in connections:
                self.structure.add_edge((node.id, c.id))
            
    def draw(self):
        """
        Draws the information structure of the Global Knowledge layer using matplotlib.
        """
        if self.structure is None:
            print("No structure to draw.")
            return
        plt.title("Global Knowledge Structure")
        nx.draw(self.structure.structure, with_labels=True, node_size=700, font_size=10, edge_color='gray')
        plt.show()