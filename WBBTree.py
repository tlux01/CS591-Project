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

    def get_weight(self):
        return self.weight
    def get_subtree_weight(self):
        return self.sub_tree_weight
    def set_weight(self,w):
        self.weight = w
    def add_weight(a):
        self.set_weight(weight+a)
    def after_rot(self):
        self.parent.sub_tree_weight = self.sub_tree_weight
        self.sub_tree_weight = self.weight
        left = self.child[LEFT]
        right = self.child[RIGHT]
        if left:
            self.sub_tree_weight += left.sub_tree_weight
        if right:
            self.sub_tree_weight += right.sub_tree_weight

################### STATIC METHODS to operate on our WBBTREE #########################


#Test Inheritance of WBBNode

class WBBNodeWithVal(WBBTree):
    def __init__(self, val):
        super().__init__()
        self.val = val
    def __repr__(self):
        return "Val: "+str(self.val)+". Weight: "+str(self.weight)


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

    w1 = b0.get_weight()
    b0.set_weight(2)
    print("b0 had weight {} and now has weight {}".format(w1,b0.get_weight()))

def test2():
    b0 = WBBNodeWithVal(0)
    b1 = WBBNodeWithVal(1)

    t = bbt.join(b0, b1, WBBTree())


    for i in range(2, 10000):
        t = bbt.join(t, WBBNodeWithVal(i), WBBTree())

    print(bbt.height(t))
    print("Weight: "+str(t.get_weight())+". Subtree weight: "+str(t.get_subtree_weight()))

if __name__ == "__main__":
    test2()
    print("Done")
