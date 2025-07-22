from information_structure import InformationStructure, Node
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def test_compose():
    print("Testing compose function")
    # Create nodes
    nodes1 = [Node(id='A'), Node(id='B', value=2), Node(id='C', value=3)]
    nodes2 = [Node(id='D', value=4), Node(id='E', value=5), Node(id='A', value=1)] # Duplicate node for composition
    #Create edges
    edges1 = [('A', 'B'), ('A', 'C')]
    edges2 = [('D', 'E'), ('A', 'D')]
    info1 = InformationStructure(node_list=nodes1, edges=edges1, root=nodes1[0])
    info2 = InformationStructure(node_list=nodes2, edges=edges2, root=nodes2[0]) # Different root node
    # Draw original structures
    info1.draw()
    info2.draw()
    # Compose structures
    info1.compose(info2)
    print("Compose Information Structure")
    info1.draw()

def test_add_node():
    print("Testing add_node function")
    # Tests add_node when nodes are already present in the structure.
    # Create nodes
    nodes = [Node(id='A', value=1), Node(id='B', value=2)]
    edges = [('A', 'B')]
    info_structure = InformationStructure(node_list=nodes, edges=edges, root=nodes[0])
    info_structure.draw()

    # Add a new node
    new_node = Node(id='C', value=3)
    info_structure.add_node(new_node, (new_node.id, info_structure.get_root_node().id))
    info_structure.draw()

    # Add another node without an edge
    another_node = Node(id='D')
    info_structure.add_node(another_node)
    info_structure.draw()

    # Add an edge
    info_structure.add_edge((new_node.id, another_node.id))
    info_structure.draw()

def test_empty_structure():
    """
    Tests the creation of an empty InformationStructure.
    """
    print("Testing empty InformationStructure")
    empty = InformationStructure()
    empty.draw()

    node = Node(id='A', value=1)
    empty.add_node(node, edge=None)
    empty.draw()

def main():
    """
    Main function to run all tests.
    """
    test_compose()
    test_add_node()
    test_empty_structure()

if __name__ == "__main__":
    main()