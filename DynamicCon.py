import networkx as nx

from WBBTree import WBBTree

class EulerTree(WBBTree):

    def __init__(self, dc, node, level = -1, active = False):

        # we an EulerTree Node initialize it with zero weight
        super().__init__(0)
        # reference to DynamicCon structure this EulerTree node belongs
        self.dc = dc
        # corresponding networkx node, this is a key, access node with G.nodes[node]
        self.node = node
        # level E_i which this node is stored on
        self.level = level
        # active denotes if this node is the active occurence
        self.active = active
        # left and right edge of node in EulerTree, left edge is represented by
        # (predecessor, node), right edge is (node, successor)
        self.edge_occurences = [None, None]

    def __repr__(self):
        output_string = "EulerTree(dc:{},level:{},node:{})".format(self.dc.max_level, self.level, self.node)
        return output_string

class DynamicConNode():
    def __init__(self):
        # list of EulerTree
        self.active_occ = None
        self.adjacent_edges = None

    def __repr__(self):
        return str(self.active_occ)

class DynamicConEdge():
    def __init__(self):
        self.level = None

        # points to non_tree_edges[level], if this is a tree edge
        # then this is none
        self.non_tree_level_edges = None

        # points to tree_edges[level], if this is a non tree edge
        # then this is none
        self.tree_level_edges = None

        # points to the two ed_nodes corresponding to this edge, are
        # none if this is a tree edge
        self.non_tree_occ = [None, None]

        # points to array for each level the 4 node occurences in EulerTree that
        # represent this edge
        self.tree_occ = None

class DynamicCon:

    def __init__(self, G):
        # G is a networkx graph
        self.G = G

        # number of levels
        logn = 0
        i = len(G.nodes())
        while i > 0:
            logn += 1
            i //= 2

        # constants for asymptotic bounds
        self.small_weight = logn * logn
        self.small_set = 16 * logn
        self.sample_size = 32 * logn * logn
        # this is l in the paper
        self.max_level = 6 * logn
        # counters for number of edges added to each level
        self.added_edges = [0 for i in range(self.max_level + 1)]
        # rebuild bound of last level, double it as we go up levels
        max_level_bound = 4
        self.rebuild_bound = [max_level_bound * (2**(self.max_level - i)) for i in range(self.max_level + 1)]

        # edge lists is a list of lists, where each list is the set of edges
        # which we will represent as a tuple on a level
        self.non_tree_edges = [[] for i in range(self.max_level + 1)]
        self.tree_edges = [[] for i in range(self.max_level + 1)]

        g_nodes = self.G.nodes
        for node in g_nodes:
            g_nodes[node]["data"] = DynamicConNode()
            g_nodes[node]["data"].active_occ = [None for i in range(self.max_level + 1)]
            g_nodes[node]["data"].adjacent_edges = [None for i in range(self.max_level + 1)]
            for level in range(self.max_level + 1):
                # create euler tree data structure for each node
                g_nodes[node]["data"].active_occ[level] = EulerTree(self, node, level, True)

        g_edges = self.G.edges
        for edge in g_edges:
            g_edges[edge]["data"] = DynamicConEdge()
        print(G.edges(data=True))

    # returns boolean of whether the two nodes are in the same tree and thus connected
    def connected(self, u, v, i = None):
        # if no level provided, assume max_level
        if i is None:
            i = self.max_level
        g_nodes = self.G.nodes
        # get active_occ
        u_active_occ = g_nodes[u]["data"].active_occ[i]
        v_active_occ = g_nodes[v]["data"].active_occ[i]

        # if they have the same root
        return(u_active_occ.find_root() is v_active_occ.find_root())

    # Insert edge into F_i, the tree spanning Union G_j , j <= i, where i
    # is the level
    def insert_tree(self, edge, i, create_tree_occ = False)
        # create_tree_occ is to flag signifying if we need to construct list
        # tree_occ for the DynamicCon class

        #endpoints
        u = edge[0]
        v = edge[1]

        # DynamicConEdge
        self.G.edges[edge]["data"].level = i

        # create some empty lists
        if create_tree_occ:
            # 4 node occurences in EulerTree
            self.G.edges[edge]["data"].tree_occ = [[None, None, None, None] for i in range(max_level+1)]

        ###IMPLEMENT et_link

        # edge now has pointer to DynamicCon's tree edges at level i,
        # and add edge to this list
        self.G.edges[edge]["data"].tree_level_edges = self.tree_edges[i].append(edge)
def test1():
    G = nx.Graph()
    for i in range(3):
        G.add_node(i)
    G.add_edge(0,1)
    G.add_edge(1,2)
    p = DynamicCon(G)
    #print(p.G.nodes(data = True))


if __name__ == "__main__":
    test1()
