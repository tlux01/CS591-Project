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
        #current node in traversal
        cur = self
        while cur.child[LEFT]:
            cur = cur.child[LEFT]

        return cur

    # starting at this node, walk down as far right
    def last(self):
        #current node in traversal
        cur = self
        while cur.child[RIGHT]:
            cur = cur.child[RIGHT]

        return cur

    # follow parent up the tree as long as possible
    def find_root(self):
        root = self
        while root.parent:
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

        # remove children
        self.child
    # find successor in InOrder Traversal of InOrder
    # returns this node if exists, None otherwise
    def successor(self):

        sub_successor = None
        # if there is a right sub tree
        if self.child[RIGHT]:
            # go into right sub tree

            cur = self.child[RIGHT]
            sub_successor = cur
            # then go left as far as possible as this will be successor
            while cur:
                sub_successor = cur
                cur = cur.child[LEFT]

        # if no sub_successor, need to go up through parent and check if successor exists there
        # otherwise return this sub_successor
        if sub_successor:
            return sub_successor
        else:
            # check if parent exists
            if self.parent:
                # if it is the left child
                if self is self.parent.child[LEFT]:
                    #successor in Inorder traversal is then the parent
                    return self.parent
                # is right child
                else:
                    cur = self.parent
                    while cur and cur.parent:
                        # keep going up to parent until we find
                        # that our parent is a left node, return the parent of this parent
                        if cur is cur.parent.child[LEFT]:
                            return cur.parent
                        cur = cur.parent

            # if we get here we return None
            return None

    # find predecessor in InOrder Traversal of InOrder
    # returns this node if exists, None otherwise
    def predecessor(self):
        sub_predecessor = None
        # if there is a left sub tree
        if self.child[LEFT]:
            # go into left sub tree

            cur = self.child[LEFT]
            sub_predecessor = cur

            # then go right as far as possible as this will be successor
            while cur:
                sub_predecessor = cur
                cur = cur.child[RIGHT]
        # if no sub_predecessor, need to go up through parent and check if predecessor exists there
        # otherwise return this sub_predecessor
        if sub_predecessor:
            return sub_predecessor
        else:
            # check if parent exists
            if self.parent:
                # if it is the right child
                if self is self.parent.child[RIGHT]:
                    #predecessor in Inorder traversal is then the parent
                    return self.parent
                # is left child
                else:
                    cur = self.parent
                    # check if there is parent
                    while cur and cur.parent:
                        # keep going up to parent until we find
                        # that our parent is a right node, return the parent of this parent
                        if cur is cur.parent.child[RIGHT]:
                            return cur.parent
                        cur = cur.parent

            # if we get here we return None
            return None

    def cyclic_pred(self):
        c_pred = self.last() if self is self.first() else self.predecessor()
        return c_pred

    def cyclic_succ(self):
        c_succ = self.first() if self is self.last() else self.successor()
        return c_succ

    def after_rot(self):
        pass
    def init(self):
        pass

    # returns the in-order list of nodes
    def in_order(self):
        accum = [self]
        if self.child[LEFT]:
            accum = self.child[LEFT].in_order() + accum
        if self.child[RIGHT]:
            accum = accum + self.child[RIGHT].in_order()
        return accum

    def makeChild(self,whichOne,child):
        child.parent = self
        self.child[whichOne] = child
################### STATIC METHODS to operate on our BBTREE #########################
# rotate a tree for balancing, does not change InOrder traversal of tree
# rotate depends if child is left or right child of parent
def rotate(r_child, r_parent):
    rotation_direction = RIGHT if r_parent.child[LEFT] is r_child else LEFT

    mid_tree = r_child.child[rotation_direction]

    # move mid tree to opposite side of child of parent
    r_parent.child[1 - rotation_direction] = mid_tree


    if mid_tree:
        mid_tree.parent = r_parent
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

    # fix additional information in derived classes
    r_parent.after_rot()

