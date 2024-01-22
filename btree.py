from __future__ import annotations
import json
from typing import List
import math

# Node Class.
# You may make minor modifications.
class Node():
    def  __init__(self,
                  keys     : List[int]  = None,
                  values   : List[str] = None,
                  children : List[Node] = None,
                  parent   : Node = None):
        self.keys     = keys
        self.values   = values
        self.children = children
        self.parent   = parent

# DO NOT MODIFY THIS CLASS DEFINITION.
class Btree():
    def  __init__(self,
                  m    : int  = None,
                  root : Node = None):
        self.m    = m
        self.root = root

    # DO NOT MODIFY THIS CLASS METHOD.
    def dump(self) -> str:
        #print(self.root.values)
        def _to_dict(node) -> dict:
            if node.children is not None:
                return {
                    "keys": node.keys,
                    "values": node.values,
                    "children": [(_to_dict(child) if child is not None else None) for child in node.children]
                }
            else:
                return {
                    "keys": node.keys,
                    "values": node.values,
                    "children": [None]
                }
        if self.root == None:
            dict_repr = {}
        else:
            dict_repr = _to_dict(self.root)
        return json.dumps(dict_repr,indent=2)

    # Insert.
    def insert(self, key: int, value: str):     
        #If the tree is empty initialize it
        if self.root is None:
            self.root = Node([key],[value])
            return
        node = self.find_key(key, self.root)
        #at the right leaf, adds the key value in the proper sorted location
        for i in range(0, len(node.keys) + 1):
            #If the target key is smaller than the next key, insert it and the value into the leaf at that spot or if we are at the end insert it regardless
            if i == len(node.keys):
                node.keys.insert(-1, key)
                node.values.insert(-1, value)
            elif key < node.keys[i]:
                node.keys.insert(i, key)
                node.values.insert(i, value)
                break
        #check if this node is now overfull, first try and rotate to fix otherwise recursively split up the parent
        while self.overfull(node):
            #gets the siblings if exist or none otherwise
            l_sib = self.get_sibling(node, -1)
            r_sib = self.get_sibling(node, 1)
            if l_sib is not None and self.has_space(l_sib):
                self.rotate(node, l_sib)
            elif r_sib is not None and self.has_space(r_sib):
                self.rotate(node, r_sib, -1)
            else:
                #if we cannot rotate then we split the current node and check the resulting parent node if its overfilled...
                node = self.split(node)

    #given an overfull node, split it and return the parent with the node replaced by the two new nodes
    def split(self, node: Node) -> Node:
        #if we are splitting the root node, create a new node and assign it to be the root node...
        if node.parent is None:
            #create an empty new root node, we add one key,value pair, and 2 children
            #initialize children array with the old root node
            node.parent = Node([],[],[node], None)
            self.root = node.parent
        if node.parent.children is None:
            pass
        p = node.parent
        #The index of the lower median
        median = math.floor((len(node.keys) - 1) / 2.0)
        #The keys get split from 0 to Median -1 and median + 1 to end
        #while the children go from 0 to Median and Median + 1 to end
        if node.children is not None: #split a normal node create two normal nodes
            l_child = Node(node.keys[0:median], node.values[0:median], node.children[0:median+1], p)
            r_child = Node(node.keys[median+1:], node.values[median+1:], node.children[median+1:], p)
        else: #If we split a leaf create two leaves
            l_child = Node(node.keys[0:median], node.values[0:median], None, p)
            r_child = Node(node.keys[median+1:], node.values[median+1:], None, p)
        #Insert the children into the parent by finding current index, replacing with right child and inserting left child, finally insert the median key as a new key
        i = p.children.index(node)
        p.children[i] = r_child
        p.children.insert(i, l_child)
        #insert the promoted median as a key,value pair into the parent
        p.keys.insert(i, node.keys[median])
        p.values.insert(i, node.values[median])
        return p

    def merge(self, node: Node, sib : Node, dir = 0) -> Node:
        sibdir = (dir * -1) - 1
        p = node.parent
        pindex = p.children.index(node) + 1 + sibdir
        #remove key,value from parent
        key = p.keys.pop(pindex)
        value = p.values.pop(pindex)
        #remove sib from parent
        p.children.remove(sib)
        #append to the node at dir the median and then the sibling's key, values
        node.keys.insert(dir, key)
        node.values.insert(dir,value)
        #removes the key,values from the sib, adding to the node in reverse order...
        while len(sib.keys) > 0:
            key = sib.keys.pop(sibdir)
            value = sib.values.pop(sibdir)
            node.keys.insert(dir, key)
            node.values.insert(dir,value)
        #Removes the children from the sibling, adding them to the node in the reverse orders
        while len(sib.children) > 0:
            node.children.insert(dir, sib.children.pop(sibdir))
        #return the parent, it now has 1 less child and key,value
        return p
        

    #given the node and its sibling ( 0 for left -1 for right) shift nodes from node to sibling until node.keys = ceil( [node.keys + sib.keys].len / 2.0 )
    def rotate(self, node : Node, sib : Node, dir = 0):
        T = self.half(len(node.keys) + len(sib.keys))
        sibdir = (dir * -1) - 1 #maps 0 -> -1 and -1 -> 0, so first goes to last and last goes to first
        p = node.parent
        #pindex represents the index of the key,value in the parent between the sibling and the node
        pindex = p.children.index(node)  + sibdir
        #if to the left, pindex = -1 + 1 -1 = -1, if to the right pindex = -1 + 1 + 0 = 0
        while len(node.keys) > T:
            #Get the lowest or highest key,value from the node
            key = node.keys.pop(dir)
            value = node.values.pop(dir)
            #Insert it into the parent at the right key spot
            p.keys.insert(pindex, key)
            p.values.insert(pindex, value)
            #remove the old key,value from the parent
            key = p.keys.pop(pindex + 1)
            value = p.values.pop(pindex + 1)
            #add the old key,value to the sibling....
            sib.keys.insert(sibdir, key)
            sib.values.insert(sibdir, value)
        



    #returns the sibling (direction is relative indexing from the current node) or returns None
    def get_sibling(self, node : Node, dir : int) -> Node:
        if node.parent is None:
            return None
        for i in range(0, len(node.parent.children)):
            if node.parent.children[i] == node:
                    sib = i + dir
                    #If sib < 0 or sib >= children.len then the left or right sibling doesnt exist
                    if sib in range(0, len(node.parent.children)):
                        return node.parent.children[i + dir]
                    else: 
                        return None



    #By default searches for the leaf where the key goes or returns the node containing the key
    def find_key(self, key : int, node : Node, acc : List = []) -> Node:
        #  #ensures that the visited node is recorded in order of traversal
        #  #acc.insert(-1, node)
        #Return the node if it is a leaf, aka children list is none
        if node.children is None:
            #get the value of the key if its in this node
            if key in node.keys:
                acc.append(node.values[node.keys.index(key)])
            return node
        #for each key, if the target is less than go to that child, or if not go to the last child
        for i in range(0, len(node.keys)):
            if key < node.keys[i]:
                acc.append(i)
                return self.find_key(key, node.children[i], acc)
            elif key == node.keys[i]:
                acc.append(node.values[i])
                return node
        acc.append(len(node.keys))
        return self.find_key(key, node.children[len(node.keys)], acc)

    # Delete.
    def delete(self, key: int):
        #If the tree is empty do nothing
        if self.root == None:
            return
        #find the node with the key
        node = self.find_key(key, node)
        #if the node isn't a leaf get the inorder successor, replace and delete from there
        if node.children is not None:
            #key+1 is garunteed to return IoS's node and it will be first in the key,value pair
            IoS_node = self.find_key(key+1, node)
            #Delete the key,value from the leaf
            IoS_key = IoS_node.keys.pop(0)
            IoS_value = IoS_node.values.pop(0)
            #swap the key,value with the IoS
            i = node.keys.index(key)
            node.keys[i] = IoS_key
            node.values[i] = IoS_value
            #set node = IoS so we can check for underfull
            node = IoS_node
        else: #if its the leaf node, we remove the key,value from the node
            i = node.keys.index(key)
            node.keys.pop(i)
            node.values.pop(i)
        #now, we know node is a leaf and we need to check if its underfull
        while self.underfull(node):
            #gets the siblings if exist or none otherwise
            l_sib = self.get_sibling(node, -1)
            r_sib = self.get_sibling(node, 1)
            if l_sib is not None and self.has_extra(l_sib):
                self.rotate(l_sib, node, -1)
            elif r_sib is not None and self.has_extra(r_sib):
                self.rotate(r_sib, node, 0)
            else:
                #if we cannot rotate then we split the current node and check the resulting parent node if its underfilled...
                if l_sib is not None:
                    node = self.merge(node, l_sib)
                elif r_sib is not None:
                    node = self.merge(node, r_sib, -1)
                else: #this node is the root node since it has no siblings, and it's underfull conditions are different
                    if len(node.keys) > 0: #has at least a single key means its not underfull so we are finished
                        return
                    else: #is undefull without keys so we promote the first (and only) child to the root
                        self.root = node.children.pop(0)
                        return



    # Search
    def search(self,key) -> str:
        path = []
        self.find_key(key, self.root, path)
        return json.dumps(path)

    #Checking for children is probably redundent...
    def overfull(self, node:Node) -> bool:
        # keys <= m - 1
        if len(node.keys) >= self.m:
            return True
        return False
    def underfull(self, node:Node) -> bool:
        # keys >= m/2 -1
        if node.keys < (self.half() - 1):
            return True
        return False
    
    def has_space(self, node:Node)-> bool:
        # keys < m - 1, then there exists room for another key
        if len(node.keys) < self.m - 1:
            return True
        return False
    
    def has_extra(self, node:Node)-> bool:
        # keys > m, then there exists an extra ontop of the minimum number of keys
        if len(node.keys) > self.half():
            return True
        return False

    #returns ceiling of self.m / 2.0, or whatever value
    def half(self, x = 0.5) -> int:
        if x == 0.5: #x should always be an integer so if it isnt it wasnt passed and use self.m as default
            x = self.m
        return math.ceil( x / 2.0)
    
