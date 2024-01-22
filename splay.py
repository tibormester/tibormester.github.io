from __future__ import annotations
import json
from typing import List

verbose = False

# DO NOT MODIFY!
class Node():
    def  __init__(self,
                  key       : int,
                  leftchild  = None,
                  rightchild = None,
                  parent     = None,):
        self.key        = key
        self.leftchild  = leftchild
        self.rightchild = rightchild
        self.parent     = parent

# DO NOT MODIFY!
class SplayTree():
    def  __init__(self,
                  root : Node = None):
        self.root = root

    # For the tree rooted at root:
    # Return the json.dumps of the object with indent=2.
    # DO NOT MODIFY!
    def dump(self) -> str:
        def _to_dict(node) -> dict:
            pk = None
            if node.parent is not None:
                pk = node.parent.key
            return {
                "key": node.key,
                "left": (_to_dict(node.leftchild) if node.leftchild is not None else None),
                "right": (_to_dict(node.rightchild) if node.rightchild is not None else None),
                "parentkey": pk
            }
        if self.root == None:
            dict_repr = {}
        else:
            dict_repr = _to_dict(self.root)
        return json.dumps(dict_repr,indent = 2)

    def search(self, key: int):
        y = self.bst(self.root, key)
        self.splay(self.root, y)
        #return self.root.key if self.root and self.root.key == key else None

    def insert(self, key: int):
        if self.root is None:
            self.root = Node(key)
        else:
            y =  self.bst(self.root, key)
            if y is None:
                return self.root
            self.root = self.splay(self.root, y)

            new_node = Node(key)

            if key < self.root.key:
                new_node.leftchild = self.root.leftchild
                if new_node.leftchild is not None:
                    new_node.leftchild.parent = new_node
                new_node.rightchild = self.root
                self.root.leftchild = None

            elif key > self.root.key:
                new_node.rightchild = self.root.rightchild
                if new_node.rightchild is not None:
                    new_node.rightchild.parent = new_node
                new_node.leftchild = self.root
                self.root.rightchild = None

            self.root.parent = new_node  # Set the parent of the old root to the new node
            self.root = new_node 

    def delete(self, key: int):
        if self.root is None:
            return
        y =  self.bst(self.root, key)
        if y is None:
            return self.root
        self.root = self.splay(self.root, y)

        if y.leftchild is None:
            self.root = y.rightchild
            self.root.parent = None
        elif y.rightchild is None:
            self.root = y.leftchild
            self.root.parent = None
        else:
            l = y.leftchild
            r = y.rightchild
            l.parent = None
            r.parent = None
            self.root = r
            new_y = self.bst(r, y.key)
            self.splay(r, new_y)
            self.root.leftchild = l
            l.parent = self.root

    #Returns the node == key or the last node before falling out of the tree
    def bst(self, root, key) -> Node:
        if root is None:
            return None
        elif root.key == key:
            return root
        else:
            if root.key < key:
                if root.rightchild is None:
                    return root
                else:
                    return self.bst(root.rightchild, key)
            elif root.key > key:
                if root.leftchild is None:
                    return root
                else:
                    return self.bst(root.leftchild, key)

    #Given the key, ios or iop we need to move y back up to the top...
    def splay(self, root, y : Node):
        #If the tree is empty or the node is already at the root do nothing
        if y.parent is None:
            return y
        else:
            grandparent = y.parent.parent
        if root is None or root == y:
            return root
        #If the key is the direct child of the root, then we want to just move it up one, returning the new root
        elif root.leftchild != None and root.leftchild == y:
            self.rotate_right(y)
            return y
        elif root.rightchild != None and root.rightchild == y:
            self.rotate_left(y)
            return y
        ##Zig-Zig target/./root -> target\.\root or symmetrical if on outside
        elif grandparent is None:
            pass
        elif grandparent.rightchild is not None and grandparent.rightchild.rightchild == y:
            self.rotate_left( y.parent)
            self.rotate_left( y)
        elif grandparent.leftchild is not None and grandparent.leftchild.leftchild == y:
            self.rotate_right(y.parent)
            self.rotate_right( y)
        #Now do Zig-Zag if left-right or right-left child....
        elif grandparent.rightchild is not None and grandparent.rightchild.leftchild == y:
            self.rotate_right( y)
            self.rotate_left( y)
        elif grandparent.leftchild is not None and grandparent.leftchild.rightchild == y:
            self.rotate_left( y)
            self.rotate_right( y)

        #Now recursively call this function...
        return self.splay( root, y)

    #Call rotate on the child node to have it move to its parents level
    def rotate_right(self, x : Node):
        #move x up to parents position swapping inner children
        p = x.parent
        if p is None:
            return
        p.leftchild = x.rightchild
        if p.leftchild is not None:
            p.leftchild.parent = p
        x.rightchild = p
        #Reparent the nodes and adjust the child pointers on the grandparents...
        if self.root == p:
            self.root = x
            p.parent = x
            x.parent = None
            return
        else:
            x.parent = p.parent
            if p.parent.leftchild == p:
                p.parent.leftchild = x
            elif p.parent.rightchild == p:
                p.parent.rightchild = x
            p.parent = x
            return x

    def rotate_left(self, x : Node):
        #move x up to parents position swapping inner children
        p = x.parent
        if (p is None):
            return
        p.rightchild = x.leftchild
        if p.rightchild is not None:
            p.rightchild.parent = p
        x.leftchild = p
        #Reparent the nodes and adjust the child pointers on the grandparents...
        #If parent is root make x the new root
        if self.root == p:
            self.root = x
            p.parent = x
            x.parent = None
            return x
        #Otherwise adjust the grandparent
        else:
            x.parent = p.parent
            if p.parent.leftchild == p:
                p.parent.leftchild = x
            elif p.parent.rightchild == p:
                p.parent.rightchild = x
            p.parent = x
            return x