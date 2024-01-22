import json
from typing import List

# DO NOT MODIFY!
class Node():
    def  __init__(self,
                  key       : int,
                  word      : str,
                  leftchild,
                  rightchild):
        self.key        = key
        self.word      = word
        self.leftchild  = leftchild
        self.rightchild = rightchild

# DO NOT MODIFY!
def dump(root: Node) -> str:
    def _to_dict(node) -> dict:
        return {
            "key": node.key,
            "word": node.word,
            "l": (_to_dict(node.leftchild) if node.leftchild is not None else None),
            "r": (_to_dict(node.rightchild) if node.rightchild is not None else None)
        }
    if root == None:
        dict_repr = {}
    else:
        dict_repr = _to_dict(root)
    return json.dumps(dict_repr,indent = 2)

#Helper function that returns the height of a node... 0 if dne otherwise the max of the either child's height + 1
#If a child DNE then it would return 0 and thus height of a leaf node is 1
def height(node: Node) -> int:
    if node is None:
        return 0
    return 1 + max(height(node.leftchild), height(node.rightchild))

#Helper function to safely return the difference in height between a node's two children
def balance_factor(node :Node) -> int:
    if node is None:
        return 0
    return height(node.rightchild) - height(node.leftchild)
#Helper function to safely determine if a None, leaf, or other node is balanced
def balanced(node :Node) -> bool:
    if abs(balance_factor(node)) <= 1:
        return True
    return False
#Left and Right rotations from teh lecture slies
def right_rotate(y):
    x = y.leftchild
    B = x.rightchild

    x.rightchild = y
    y.leftchild = B

    return x
def left_rotate(y):
    z = y.rightchild
    C = z.leftchild

    z.leftchild = y
    y.rightchild = C

    return z

# insert
# For the tree rooted at root, insert the given key,word pair and then balance as per AVL trees.
# The key is guaranteed to not be in the tree.
# Return the root.
def bst_insert(root: Node, key: int, word:str) -> Node:
    if root is None:
        return Node(key, word, None, None)
    if key < root.key:
        root.leftchild = bst_insert(root.leftchild, key, word)
    else:
        root.rightchild = bst_insert(root.rightchild, key, word)
    return root

def insert(root: Node, key: int, word: str) -> Node:
    if root is None:
        return Node(key, word, None, None)
    if key < root.key:
        root.leftchild = insert(root.leftchild, key, word)
    else:
        root.rightchild = insert(root.rightchild, key, word)

    balance = balance_factor(root)
    if balance > 1: #Right Heavy
        if balance_factor(root.rightchild) > 0: #right-right heavy
            return left_rotate(root)
        else: #Right - left heavy
            root.rightchild = right_rotate(root.rightchild)
            return left_rotate(root)
    if balance < -1: #Left Heavy
        if balance_factor(root.leftchild) < 0: #Left-Left Heavy
            return right_rotate(root)
        else: #Left-Right Heavy
            root.leftchild = left_rotate(root.leftchild)
            return right_rotate(root)
    return root

def preorder(root: Node, acc = []) -> List:
    if root == None:
        return acc
    
    acc.append(root.key)
    acc.append(root.word)

    acc = preorder(root.leftchild, acc)
    acc = preorder(root.rightchild, acc)

    return acc

# bulkInsert
# The parameter items should be a list of pairs of the form [key,word] where key is an integer and word is a string.
# For the tree rooted at root, first insert all of the [key,word] pairs as if the tree were a standard BST, with no balancing.
# Then do a preorder traversal of the [key,word] pairs and use this traversal to build a new tree using AVL insertion.
# Return the root
def bulkInsert(root: Node, items: List) -> Node:
    while len(items) != 0:
        pair = items.pop(0)
        word = pair[1]
        key = int(pair[0])
        root = bst_insert(root, key, word)
    
    order = preorder(root)
    root = None

    while len(order) != 0:
        word = order.pop(1)
        key = order.pop(0)
        root = insert(root, key, word)

    return root

# bulkDelete
# The parameter keys should be a list of keys.
# For the tree rooted at root, first tag all the corresponding nodes (however you like),
# Then do a preorder traversal of the [key,word] pairs, ignoring the tagged nodes,
# and use this traversal to build a new tree using AVL insertion.
# Return the root.
def bulkDelete(root: Node, keys: List[int]) -> Node:
    # Keys should be unique so there is no need to tage them in their nodes
    order = preorder(root)
    #for each key, remove it from the preorder traversal which is pairs of [key,node]
    while len(keys) != 0:
        key = keys.pop()
        i = order.index(key)
        order.pop(i+1)
        order.pop(i)
    #start with an empty tree
    root = None
    #insert each key word from the inorder traversal in the AVL insertion method
    while len(order) != 0:
        word = order.pop(1)
        key = order.pop(0)
        root = insert(root, key, word)

    return root

# search
# For the tree rooted at root, calculate the list of keys on the path from the root to the search_key,
# including the search key, and the word associated with the search_key.
# Return the json stringified list [key1,key2,...,keylast,word] with indent=2.
# If the search_key is not in the tree return a word of None.
def search(root: Node, search_key: int) -> str:
    node = root
    acc = []

    while node:
        key = node.key
        acc.append(key)

        if key == search_key:
            return json.dumps(acc + [node.word], indent=2)

        if search_key < key:
            node = node.leftchild
        else:
            node = node.rightchild

    # If the loop terminates without finding the search_key, return a word of None.
    return json.dumps(["None"], indent=2)

# replace
# For the tree rooted at root, replace the word corresponding to the key search_key by replacement_word.
# The search_key is guaranteed to be in the tree.
# Return the root
def replace(root: Node, search_key: int, replacement_word:str) -> None:
    node = root
    acc = []

    while node:
        key = node.key
        acc.append(key)

        if key == search_key:
            node.word = replacement_word
            break
        if search_key < key:
            node = node.leftchild
        else:
            node = node.rightchild

    return root