from framework.global_information import GlobalInformation
from framework.global_knowledge import GlobalKnowledge
from framework.local_information import LocalInformation
from framework.local_knowledge import LocalKnowledge
from framework.data_types.information_structure import InformationStructure, Node
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def test_local_information():
    """
    Test function for LocalInformation class.
    Creates a few InformationStructure objects and adds them to LocalInformation.
    """
    nodes1 = [Node(id='A', value=1), Node(id='B', value=2), Node(id='C', value=3), Node(id='D', value=4)]
    nodes2 = [Node(id='D', value=4), Node(id='E', value=5), Node(id='F', value=6)]
    nodes3 = [Node(id='B', value=2), Node(id='H', value=7), Node(id='I', value=8)]
    nodes4 = [Node(id='F', value=6), Node(id='J', value=9), Node(id='K', value=10)]

    # Create edges
    edges1 = [('A', 'B'), ('A', 'C'), ('A', 'D')]
    edges2 = [('D', 'E'), ('D', 'F')]
    edges3 = [('B', 'H'), ('B', 'I')]
    edges4 = [('F', 'J'), ('F', 'K')]

    # Create Information Structures
    info1 = InformationStructure(node_list=nodes1, edges=edges1, root=nodes1[0])
    info2 = InformationStructure(node_list=nodes2, edges=edges2, root=nodes2[0])
    info3 = InformationStructure(node_list=nodes3, edges=edges3, root=nodes3[0])
    info4 = InformationStructure(node_list=nodes4, edges=edges4, root=nodes4[0])

    # Create Local Information Layer
    local_info = LocalInformation(structure_list=[info1, info2, info3, info4])
    local_info.draw()

def test_local_knowledge():
    """
    Test functions for the LocalKnowledge class.
    """
    def test_basic():
        print("Testing Local Knowledge layer growth")
        # Create nodes and information structures
        # Create nodes
        nodes1 = [Node(id='A', value=1), Node(id='B', value=2), Node(id='C', value=3)]
        nodes2 = [Node(id='D', value=4), Node(id='E', value=5), Node(id='A', value=1)] # Duplicate node for composition
        #Create edges
        edges1 = [('A', 'B'), ('A', 'C')]
        edges2 = [('D', 'E'), ('A', 'D')]
        info1 = InformationStructure(node_list=nodes1, edges=edges1, root=nodes1[0])
        info2 = InformationStructure(node_list=nodes2, edges=edges2, root=nodes2[0]) # Different root node
        # Create Local Knowledge layer
        local_knowledge = LocalKnowledge()
        local_knowledge.add_structure(info1)
        local_knowledge.draw()
        local_knowledge.add_structure(info2)
        local_knowledge.draw()

    def test_expand():
        print("Testing Local Knowledge layer expansion")
        # Create nodes and information structures
        """
        info1:
            A
        / | |
        B  C  D
        info2:
            D
            / \ 
        E  F
        info3:
            B
            / \ 
        H  I
        info4:
            F
            / \ 
        J  K
        """
        # Create nodes
        nodes1 = [Node(id='A', value=1), Node(id='B', value=2), Node(id='C', value=3), Node(id='D', value=4)]
        nodes2 = [Node(id='D', value=4), Node(id='E', value=5), Node(id='F', value=6)]
        nodes3 = [Node(id='B', value=2), Node(id='H', value=7), Node(id='I', value=8)]
        nodes4 = [Node(id='F', value=6), Node(id='J', value=9), Node(id='K', value=10)]

        # Create edges
        edges1 = [('A', 'B'), ('A', 'C'), ('A', 'D')]
        edges2 = [('D', 'E'), ('D', 'F')]
        edges3 = [('B', 'H'), ('B', 'I')]
        edges4 = [('F', 'J'), ('F', 'K')]

        # Create Information Strucrtures
        info1 = InformationStructure(node_list=nodes1, edges=edges1, root=nodes1[0])
        info2 = InformationStructure(node_list=nodes2, edges=edges2, root=nodes2[0])
        info3 = InformationStructure(node_list=nodes3, edges=edges3, root=nodes3[0])
        info4 = InformationStructure(node_list=nodes4, edges=edges4, root=nodes4[0])

        # Create Local Information Layer
        local_info = LocalInformation(structure_list=[info1, info2, info3, info4])

        # Create local knowledge layer
        local_knowledge = LocalKnowledge()
        root = Node(id='A', value=1) # Initial root node for expansion
        local_knowledge.expand(agent=local_info, root=root)
        local_knowledge.draw()

    test_basic()
    test_expand()

