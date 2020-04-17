from WBBTree import WBBTree
import BBTree
import random

#random.seed(10)
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

######################### Static Methods fo AdjacencyTree #############################
def adj_insert(adt, e, dummy):
    '''return self with inserted edge (a,b)'''
    aux = AdjacencyTree(e)
    # if adt is None, join handles this by returning aux
    return BBTree.join(adt,aux,dummy)

def adj_delete(adt, dummy):
    '''delete the self node'''

    t1, t2 = BBTree.split(adt, BBTree.LEFT, dummy)

    t3, t2 = BBTree.split(adt, BBTree.RIGHT, dummy)
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
    print(delete(ats[4],dummy).in_order())


def test2():
    dummy = AdjacencyTree( -1 )
    #edges = [(1,2),(2,3),(3,4),(4,5),(5,6)]
    edges = [x for x in range(1,10)]
    ats = [AdjacencyTree(e) for e in edges]
    at = AdjacencyTree( 0 )
    for e in edges:
        at = at.insert(e,dummy)
    print("In-order: ")
    print(at.in_order())
    print()


if __name__ == "__main__":
    test2()
    print("Done")
