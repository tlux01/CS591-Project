import random
from BBTree import BBTree
import BBTree as bbt

#don't touch
LEFT = 0
RIGHT = 1

# Weighted Balance Binary Tree Class
class WBBTree(BBTree):

    def __init__(self, weight = 1):
        super().__init__()
        self.weight = weight
        self.sub_tree_weight = weight

    def __repr__(self):
        return "(weight:{}, subtree weight:{})".format(self.weight, self.sub_tree_weight)
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

    # recursively update subtree weights for all nodes in subtree of self
    def update_weights(self):
        self.sub_tree_weight = self.weight
        if self.child[LEFT]:
            self.child[LEFT].update_weights()
            self.sub_tree_weight += self.child[LEFT].sub_tree_weight
        if self.child[RIGHT]:
            self.child[RIGHT].update_weights()
            self.sub_tree_weight += self.child[RIGHT].sub_tree_weight
################### STATIC METHODS to operate on our WBBTree #########################

# return the node of tree t that corresponds to w wrt In-order
def locate(t, w, offset):
    curr_node = t
    left = curr_node.child[LEFT]
    lower = left.sub_tree_weight if curr_node.child[LEFT] else 0
    upper = lower + curr_node.weight

    while (w <= lower or w > upper):
        print("current node: {}. lower: {}. upper: {}".format(curr_node, lower, upper))
        if (w <= lower):
            # proceed to the left child
            curr_node = curr_node.child[LEFT]
            lower -= curr_node.sub_tree_weight
            if (curr_node.child[LEFT]):
                lower += curr_node.child[LEFT].sub_tree_weight
            upper = lower + curr_node.weight
        else:
            # proceed to the right child
            curr_node = curr_node.child[RIGHT]
            lower = upper + curr_node.sub_tree_weight - curr_node.weight
            if (curr_node.child[RIGHT]):
                lower -= curr_node.child[RIGHT].sub_tree_weight
            upper = lower + curr_node.weight

    # in the paper they store w - lower in offset. Python has no such ability
    return curr_node, w - offset

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
    b0 = WBBNodeWithVal(0)
    b1 = WBBNodeWithVal(1)
    b2 = WBBNodeWithVal(2)
    b0.child[LEFT] = b1
    b1.parent = b0
    b0.child[RIGHT] = b2
    b2.parent = b0

    b3 = WBBNodeWithVal(3)
    b2.child[RIGHT] = b3
    b3.parent = b2

    b4 = WBBNodeWithVal(4)
    b2.child[LEFT] = b4
    b4.parent = b2
    print(b0.find_root())
    print(b4.find_root())

    w1 = b0.weight
    b0.set_weight(2)
    print("b0 had weight {} and now has weight {}".format(w1,b0.weight))
    print("The tree looks like:")
    print_tree(b0)
    print("In-order:")
    print(b0.in_order())


def test2():
    b0 = WBBNodeWithVal(0)
    b1 = WBBNodeWithVal(1)

    t = bbt.join(b0, b1, WBBTree())


    for i in range(2, 10):
        t = bbt.join(t, WBBNodeWithVal(i), WBBTree())

    print(bbt.height(t))
    print("Weight: "+str(t.weight)+". Subtree weight: "+str(t.sub_tree_weight))

    print("The tree looks like:")
    print_tree(t)

    print("In-order:")
    print(t.in_order())
    w = 4.5
    print("Locating node corresponding to weight {}:".format(w))
    print(locate(b0,w))


def test3():
    b0 = WBBNodeWithVal(0)
    b0.weight = 2
    b1 = WBBNodeWithVal(1)
    b2 = WBBNodeWithVal(2)
    b0.child[LEFT] = b1
    b1.parent = b0
    b0.child[RIGHT] = b2
    b2.parent = b0

    b3 = WBBNodeWithVal(3)
    b2.child[RIGHT] = b3
    b3.parent = b2

    b4 = WBBNodeWithVal(4)
    b2.child[LEFT] = b4
    b4.parent = b2

    b0.update_weights()

    print("In-order:")
    print(b0.in_order())

    w = 4.5
    print("Locating weight "+str(w))
    print(locate(b0,w))

def test4():
    b0 = WBBTree(20)
    b1 = WBBTree(10)
    t = bbt.join(b0, b1, WBBTree())
    t = bbt.join(t, WBBTree(), WBBTree())
    t = bbt.join(t, WBBTree(12), WBBTree())
    t = bbt.join(t, WBBTree(2), WBBTree())
    print_tree(t)
    print(t.in_order())
    print(locate(t, 32))
if __name__ == "__main__":
    test4()
    print("Done")
