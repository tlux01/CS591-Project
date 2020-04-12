from DynamicCon import DynamicCon
import networkx as nx
from random import choice


def areConnected(G,node1,node2):
    '''test if node1 and node2 are connected in G using bfs. Takes linear time in the number of nodes
    in the connected component of node1'''
    return node2 in nx.bfs_successors(G, node1)

def getRandomConnectedNodes(G):
    '''return two random connected nodes'''
    node1 = choice(G.nodes())
    node2 = nx.bfs_successors(G, node1)
    return node1, node2

def getRandomNotConnectedNodes(G):
    '''return two random connected nodes'''
    node1 = choice(G.nodes())
    nodes = set(G.nodes())
    CC = set(nx.bfs_successors).union(set(node1))
    possible_nodes = nodes - CC
    if possible_nodes == set():
        print("Error: G is connected!")
        return None
    node2 = choice(list(nodes - CC))
    return node1, node2

def test1(n,p):
    G = nx.gnp_random_graph(n,p)
    #DC = DynamicCon(G)
    N = 100
    allTrues1 = [False]*N
    allTrues2 = [False]*N
    for i in range(100):
        node1,node2 = getRandomConnectedNodes(G)
        allTrues1[i] = areConnected(G,node1,node2)
        #allTrues2[i] = DC.connected(node1,node2)
    allFalses1 = [True]*N
    for i in range(100):
        node1,node2 = getRandomNotConnectedNodes(G)
        allFalses1[i] = areConnected(G,node1,node2)
        #allTrues2[i] = DC.connected(node1,node2)
    print("The BFS-based alg works correctly = " + str(True not in allTrues1))
    print("The BFS-based alg works correctly = " + str(True not in allFalses1))

if __name__ == "__main__":
    test1(200,0.05)
    print("Done")