def test_global_information():
    print("Testing grow_global function")
    """
    Test will Have 3 main agents
    Agent 1:
                T1
                |
                a
               / \
              b -  d
                   |
                   T2
    Agent 2:
                T2
                |
                a
               / \
              b   d
             /    |
            c     e
                  |
                  g
                  |
                  TK
    Agent 3:
                TN
                |
                d
                |
                c
    
    The global information layer will be initialized with the nodes T1, TK, and TN.
    The growth will start from T1, and will traverse through the local knowledge layers of agents
    to build the global information structure.
    The expected result is that the global information layer will contain the necessary root nodes and their connections from 
    the local knowledge layers.
    """
    # Create nodes
    nodes1 = [Node('T1'), Node('a'), Node('b', value=1), Node('d'), Node('T2')]
    nodes2 = [Node('T2'), Node('a'), Node('b', value=1), Node('c', value=1), Node('d'), Node('e'), Node('g'), Node('TK', value=1)]
    nodes3 = [Node('TN', value=1), Node('d'), Node('c')]

    # Create edges
    edges1 = [('T1', 'a'), ('a', 'b'), ('a', 'd'), ('b', 'd'), ('d', 'T2')]
    edges2 = [('T2', 'a'), ('a', 'b'), ('a', 'd'), ('b', 'c'), ('d', 'e'), ('e', 'g'), ('g', 'TK')]
    edges3 = [('TN', 'd'), ('d', 'c')]

    # Create information structures
    info1 = InformationStructure(node_list=nodes1, edges=edges1, root=nodes1[0])
    info2 = InformationStructure(node_list=nodes2, edges=edges2, root=nodes2[0])
    info3 = InformationStructure(node_list=nodes3, edges=edges3, root=nodes3[0])

    # Draw them for sanity
    """info1.draw()
    info2.draw()
    info3.draw()"""

    init_nodes = [Node('T1'), Node('TK', value=1), Node('TN')]

    agent1 = LocalKnowledge(structure=info1, root=info1.root)
    agent2 = LocalKnowledge(structure=info2, root=info2.root)
    agent3 = LocalKnowledge(structure=info3, root=info3.root)

    for agent in [agent1, agent2, agent3]:
        agent.draw()

    """agent1.draw()
    agent2.draw()
    agent3.draw()"""

    agent_list = [agent1, agent2, agent3]

    global_info = GlobalInformation(init_nodes=init_nodes, agent_list=agent_list)
    global_info.grow_global()
    global_info.draw()

def test_global_knowledge():
    """
    Test function for GlobalKnowledge class.
    """
    print("Testing GlobalKnowledge layer")
    # Example usage of GlobalKnowledge layer using example from GlobalInformation layer.
    nodes1 = [Node('T1'), Node('a'), Node('b', value=1), Node('d'), Node('T2')]
    nodes2 = [Node('T2'), Node('a'), Node('b', value=1), Node('c', value=1), Node('d'), Node('e'), Node('g'), Node('TK', value=1)]
    nodes3 = [Node('TN', value=1), Node('d'), Node('c')]

    # Create edges
    edges1 = [('T1', 'a'), ('a', 'b'), ('a', 'd'), ('b', 'd'), ('d', 'T2')]
    edges2 = [('T2', 'a'), ('a', 'b'), ('a', 'd'), ('b', 'c'), ('d', 'e'), ('e', 'g'), ('g', 'TK')]
    edges3 = [('TN', 'd'), ('d', 'c')]

    # Create information structures
    info1 = InformationStructure(node_list=nodes1, edges=edges1, root=nodes1[0])
    info2 = InformationStructure(node_list=nodes2, edges=edges2, root=nodes2[0])
    info3 = InformationStructure(node_list=nodes3, edges=edges3, root=nodes3[0])

    init_nodes = [Node('T1'), Node('TK', value=1), Node('TN')]

    agent1 = LocalKnowledge(structure=info1, root=info1.root)
    agent2 = LocalKnowledge(structure=info2, root=info2.root)
    agent3 = LocalKnowledge(structure=info3, root=info3.root)

    agent_list = [agent1, agent2, agent3]

    global_info = GlobalInformation(init_nodes=init_nodes, agent_list=agent_list)
    global_info.grow_global()
    global_info.draw()

    global_knowledge = GlobalKnowledge(init_nodes=init_nodes)
    global_knowledge.add_edges(global_info=global_info)
    global_knowledge.draw()

def main():
    """
    Ask the user which test to run.
    """
    while(True):
        print("Select a test to run:")
        print("1. Local Information Tests")
        print("2. Local Knowledge Test")
        print("3. Global Information Test")
        print("4. Global Knowledge Test")
        choice = input("Choose test number: ")
        if choice == '1':
            test_local_information()
        elif choice == '2':
            test_local_knowledge()
        elif choice == '3':
            test_global_information()
        elif choice == '4':
            test_global_knowledge()
        else:
            print("No number chosen. Exiting tests.")
            break
        print("Run another test? (y/n)")
        if input().lower() != 'y':
            print("Exiting tests.")
            break
    # Let user choose which test to run, allow multiple tests to be run
    
    
if __name__ == "__main__":
    main()