# returns true if node u is before v in the InOrder traversal, false otherwise
def smaller(u, v):
    # if u or v = None
    if not u or not v:
        return False

    # if they are the same also return false
    if u is v:
        return False

    # get height of u
    height_u = 0
    cur_u = u
    while cur_u.parent:
        height_u += 1
        cur_u = cur_u.parent

    # get height of v
    height_v = 0
    cur_v = v
    while cur_v.parent:
        height_v += 1
        cur_v = cur_v.parent

    #case where they have different root, then we can't determine smaller
    if cur_u is not cur_v:
        return False

    # paths from root
    u_path = []
    v_path = []

    # construct paths in term of Lefts and Rights from root
    cur_u = u

    while cur_u.parent:
        if cur_u.parent.child[LEFT] is cur_u:
            #build path bottom up, first index will be path starting from root
            u_path = [LEFT] + u_path
        else:
            u_path = [RIGHT] + u_path
        cur_u = cur_u.parent

    cur_v = v

    while cur_v.parent:
        if cur_v.parent.child[LEFT] is cur_v:
            #build path bottom up, first index will be path starting from root
            v_path = [LEFT] + v_path
        else:
            v_path = [RIGHT] + v_path
        cur_v = cur_v.parent

    #we compare paths such that the one that is most left is the one that will be before in Inorder
    i = 0
    # we find index of first difference in paths
    while i < height_u and i < height_v:
        if u_path[i] != v_path[i]:
            break
        i += 1
    # if we have not reached end of path u, and step at i is LEFT for u, then u is more left than v
    if i < height_u and u_path[i] == LEFT:
        return True
    # if we have not reach end of path v, and step at i is RIGHT for v, v is more right than u
    elif i < height_v and v_path[i] == RIGHT:
        return True
    else:
        return False

# join two trees with the correct InOrder based on their priority
def join(t1, t2, dummy):
    if not t1 or not t2:
        if t1:
            return t1
        elif t2:
            return t2
        else:
            return None

    # make dummy the root of both trees
    dummy.parent = None
    dummy.child[LEFT] = t1
    dummy.child[RIGHT] = t2

    t1.parent = dummy
    t2.parent = dummy
    #fix info for derived classes
    dummy.init()

    # rotate dummy down until it is a leaf
    while dummy.child[LEFT] or dummy.child[RIGHT]:
        # to preserve in order we rotate with the node down
        larger = None
        left = dummy.child[LEFT]
        right = dummy.child[RIGHT]
        # check if right child exists
        if right:
            # check that left child exists
            if left:
                if right.priority > left.priority:
                    larger = right
                else:
                    larger = left
            else:
                larger = right
        # no right child so default to left
        else:
            larger = left

        # Now that we have found larger child, we rotate it with dummy
        rotate(larger, dummy)

    # remove dummy from tree
    dummy.isolate()

    #if t1, which is root of t1, does have parent then t2 is the root
    if t1.parent:
        return t2
    else:
        return t1

#starting at our start_node, return two trees either split starting from the LEFT or RIGHT of this node
def split(start_node, direction, dummy):
    if not start_node:
        t1 = None
        t2 = None
        return t1, t2

    dummy.child[LEFT] = None
    dummy.child[RIGHT] = None


    # we want to add dummy node in manner where we don't cut off and part
    # of the tree, and maintains InOrder of our tree, rotating dummy up until it
    # replaces our root, where we then can isolate dummy creating two split
    # trees


    # split after our start node, t1 contains start node
    if(direction == RIGHT):
        sub_successor = None
        if start_node.child[RIGHT]:
            cur = start_node.child[RIGHT]
            sub_successor = cur
            while cur:
                sub_successor = cur
                cur = cur.child[LEFT]

        if not sub_successor:
            #None to right of start node, so replace with dummy
            start_node.child[RIGHT] = dummy
            dummy.parent = start_node
        else:
            # store dummy as left child of subtree successor which is immediately after our start node
            # as this is always None, sub_successor does not have a right child by def
            sub_successor.child[LEFT] = dummy
            dummy.parent = sub_successor

    # split before our start node, t1 does not contain start node
    else:
        sub_predecessor = None
        if start_node.child[LEFT]:
            cur = start_node.child[LEFT]
            sub_predecessor = cur
            while cur:
                sub_predecessor = cur
                cur = cur.child[RIGHT]

        if not sub_predecessor:
            # None at left child so replace that with dummy
            start_node.child[LEFT] = dummy
            dummy.parent = start_node
        else:
            # store dummy as right child of subtree predecessor which is immediately before our start node
            # as this is always None, sub_predecessor does not have a right child by def
            sub_predecessor.child[RIGHT] = dummy
            dummy.parent = sub_predecessor

    # for derived classes
    dummy.init()
    #rotate dummy until it becomes root

    while dummy.parent:

        p = dummy.parent
        #print(p)
        rotate(dummy, p)


    t1 = dummy.child[LEFT]
    t2 = dummy.child[RIGHT]


    dummy.isolate()

    return t1, t2

