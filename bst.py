import json
from typing import List
from collections import deque

# DO NOT MODIFY THIS CLASS!
class Node():
    def  __init__(self,
                  key        = None,
                  keycount   = None,
                  leftchild  = None,
                  rightchild = None):
        self.key        = key
        self.keycount   = keycount
        self.leftchild  = leftchild
        self.rightchild = rightchild

# DO NOT MODIFY THIS FUNCTION!
# For the tree rooted at root, dump the tree to stringified JSON object and return.
# NOTE: in future projects you'll need to write the dump code yourself,
# but here it's given to you.
def dump(root: Node) -> str:
    def _to_dict(node) -> dict:
        return {
            "key": node.key,
            "keycount": node.keycount,
            "leftchild": (_to_dict(node.leftchild) if node.leftchild is not None else None),
            "rightchild": (_to_dict(node.rightchild) if node.rightchild is not None else None)
        }
    if root == None:
        dict_repr = {}
    else:
        dict_repr = _to_dict(root)
    return json.dumps(dict_repr,indent = 2)

#---------------------------------------------------------------------------------------------------

# For the tree rooted at root and the key given:
# If the key is not in the tree, insert it with a keycount of 1.
# If the key is in the tree, increment its keycount.
def insert(root: Node, key: int) -> Node:
    if root is None :
        return Node(key, 1)

    if key < root.key:
        root.leftchild = insert(root.leftchild, key)
    elif key > root.key:
        root.rightchild = insert(root.rightchild, key)
    elif key == root.key:
        root.keycount += 1

    return root

# For the tree rooted at root and the key given:
# If the key is not in the tree, do nothing.
# If the key is in the tree, decrement its key count. If they keycount goes to 0, remove the key.
# When replacement is necessary use the inorder successor.
def delete(root: Node, key: int) -> Node:
    if root is None :
        return

    if key < root.key:
        root.leftchild = delete(root.leftchild, key)
    elif key > root.key:
        root.rightchild = delete(root.rightchild, key)
    elif key == root.key:
        root.keycount -= 1
        if root.keycount < 1 :
            if root.leftchild is None:
                return root.rightchild
            elif root.rightchild is None:
                return root.leftchild

            successor = root.rightchild
            while successor.leftchild is not None:
                successor = successor.leftchild
            root.key = successor.key
            root.keycount = successor.keycount
            successor.keycount = 1
            root.rightchild = delete(root.rightchild, successor.key)
            return root

    return root

# For the tree rooted at root and the key given:
# Calculate the list of keys on the path from the root towards the search key.
# The key is not guaranteed to be in the tree.
# Return the json.dumps of the list with indent=2.
def search(root: Node, search_key: int) -> str:
    path = [] 
    current = root 
    
    while current is not None:
        path.append(current.key) 
        
        if search_key < current.key:
            current = current.leftchild 
        elif search_key > current.key:
            current = current.rightchild 
        else:
            break  # Found the search key, exit the loop

    return json.dumps(path, indent=2)

# For the tree rooted at root, find the preorder traversal.
# Return the json.dumps of the list with indent=2.
def preorder(root: Node) -> str:
    def _preorder_traversal(node):
        if node is None:
            return []
        traversal = [node.key]
        traversal.extend(_preorder_traversal(node.leftchild))  
        traversal.extend(_preorder_traversal(node.rightchild))  
        return traversal

    result = _preorder_traversal(root)  # Perform the preorder traversal
    return json.dumps(result, indent=2)

# For the tree rooted at root, find the inorder traversal.
# Return the json.dumps of the list with indent=2.
def inorder(root: Node) -> str:
    def _inorder_traversal(node):
        if node is None:
            return []
        traversal = _inorder_traversal(node.leftchild)
        traversal.extend([node.key])
        traversal.extend(_inorder_traversal(node.rightchild)) 
        return traversal

    result = _inorder_traversal(root) 
    return json.dumps(result, indent=2)

# For the tree rooted at root, find the postorder traversal.
# Return the json.dumps of the list with indent=2.
def postorder(root: Node) -> str:
    def _postorder_traversal(node):
        if node is None:
            return []
        traversal = _postorder_traversal(node.leftchild)
        traversal.extend(_postorder_traversal(node.rightchild))
        traversal.extend([node.key])
        return traversal

    result = _postorder_traversal(root) 
    return json.dumps(result, indent=2)

# For the tree rooted at root, find the BFT traversal (go left-to-right).
# Return the json.dumps of the list with indent=2.
def bft(root: Node) -> str:
    if root is None:
        return json.dumps([], indent=2)

    result = [] 
    queue = deque()
    queue.append(root) 

    while queue:
        node = queue.popleft()
        result.append(node.key) 

        if node.leftchild:
            queue.append(node.leftchild)

        if node.rightchild:
            queue.append(node.rightchild)

    return json.dumps(result, indent=2)
