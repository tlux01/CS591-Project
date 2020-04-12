from WBBTree import WBBTree
import BBTree

class AdjacencyTree(WBBTree):

    # (a,b) is the edge
    def __init__(self, e, weight = 1):
        '''e is an edge, probably represented by a pair of nodes like (node1, node2)'''
        super().__init__(weight)
        self.edge = e

    def __repr__(self):
        return "{}".format(self.edge)
        #return "({}, {})".format(self.weight, self.edge)

    def insert(self, e, weight = 1):
        '''in-place insert edge (a,b) in the tree. return the node with the edge'''
        aux = AdjacencyTree(e, weight)
        self = self.join(aux)
        return aux


def delete(node, dummy):
    '''delete node'''
    t1, t2 = BBTree.split(node, BBTree.LEFT, dummy)
    print("t1:" )
    print(str(BBTree.print_tree(t1)))
    print("t2:" )
    print(str(BBTree.print_tree(t2)))
    
    # UNCOMMENT THIS LINE AFTER:
    #t3, t2 = BBTree.split(node, BBTree.RIGHT, dummy)

    return BBTree.join(t1,t2,dummy)



################### Test ###################################################
def test1():
    dummy = AdjacencyTree( -1 )
    #edges = [(1,2),(2,3),(3,4),(4,5),(5,6)]
    edges = [x for x in range(1,6)]
    ats = [AdjacencyTree(e) for e in edges]
    at = AdjacencyTree( 0 )
    at.makeChild(BBTree.LEFT, ats[0])
    at.makeChild(BBTree.RIGHT, ats[1])
    ats[0].makeChild(BBTree.LEFT, ats[2])
    ats[0].makeChild(BBTree.RIGHT, ats[3])
    ats[1].makeChild(BBTree.RIGHT, ats[4])
    # print("Before deletion")
    # print("In-order: ")
    # print(str(at.in_order()))
    # print("Tree: ")
    # print(str(BBTree.print_tree(at)))

    print("Deleting a node...")
    delete(ats[0],dummy)
    print("After deletion")
    print("In-order: ")
    print(str(at.in_order()))
    print("Tree: ")
    print(str(BBTree.print_tree(at)))
if __name__ == "__main__":
    test1()
    print("Done")
