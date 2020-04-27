from WRBBTree import WRBBTree
import RBBTree as rbbt

#don't touch
LEFT = 0
RIGHT = 1

class AdjacencyRBBTree(WRBBTree):

    # (a,b) is the edge
    def __init__(self, e, weight = 1):
        '''e is an edge, probably represented by a pair of nodes like (node1, node2)'''
        super().__init__(weight)
        self.edge = e

    def __repr__(self):
        return "{}".format(self.edge)


######################### Static Methods fo AdjacencyTree #############################
def adj_insert(adt, e, dummy):
    '''return self with inserted edge (a,b)'''
    aux = AdjacencyRBBTree(e)
    # if adt is None, join handles this by returning aux
    rbbt.join(adt,aux,dummy)
    return aux

def adj_delete(adj_t, node, dummy):
    '''deletes node from adj_t'''

    t1, t2 = rbbt.split(node, LEFT, dummy)

    t3, t2 = rbbt.split(node, RIGHT, dummy)

    node.isolate()

    adj_t = rbbt.join(t1,t2,dummy)
    # this return is there to protect from weird behavior when node and adj_t are the same
    # make sure to set new value of adj_t to be the result of this delete
    return adj_t
