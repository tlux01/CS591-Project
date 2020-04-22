from DynamicCon import DynamicCon
import networkx as nx
from random import sample, seed
import random


def mySample(s):
    return sample(s,1)[0]

def areConnected(G,node1,node2):
    """test if node1 and node2 are connected in G using bfs. Takes linear time in the number of nodes
    in the connected component of node1"""
    return node2 in nx.node_connected_component(G,node1)

def getRandomConnectedNodes(G):
    """return two random connected nodes"""
    node1 = mySample(G.nodes())
    node2 = mySample(nx.node_connected_component(G,node1))
    return node1, node2

def getRandomNotConnectedNodes(G):
    """return two random connected nodes"""
    node1 = mySample(G.nodes())
    nodes = set(G.nodes())
    CC = nx.node_connected_component(G,node1)
    possible_nodes = nodes - CC
    if len(possible_nodes) == 0:
        print("Error: G is connected!")
        return None
    node2 = mySample(list(nodes - CC))
    return node1, node2

def test1(n,p):
    """tests DC and BFS-based connectivity alg on a G(n,p)"""
    #seed(69)

    G = nx.gnp_random_graph(n,p)
    print("G has {} connected components".format(nx.number_connected_components(G)))
    DC = DynamicCon(G)
    N = 100
    allTrues1 = [False]*N
    allTrues2 = [False]*N
    for i in range(N):
        node1,node2 = getRandomConnectedNodes(G)
        allTrues1[i] = areConnected(G,node1,node2)
        allTrues2[i] = DC.connected(node1,node2)
    print("The BFS-based alg works correctly = " + str(False not in allTrues1))
    print("The DC-based alg works correctly = " + str(False not in allTrues2))

    allFalses1 = [True]*N
    allFalses2 = [True] * N
    for i in range(N):
        node1,node2 = getRandomNotConnectedNodes(G)
        allFalses1[i] = areConnected(G,node1,node2)
        allFalses2[i] = DC.connected(node1,node2)
        if allFalses2[i]:
            print("DC reports that {} and {} are connected!".format(node1, node2))
            print("Node1: {}, node2: {}. CC of node1: {}".format(node1, node2, nx.node_connected_component(G,node1)))

    print("The BFS-based alg works correctly = " + str(True not in allFalses1))
    print("The DC-based alg works correctly = " + str(True not in allFalses2))

def test2():
    """tests DC with adding edges on n nodes"""
    G = nx.Graph()
    for i in range(5):
        G.add_node(i)
    DC = DynamicCon(G)
    DC.ins(0,1)
    DC.ins(0,1)
    DC.ins(1,2)
    DC.ins(0,4)
    print("edge are: {}".format(G.edges))
    print("DC works correctly wrt insertion = {}".format(DC.connected(0,1)))
    print("DC works correctly wrt insertion = {}".format(DC.connected(0, 2)))
    print("DC works correctly wrt insertion = {}".format(DC.connected(1, 4)))
    print("DC works correctly wrt insertion = {}".format(not DC.connected(1, 3)))

    print("Deleting edge (0,1)...")
    DC.del_edge((0,1))
    DC.del_edge((0, 1))
    print("edge are: {}".format(G.edges))
    print("DC works correctly wrt deletion = {}".format(DC.connected(1,2)))
    print("DC works correctly wrt deletion = {}".format(DC.connected(0,4)))
    print("DC works correctly wrt deletion = {}".format(not DC.connected(0,1)))
    print("DC works correctly wrt deletion = {}".format(not DC.connected(1,4)))


    print("Inserting edge (0,1)...")
    DC.ins(0, 1)
    DC.ins(0, 1)
    print("edge are: {}".format(G.edges))
    print("DC works correctly wrt insertion = {}".format(DC.connected(0, 1)))
    print("DC works correctly wrt insertion = {}".format(DC.connected(1,2)))
    print("DC works correctly wrt insertion = {}".format(DC.connected(0, 2)))
    print("DC works correctly wrt insertion = {}".format(not DC.connected(1, 3)))

def test3():
    G = nx.Graph()
    for i in range(3):
        G.add_node(i)
    DC = DynamicCon(G)
    DC.ins(0, 1)
    DC.ins(0, 1)
    DC.ins(1, 2)
    DC.del_edge((0,1))
    DC.del_edge((0, 1))
    DC.ins(0, 1)
    DC.ins(0, 1)
    print("edges: {}".format(G.edges))
    u = 1
    v = 2
    g_nodes = DC.G.nodes
    print("In-order of the tree containing {}: {}".format(u, g_nodes[u]["data"].active_occ[DC.max_level].find_root().in_order()))
    print("In-order of the tree containing {}: {}".format(v, g_nodes[v]["data"].active_occ[DC.max_level].find_root().in_order()))

def test4():
    seed(10)
    n = 30
    p = .09
    num_tests = 3
    G = nx.gnp_random_graph(n, p)
    DC = DynamicCon(G)
    DC_correct = [False]*num_tests
    for i in range(num_tests):
        r = random.random()
        if r < 0.5:
            # add random edge
            node1 = mySample(G.nodes)
            node2 = mySample(G.nodes - {node1})
            print("{} | Want to insert: {}".format(i,(node1,node2)))
            DC.ins(node1,node2)
        else:
            # remove random edge


            node1, node2 = mySample(G.edges)
            print("{} | Want to delete: {}".format(i,(node1,node2)))
            DC.del_edge((node1,node2))
        node1,node2 = getRandomConnectedNodes(G)
        node3, node4 = getRandomNotConnectedNodes(G)

        DC_correct[i] = DC.connected(node1,node2) and not DC.connected(node3,node4)
        if not DC_correct[i]:
            print("{} and {} connected: {}".format(node1, node2, DC.connected(node1,node2)))
            print("{} and {} not connected: {}".format(node3, node4, DC.connected(node3,node4)))
    print("DC works correctly = {}".format(False not in DC_correct))

def test5():
    seed(10)
    n = 10
    p = .06
    num_tests = 100
    G = nx.gnp_random_graph(n, p)
    DC = DynamicCon(G)
    DC_correct = [False]*num_tests
    for i in range(num_tests):
        r = random.random()
        if r < 0.5:
            # add random edge
            node1 = mySample(G.nodes)
            node2 = mySample(G.nodes - {node1})
            print("{} | Want to insert: {}".format(i,(node1,node2)))
            DC.ins(node1,node2)
        else:
            # remove random edge


            node1, node2 = mySample(G.edges)
            print("{} | Want to delete: {}".format(i,(node1,node2)))
            DC.del_edge((node1,node2))
        node1,node2 = getRandomConnectedNodes(G)
        node3, node4 = getRandomNotConnectedNodes(G)

        DC_correct[i] = DC.connected(node1,node2) and not DC.connected(node3,node4)
        if not DC_correct[i]:
            print("{} and {} connected: {}".format(node1, node2, DC.connected(node1,node2)))
            print("{} and {} not connected: {}".format(node3, node4, DC.connected(node3,node4)))
    print("DC works correctly = {}".format(False not in DC_correct))

def test6():
    G = nx.Graph()
    for i in range(4):
        G.add_node(i)
    G.add_edge(0,1)
    G.add_edge(1,2)




    DC = DynamicCon(G)

    DC.ins(0,2)

    DC.ins(0,3)
if __name__ == "__main__":
    n = 200
    test6()
    print("Done")
