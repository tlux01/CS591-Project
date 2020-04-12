from WBBTree import WBBTree
import BBTree
import random

random.seed(10)
class AdjacencyTree(WBBTree):

    # (a,b) is the edge
    def __init__(self, e, weight = 1):
        '''e is an edge, probably represented by a pair of nodes like (node1, node2)'''
        super().__init__(weight)
        self.edge = e

    def __repr__(self):
        # return "{} , parent: {}, children: [{},{}] |".format(self.edge,
        #                                             self.parent.edge if self.parent else "None",
        #                                             self.child[BBTree.LEFT].edge if self.child[BBTree.LEFT] else "None" ,
        #                                             self.child[BBTree.RIGHT].edge if self.child[BBTree.RIGHT] else "None")
        #return "({}, {})".format(self.weight, self.edge)
        return str(self.edge)
    def insert(self, e, weight = 1):
        '''in-place insert edge (a,b) in the tree. return the node with the edge'''
        aux = AdjacencyTree(e, weight)
        self = BBTree.join(aux)
        return aux


def delete(node, dummy):
    '''delete node'''
<<<<<<< HEAD
    t1, t2 = BBTree.split(node, BBTree.LEFT, dummy)
    print("t1:" )
    print(str(BBTree.print_tree(t1)))
    print("t2:" )
    print(str(BBTree.print_tree(t2)))
    print("node:" )
    print(str(BBTree.print_tree(node)))
=======

    t1, t2 = BBTree.split(node, BBTree.LEFT, dummy)
>>>>>>> 97080c49b8f638d49c914f94735683fe7b08fd02
    # UNCOMMENT THIS LINE AFTER:
    t3, t2 = BBTree.split(node, BBTree.RIGHT, dummy)
    return BBTree.join(t1,t2,dummy)



################### Test ###################################################
def test1():
    dummy = AdjacencyTree( -1 )
    #edges = [(1,2),(2,3),(3,4),(4,5),(5,6)]
    edges = [x for x in range(1,10)]
    ats = [AdjacencyTree(e) for e in edges]
    at = AdjacencyTree( 0 )
    for t in ats:
        at = BBTree.join(at,t,dummy)
    print("Before deletion")
    print("In-order: ")
    print(str(at.in_order()))


    #print("Inseting a node")

    print("Deleting a node...")
    print("After deletion")
    print("In-order: ")
    print(delete(ats[8],dummy).in_order())


if __name__ == "__main__":
    test1()
    print("Done")
