"""
Defines the Global Information class used in the KI framework, which is grown from a collection of local knowledge layers.
"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from queue import LifoQueue
from framework.data_types.information_structure import InformationStructure, Node
from framework.local_information import LocalInformation
from framework.local_knowledge import LocalKnowledge

class GlobalInformation:
    def __init__(self, init_nodes:list[Node], agent_list:list[LocalKnowledge]):
        """
        Initializes the GlobalInformation layer with a list of initial nodes that can be known or unknown.
        Args:
            init_nodes (list[Node]): List of Node objects to initialize the global information layer.
            agent_list (list[LocalKnowledge]): List of LocalKnowledge objects representing the local knowledge of agents.
        
        Member Variables:

        """
        if not isinstance(init_nodes, list):
            raise TypeError("init_nodes must be a list of Node objects.")
        self.init_nodes = init_nodes
        self.init_nodes_ids = [node.id for node in init_nodes]
        if not isinstance(agent_list, list):
            raise TypeError("agent_list must be a list of LocalKnowledge objects.")
        self.agent_list = agent_list
        self.structures = {}
        for node in init_nodes:
            if not isinstance(node, Node):
                raise TypeError("All elements in init_nodes must be of type Node.")
        self.visited = np.zeros(len(init_nodes), dtype=bool)

        self.roots = []
        for agent in agent_list:
            if not isinstance(agent, LocalKnowledge):
                raise TypeError("All elements in agent_list must be of type LocalKnowledge.")
            if agent.root is None:
                raise ValueError("LocalKnowledge agent must have a root node.")
            self.roots.append(agent.root.id)
    
    # Might not actually need this function, will just keep it for now
    def is_visited(self, node:Node):
        """
        Checks if a node has been visited in the global information layer during the growth process.
        Args:
            node (Node): The node to check.
        Returns:
            bool: True if the node has been visited, False otherwise.
        """
        if not isinstance(node, Node):
            raise TypeError("node must be an instance of Node.")
        if node.id not in self.init_nodes:
            raise KeyError(f"Node with ID {node.id} not found in the global information layer.")
        index = self.init_nodes.index(node)
        return self.visited[index]
    
    def get_node(self):
        """
        Returns a node that is not yet visited in the global information layer. 
        If all nodes have been visited, returns None.
        Returns:
            Node: An unvisited node from the global information layer, or None if all nodes have been visited.
        """
        for i, node in enumerate(self.init_nodes):
            if not self.visited[i]:
                self.visited[i] = True
                return node
        return None

    def find_agent(self, node):
        """
        Finds the local knowledge layer that contains the given node.
        Args:
            node (Node): The node to find in the local knowledge layers.
        Returns:
            LocalKnowledge: The local knowledge layer that contains the node, or None if not found.
        """
        if not isinstance(node, Node):
            raise TypeError("node must be an instance of Node.")
        for agent in self.agent_list:
            if agent.contains_node(node):
                return agent
        return None
    
    def all_visited(self):
        """
        Checks if all nodes in the global information layer have been visited.
        Returns:
            bool: True if all nodes have been visited, False otherwise.
        """
        return np.all(self.visited)
    
    def grow_global(self):
        """
        Grows the global information layer by traversing through the local knowledge layers of agents.
        It uses a depth-first search approach to explore the information structures and to build structures from the back.
        """
        stack = []
        while not self.all_visited():
            # Each iteration of this loop will find a new node to start from, and thus will grow a new information structure
            info = InformationStructure()
            # Get a node that has not been visited, and mark as visited
            node = self.get_node()
            root = node
            # Push starter node onto the stack, along with node it came from (itself)
            info.add_node(node, edge=None)
            stack.append((node, node))
            while len(stack) != 0:
                # Get the top of stack, which is a tuple of (current_node, previous_node)
                curr_node = stack[-1]
                if not isinstance(curr_node[0], Node):
                    raise TypeError("curr_node must be an instance of Node.")
                # Check if the current node value is known or not
                if not curr_node[0].data_status:
                    # Find an agent that contains this node
                    agent = self.find_agent(curr_node[0])
                    structure = agent.structure
                    # For each sub-node in the structure, if it is a root node, push it onto the stack
                    for sub_node in structure.node_list:
                        # Might want to change this logic around, for now its ok
                        # If the sub node is not the current node and it is a root node or an init node, push it onto the stack
                        num_added = 0
                        if sub_node.id != curr_node[0].id and (sub_node.id in self.roots or sub_node.id in self.init_nodes_ids):
                            stack.append((sub_node, curr_node[0]))
                            # Add the sub node to the information structure
                            info.add_node(sub_node)
                            # If sub node is an init node, mark it as visited
                            num_added += 1
                            if sub_node.id in self.init_nodes_ids:
                                index = self.init_nodes_ids.index(sub_node.id)
                                self.visited[index] = True
                    if num_added == 0:
                        # If no sub nodes were added, we can pop the current node from the stack as this means it is calculable
                        # and we can add it to the information structure
                        curr_node[0].data_status = True

                else:
                    # If the current node is now known, we can add an edge to the information structure
                    # If the current node is the root node, we do not add an edge to itself
                    # Draw an edge between current node and the node it came from
                    if not curr_node[0].id == curr_node[1].id:
                        info.add_edge((curr_node[0].id, curr_node[1].id))
                        curr_node[1].data_status = True
                        stack.pop()
                    else:
                        stack.pop()
            # After the stack is empty, we have a complete information structure
            self.structures[root.id] = info

    def draw(self):
        """
        Draws the global information layer using matplotlib, displaying nodes, edges, and designating the root nodes.
        """
        plt.figure(figsize=(10, 10))
        for i, (root_id, structure) in enumerate(self.structures.items()):
            plt.subplot(len(self.structures), 1, i + 1)
            plt.title(f"Information Structure with Root Node ID = {root_id}")
            nx.draw(structure.structure, with_labels=True, node_size=700, font_size=10, edge_color='gray')
        plt.show()