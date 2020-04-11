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
        output_string = "EulerTree(dc:{},level:{},node{})".format(self.dc.max_level, self.level, self.node)
        return output_string
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

        g_nodes = G.nodes
        for node in g_nodes:
            # this is in place of dc_node_struct
            g_nodes[node]["active_occ"] = [None for i in range(self.max_level + 1)]
            g_nodes[node]["adjacent_edges"] = [None for i in range(self.max_level + 1)]
            for level in range(self.max_level + 1):
                g_nodes[node]["active_occ"][level] = EulerTree(self, node, level, True)

def test1():
    G = nx.Graph()
    for i in range(10):
        G.add_node(i)

    p = DynamicCon(G)
    print(p.G.nodes(data = True))
if __name__ == "__main__":
    test1()
