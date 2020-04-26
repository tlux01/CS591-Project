#don't touch
LEFT = 0
RIGHT = 1

# Balance Binary Tree Class
class AVLTree:

    def __init__(self):
        self.parent = None
        self.child = [None, None]
        self.height = 0


    def __repr__(self):
        return "|{}, h:{}, b:{}, parent:{}, children [{},{}]|".format(self.name, self.height, self.compute_balance_factor(),
                                                None if not self.parent else self.parent.name,
                                                None if not self.child[LEFT] else self.child[LEFT].name,
                                                None if not self.child[RIGHT] else self.child[RIGHT].name)

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
        # decrease heights of all parents
        aux = self.parent
        while aux:
            aux.height -= 1
            aux = aux.parent

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

    #this will be called in the weighted class
    def after_rot(self):
        pass

    # this will be called in the weighted class
    def init(self):
        pass

    def tallerChild(self):
        left_h = -1
        right_h = -1
        if self.child[LEFT]:
            left_h = self.child[LEFT].height
        if self.child[RIGHT]:
            right_h = self.child[RIGHT].height
        if right_h > left_h:
            return self.child[RIGHT]
        else:
            return self.child[LEFT]

    # this will be called in the weighted class
    def update_subtree_weight(self):
        pass

    # returns the in-order list of nodes
    def in_order(self):
        accum = [self]
        if self.child[LEFT]:
            accum = self.child[LEFT].in_order() + accum
        if self.child[RIGHT]:
            accum = accum + self.child[RIGHT].in_order()
        return accum

    def compute_balance_factor(self):
        right_h = -1 if not self.child[RIGHT] else self.child[RIGHT].height
        left_h = -1 if not self.child[LEFT] else self.child[LEFT].height

        return right_h - left_h

    def update_height(self):
        right_h = -1 if not self.child[RIGHT] else self.child[RIGHT].height
        left_h = -1 if not self.child[LEFT] else self.child[LEFT].height

        self.height = max(right_h, left_h) + 1

        aux = self.parent
        while aux:
            right_h = -1 if not aux.child[RIGHT] else aux.child[RIGHT].height
            left_h = -1 if not aux.child[LEFT] else aux.child[LEFT].height

            aux.height = max(right_h, left_h) + 1
            aux = aux.parent

def split(start_node, direction, dummy):
    #print("splitting")
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
        rotation_direction = RIGHT if p.child[LEFT] is dummy else LEFT
        #print(p)
        rotate(p, rotation_direction)


    t1 = dummy.child[LEFT]
    t2 = dummy.child[RIGHT]
    dummy.isolate()
    if t1:
        rebalance(t1)
        t1 = t1.find_root()

    if t2:
        rebalance(t2)
        t2 = t2.find_root()

    return t1, t2
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

def join(t1, t2, dummy):

    if not t1 or not t2:
        if t1:
            return t1
        elif t2:
            return t2
        else:
            return None
    dummy.init()

    if t1.height > t2.height + 1:
        joinRight(t1, t2, dummy)
    elif t2.height > t1.height + 1:
        joinLeft(t1, t2, dummy)
    else:

        dummy.child[LEFT] = t1
        dummy.child[RIGHT] = t2
        t1.parent = dummy
        t2.parent = dummy
        dummy.update_height()


    delete_dummy(dummy)

    return t1.find_root()

#delete node from the tree it belongs to
def delete_dummy(dummy):
    if not dummy.child[LEFT] and not dummy.child[RIGHT]:
        parent = dummy.parent
        dummy.isolate()
        parent.update_subtree_weight()
        parent.update_height()
        rebalance(parent)

    elif not dummy.child[LEFT]:
        parent = dummy.parent
        if parent.child[LEFT] is dummy:
            parent.child[LEFT] = dummy.child[RIGHT]
            if parent.child[LEFT]:
                parent.child[LEFT].parent = parent
        else:
            parent.child[RIGHT] = dummy.child[RIGHT]
            if parent.child[RIGHT]:
                parent.child[RIGHT].parent = parent
        dummy.child[RIGHT] = None
        dummy.child[LEFT] = None
        dummy.parent = None
        parent.update_subtree_weight()
        parent.update_height()
        rebalance(parent)

    elif not dummy.child[RIGHT]:
        parent = dummy.parent
        if parent.child[LEFT] is dummy:
            parent.child[LEFT] = dummy.child[LEFT]
            if parent.child[LEFT]:
                parent.child[LEFT].parent = parent
        else:
            parent.child[RIGHT] = dummy.child[LEFT]
            if parent.child[RIGHT]:
                parent.child[RIGHT].parent = parent
        dummy.child[RIGHT] = None
        dummy.child[LEFT] = None
        dummy.parent = None
        parent.update_subtree_weight()
        parent.update_height()
        rebalance(parent)
    else: # case where dummy has two children
        succ = dummy.successor()
        parent = succ.parent
        succ.child[LEFT] = dummy.child[LEFT]
        if succ.child[LEFT]:
            succ.child[LEFT].parent = succ

        if dummy.parent:
            if dummy.parent.child[RIGHT] is dummy:
                dummy.parent.child[RIGHT] = succ
            else:
                dummy.parent.child[LEFT] = succ
        succ.parent = dummy.parent

        if parent is not dummy:
            parent.child[LEFT] = succ.child[RIGHT]
            if parent.child[LEFT]:
                parent.child[LEFT].parent = parent

            succ.child[RIGHT] = dummy.child[RIGHT]
            if succ.child[RIGHT]:
                succ.child[RIGHT].parent = succ


        dummy.child[RIGHT] = None
        dummy.child[LEFT] = None
        dummy.parent = None
        succ.update_height()
        parent.update_height()
        parent.update_subtree_weight()
        succ.update_subtree_weight()
        rebalance(parent)


