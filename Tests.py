from DynamicCon import DynamicCon
import networkx as nx
from random import sample


def mySample(s):
    return sample(s,1)[0]

def areConnected(G,node1,node2):
    """test if node1 and node2 are connected in G using bfs. Takes linear time in the number of nodes
    in the connected component of node1"""
    return node2 in list(dict(nx.bfs_successors(G, node1)))

def getRandomConnectedNodes(G):
    """return two random connected nodes"""
    node1 = mySample(G.nodes())
    node2 = mySample(list(dict(nx.bfs_successors(G, node1))))
    return node1, node2

def getRandomNotConnectedNodes(G):
    """return two random connected nodes"""
    node1 = mySample(G.nodes())
    nodes = set(G.nodes())
    CC = set(list(dict(nx.bfs_successors(G,node1))))
    possible_nodes = nodes - CC
    if len(possible_nodes) == 0:
        print("Error: G is connected!")
        return None
    node2 = mySample(list(nodes - CC))
    return node1, node2

def test1(n,p):
    """tests DC and BFS-based connectivity alg on a G(n,p)"""
    G = nx.gnp_random_graph(n,p)
    print("G has {} connected components".format(nx.number_connected_components(G)))
    DC = DynamicCon(G)
    N = 100
    allTrues1 = [False]*N
    allTrues2 = [False]*N
    for i in range(100):
        node1,node2 = getRandomConnectedNodes(G)
        allTrues1[i] = areConnected(G,node1,node2)
        allTrues2[i] = DC.connected(node1,node2)
    print("The BFS-based alg works correctly = " + str(False not in allTrues1))
    print("The DC-based alg works correctly = " + str(False not in allTrues2))

    allFalses1 = [True]*N
    allFalses2 = [True] * N
    for i in range(100):
        node1,node2 = getRandomNotConnectedNodes(G)
        allFalses1[i] = areConnected(G,node1,node2)
        allFalses2[i] = DC.connected(node1,node2)

    print("The BFS-based alg works correctly = " + str(True not in allFalses1))
    print("The DC-based alg works correctly = " + str(True not in allFalses2))

def test2():
    """tests DC with adding and removing edges"""
    # TODO

if __name__ == "__main__":
    n = 200
    test1(n, 2/n)
    print("Done")
