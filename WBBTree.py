import random
from BBTree import BBTree
import BBTree as bbt

#don't touch
LEFT = 0
RIGHT = 1

# Weighted Balance Binary Tree Class
class WBBTree(BBTree):

    def __init__(self, weight = 1, subTreeWeight = 1):
        super().__init__()
        self.weight = weight
        self.sub_tree_weight = subTreeWeight

    def set_weight(self,w):
        w_diff = w - self.weight
        self.weight = w
        self.sub_tree_weight += w_diff
        aux = self.parent
        while(aux):
            aux.sub_tree_weight += w_diff
            aux = aux.parent
    def add_weight(a):
        self.set_weight(self.weight+a)
    # these functions fix the weights
    def after_rot(self):
        self.parent.sub_tree_weight = self.sub_tree_weight
        self.sub_tree_weight = self.weight
        left = self.child[LEFT]
        right = self.child[RIGHT]
        if left:
            self.sub_tree_weight += left.sub_tree_weight
        if right:
            self.sub_tree_weight += right.sub_tree_weight
    def init(self):
        sub_tree_weight = self.weight
        left = self.child[LEFT]
        right = self.child[RIGHT]
        if left:
            self.sub_tree_weight += left.sub_tree_weight
        if right:
            self.sub_tree_weight += right.sub_tree_weight
    def isolate(self):
        aux = self.parent
        while(aux):
            aux.sub_tree_weight -= self.sub_tree_weight
            aux = aux.parent
        BBTree.isolate(self)

    # rerturn the node of tree t that corresponds to w wrt In-order
    def locate(t,w):


################### STATIC METHODS to operate on our WBBTree #########################
def print_tree(root):
    h = bbt.height(root)
    for i in range(1,  h+ 1):
        _print_tree(root, i)
        print("")

def _print_tree(root, level):
    if not root:
        return root
    if level == 1:
        print(root, end = ' ')
    elif level > 1:
        _print_tree(root.child[LEFT], level - 1)
        _print_tree(root.child[RIGHT], level - 1)

#Test Inheritance of WBBNode

class WBBNodeWithVal(WBBTree):
    def __init__(self, val):
        super().__init__()
        self.val = val
    def __repr__(self):
        return "(" + str(self.val) + ", " + str(self.weight) + ", " + str(self.priority)[:5] + ")"


################### Test ###################################################
def test1():
    b0 = WBBNodeWithVal(1)
    b1 = WBBNodeWithVal(2)
    b2 = WBBNodeWithVal(10)
    b0.child[LEFT] = b1
    b1.parent = b0
    b0.child[RIGHT] = b2
    b2.parent = b0

    b3 = WBBNodeWithVal(11)
    b2.child[RIGHT] = b3
    b3.parent = b2

    b4 = WBBNodeWithVal(12)
    b2.child[LEFT] = b4
    b4.parent = b2
    print(b0.find_root()) #expect 1
    print(b4.find_root()) #expect 1

    w1 = b0.weight
    b0.set_weight(2)
    print("b0 had weight {} and now has weight {}".format(w1,b0.weight))
    print("The tree looks like:")
    print_tree(b0)

def test2():
    b0 = WBBNodeWithVal(0)
    b1 = WBBNodeWithVal(1)

    t = bbt.join(b0, b1, WBBTree())


    for i in range(2, 10000):
        t = bbt.join(t, WBBNodeWithVal(i), WBBTree())

    print(bbt.height(t))
    print("Weight: "+str(t.weight)+". Subtree weight: "+str(t.sub_tree_weight))

if __name__ == "__main__":
    test1()
    print("Done")