def rebalance(parent):
    while (parent):
        if abs(parent.compute_balance_factor()) > 1:
            x = parent
            y = x.tallerChild()
            z = y.tallerChild()
            parent = trinode_restructure(x,y,z)
        parent.update_subtree_weight()

        parent = parent.parent

def trinode_restructure(x,y,z):
    zLeft = (z is y.child[LEFT])
    yLeft = (y is x.child[LEFT])

    if zLeft and yLeft:
        rotate(x, RIGHT)
        return y
    elif not zLeft and yLeft:
        rotate(y, LEFT)
        rotate(x, RIGHT)
        return y
    elif zLeft and not yLeft:
        rotate(y, RIGHT)
        rotate(x, LEFT)
        return y
    else:
        rotate(x, LEFT)
        return y

def joinRight(t1, t2, dummy):
    t1_left = t1.child[LEFT]
    t1_right = t1.child[RIGHT]
    if height(t1_right) <= height(t2) + 1:
        dummy.child[LEFT] = t1_right
        dummy.child[RIGHT] = t2
        if t1_right:
            t1_right.parent = dummy
        t2.parent = dummy
        dummy.update_subtree_weight()
        dummy.update_height()
        if height(dummy) <= height(t1_left) + 1:
            t1.child[LEFT] = t1_left
            t1.child[RIGHT] = dummy
            if t1_left:
                t1_left.parent = t1
            dummy.parent = t1
            t1.update_height()
            t1.update_subtree_weight()
            return t1
        else:
            t_ = rotate(dummy, RIGHT)
            t1.child[LEFT] = t1_left
            t1.child[RIGHT] = t_
            if t1_left:
                t1_left.parent = t1
            t_.parent = t1

            t1.update_height()
            t1.update_subtree_weight()
            return rotate(t1, LEFT)
    else:
        t_ = joinRight(t1_right, t2, dummy)
        t1.child[LEFT] = t1_left
        t1.child[RIGHT] = t_
        if t1_left:
            t1_left.parent = t1
        t_.parent = t1
        t1.update_subtree_weight()
        t1.update_height()

        if height(t_) <= height(t1_left) + 1:
            return t1
        else:
            return rotate(t1, LEFT)

def joinLeft(t1, t2, dummy):
    t2_left = t2.child[LEFT]
    t2_right = t2.child[RIGHT]
    if height(t2_left) <= height(t1) + 1:
        dummy.child[LEFT] = t1
        dummy.child[RIGHT] = t2_left
        if t2_left:
            t2_left.parent = dummy
        t1.parent = dummy
        dummy.update_subtree_weight()
        dummy.update_height()
        if height(dummy) <= height(t2_right) + 1:
            t2.child[LEFT] = dummy
            t2.child[RIGHT] = t2_right
            if t2_right:
                t2_right.parent = t2
            dummy.parent = t2
            t2.update_subtree_weight()
            t2.update_height()
            return t2
        else:
            t_ = rotate(dummy, LEFT)
            t2.child[LEFT] = t_
            t2.child[RIGHT] = t2_right
            if t2_right:
                t2_right.parent = t2
            t_.parent = t2
            t2.update_subtree_weight()
            t2.update_height()
            return rotate(t2, RIGHT)
    else:
        t_ = joinLeft(t1, t2_left, dummy)
        t2.child[LEFT] = t_
        t2.child[RIGHT] = t2_right
        if t2_right:
            t2_right.parent = t2
        t_.parent = t2
        t2.update_subtree_weight()
        t2.update_height()
        if height(t_) <= height(t2_right) + 1:
            return t2
        else:
            return rotate(t2, RIGHT)



def rotate(r_parent, rotation_direction):

    r_child = r_parent.child[1 - rotation_direction]
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

    # update r_parent first as it is below r_child now, propagate weights up
    r_parent.update_height()
    r_child.update_height()



    # fix additional information in derived classes
    r_parent.after_rot()

    #this is new root
    return r_child

# compute height in O(1) time
def height(root):
    if not root:
        return -1
    r = -1
    l = -1
    if root.child[LEFT]:
        l = root.child[LEFT].height
    if root.child[RIGHT]:
        r = root.child[RIGHT].height
    return 1 + max(l, r)

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
