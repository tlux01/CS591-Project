import random

#don't touch
LEFT = 0
RIGHT = 1

# Balance Binary Tree Class
class BBTree:

    def __init__(self):
        self.parent = None
        self.child = [None, None]
        # priority used in balancing tree
        self.priority = random.random()

    # starting at this node, walk down as far left
    def first(self):
        leftMost = None
        #current node in traversal
        cur = self
        while cur.child[LEFT] != None:
            cur = cur.child[LEFT]
            leftMost = cur
        return leftMost

    # starting at this node, walk down as far right
    def last(self):
        rightMost = None
        #current node in traversal
        cur = self
        while cur.child[RIGHT] != None:
            cur = cur.child[RIGHT]
            rightMost = cur
        return rightMost

    # follow parent up the tree as long as possible
    def find_root(self):
        root = self
        while root.parent != None:
            root = root.parent
        return root

    #isolates this node, takes care of child and parent pointers
    def isolate(self):
        # false if no parent
        # isolate from parent
        if self.parent:
            if self.parent.child[LEFT] is self:
                self.parent.child[LEFT] = None
            else:
                self.parent.child[RIGHT] = None

        # Isolate from children
        if self.child[LEFT]:
            self.child[LEFT].parent = None
        if self.child[RIGHT]:
            self.child[RIGHT].parent = None




################### STATIC METHODS to operate on our BBTREE #########################
# rotate a tree for balancing
# rotate depends if child is left or right child of parent
def rotate(r_child, r_parent):
    rotation_direction = RIGHT if r_parent.child[LEFT] is r_child else LEFT

    mid_tree = r_child.child[rotation_direction]

    # move mid tree to opposite side of child of parent
    r_parent.child[1 - rotation_direction] = mid_tree

    # assign child the parent of its parent

    r_child.parent = r_parent.parent

    # update this new parent to replace its child which was
    # r_parent to be r_child
    if r_child.parent:
        if (r_child.parent.child[LEFT] is r_parent):
            r_child.parent.child[LEFT] = r_child
        else:
            r_child.parent.child[RIGHT] = r_child

    # rotate parent to be child of child in direction
    r_child.child[rotation_direction] = r_parent
    r_parent.parent = r_child

#Test Inheritance of BBNode

class BBNodeWithVal(BBTree):
    def __init__(self, val):
        super().__init__()
        self.val = val
    def __repr__(self):
        return str(self.val)




################### Test ###################################################
def test1():
    b0 = BBNodeWithVal(1)
    b1 = BBNodeWithVal(2)
    b2 = BBNodeWithVal(10)
    b0.child[LEFT] = b1
    b1.parent = b0
    b0.child[RIGHT] = b2
    b2.parent = b0

    b3 = BBNodeWithVal(11)
    b2.child[RIGHT] = b3
    b3.parent = b2

    b4 = BBNodeWithVal(12)
    b2.child[LEFT] = b4
    b4.parent = b2
    print(b0.find_root())

if __name__ == "__main__":
    test1()
    print("Done")