# for level order traversal
def height(root):
    if not root:
        return 0

    return 1 + max(height(root.child[LEFT]), height(root.child[RIGHT]))

# levelorder traversal from root
def print_tree(root):
    h = height(root)
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


########################################################################################


#Test Inheritance of BBNode
class BBNodeWithVal(BBTree):
    def __init__(self, val):
        super().__init__()
        self.val = val
    def __repr__(self):
        return "(" + str(self.val) + ", " + str(self.priority)[:5] + ")"




################### Test ###################################################
def test1():
    b0 = BBNodeWithVal(0)
    b1 = BBNodeWithVal(1)
    b2 = BBNodeWithVal(2)
    b0.child[LEFT] = b1
    b1.parent = b0
    b0.child[RIGHT] = b2
    b2.parent = b0

    b3 = BBNodeWithVal(3)
    b2.child[RIGHT] = b3
    b3.parent = b2

    b4 = BBNodeWithVal(4)
    b2.child[LEFT] = b4
    b4.parent = b2

    b5 = BBNodeWithVal(5)
    b1.child[LEFT] = b5
    b5.parent = b1

    b6 = BBNodeWithVal(6)
    b1.child[RIGHT] = b6
    b6.parent = b1
    #print(b0.find_root())
    #print(b0.last())
    # print_tree(b0)
    # print(b5.successor())
    # print(b2.predecessor())
    #
    #
    # a = BBTree()
    # height_v = 0
    # cur_v = b0
    # while cur_v.parent:
    #     height_v += 1
    #     cur_v = cur_v.parent
    # print(height_v)
    #
    # cur_u = b0
    # u_path = []
    # while cur_u.parent:
    #     if cur_u.parent.child[LEFT] is cur_u:
    #         #build path bottom up, first index will be path starting from root
    #         u_path = [LEFT] + u_path
    #     else:
    #         u_path = [RIGHT] + u_path
    #     cur_u = cur_u.parent
    # print(u_path)
    #
    # print(smaller(b2,b3))
    print("In-order before split: ")
    print(str(b0.in_order()))
    print("Tree before split: ")
    print(str(print_tree(b0)))

    t1, t2 = split(b0, RIGHT, BBTree())

    print("In-order of left tree: ")
    print(str(t1.in_order()))
    print_tree(t1)
    print("In-order of right tree: ")
    print(str(t2.in_order()))
    print_tree(t2)

    print("Is the tree preserved after the split?")
    print("In-order: ")
    print(str(b0.in_order()))
    print("Tree after split: ")
    print(str(print_tree(b0)))

def test2():
    b0 = BBNodeWithVal(0)
    b1 = BBNodeWithVal(1)

    t = (b0, b1, BBTree())


    for i in range(2, 100000):
        t = join(t, BBNodeWithVal(i), BBTree())

    print(height(t))
    #print_tree(t)

def test3():
    b0 = BBNodeWithVal(0)
    b1 = BBNodeWithVal(1)
    b2 = BBNodeWithVal(2)
    b0.child[LEFT] = b1
    b1.parent = b0
    b1.child[LEFT] = b2
    b2.parent = b1
    b0.isolate()
    print(b1.parent)

if __name__ == "__main__":
    test3()
    print("Done")
