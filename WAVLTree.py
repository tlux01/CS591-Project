from AVLTree import AVLTree
import AVLTree as avl

#don't touch
LEFT = 0
RIGHT = 1

# Weighted Balance Binary Tree Class
class WAVLTree(AVLTree):

    def __init__(self, weight = 1):
        super().__init__()
        self.weight = weight
        self.sub_tree_weight = weight

    def __repr__(self):
        return "({}, {})".format(self.weight, self.sub_tree_weight)

    def set_weight(self,w):
        w_diff = w - self.weight
        self.weight = w
        self.sub_tree_weight += w_diff
        aux = self.parent
        while(aux):
            aux.sub_tree_weight += w_diff
            aux = aux.parent
    def add_weight(self, a):
        self.set_weight(self.weight+a)

    # these functions fix the weights
    def update_subtree_weight(self):
        self.sub_tree_weight = self.weight
        if self.child[LEFT]:
            self.sub_tree_weight += self.child[LEFT].sub_tree_weight
        if self.child[RIGHT]:
            self.sub_tree_weight += self.child[RIGHT].sub_tree_weight

    def after_rot(self):
        #print('After Rot')
        self.parent.sub_tree_weight = self.sub_tree_weight
        self.sub_tree_weight = self.weight
        left = self.child[LEFT]
        right = self.child[RIGHT]
        if left:
            self.sub_tree_weight += left.sub_tree_weight
        if right:
            self.sub_tree_weight += right.sub_tree_weight

    def init(self):
        self.sub_tree_weight = self.weight
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
        AVLTree.isolate(self)

    # recursively update subtree weights for all nodes in subtree of self
    def update_weights(self):
        self.sub_tree_weight = self.weight
        if self.child[LEFT]:
            self.child[LEFT].update_weights()
            self.sub_tree_weight += self.child[LEFT].sub_tree_weight
        if self.child[RIGHT]:
            self.child[RIGHT].update_weights()
            self.sub_tree_weight += self.child[RIGHT].sub_tree_weight

################### STATIC METHODS to operate on our WAVLTree #########################
def check_sub_tree_weights(root):
    if root.child[RIGHT] and root.child[LEFT]:
        r = root.sub_tree_weight == (root.weight + root.child[RIGHT].sub_tree_weight + root.child[LEFT].sub_tree_weight)
        return r and check_sub_tree_weights(root.child[LEFT]) and check_sub_tree_weights(root.child[RIGHT])
    elif root.child[LEFT]:
        r = root.sub_tree_weight == (root.weight + root.child[LEFT].sub_tree_weight)
        return r and check_sub_tree_weights(root.child[LEFT])
    elif root.child[RIGHT]:
        r = root.sub_tree_weight == (root.weight + root.child[RIGHT].sub_tree_weight)
        return r and check_sub_tree_weights(root.child[RIGHT])
    else:
        r = root.sub_tree_weight == root.weight
        return r
        
# return the node of tree t that corresponds to w wrt In-order
def locate(t, w):

    curr_node = t
    left = curr_node.child[LEFT]
    lower = left.sub_tree_weight if curr_node.child[LEFT] else 0
    upper = lower + curr_node.weight

    while (w <= lower or w > upper):
        #print("current node: {}. lower: {}. upper: {}".format(curr_node, lower, upper))
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
    return curr_node, w - lower
