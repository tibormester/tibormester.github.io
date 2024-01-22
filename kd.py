from __future__ import annotations
import json
import math
from typing import List

#Global variable to enable debug print operations
debug = False

# Datum class.
# DO NOT MODIFY.
class Datum():
    def __init__(self,
                 coords : tuple[int],
                 code   : str):
        self.coords = coords
        self.code   = code
    def to_json(self) -> str:
        dict_repr = {'code':self.code,'coords':self.coords}
        return(dict_repr)
    def dimension(self) -> int:
        return len(self.coords)
    #returns the distance^2 to the point
    def distance(self, point : tuple) -> int:
        distances = [0] * self.dimension()
        #Checks if the point is less than the min, greater than the max or somewhere inbetween
        for i in range(0, self.dimension()):
            if point[i] < self.coords[i]:
                distances[i] = self.coords[i] - point[i]
            elif point[i] > self.coords[i]:
                distances[i] = point[i] - self.coords[i]
            else:
                distances[i] = 0
        distance = 0
        #The overall euclidean distance is the sum of the squares of the distance in each direction
        for dist in map(lambda dist : dist * dist, distances):
            distance += dist
        return distance
    
    

# Internal node class.
# DO NOT MODIFY.
class NodeInternal():
    def  __init__(self,
                  splitindex : int,
                  splitvalue : float,
                  leftchild,
                  rightchild):
        self.splitindex = splitindex
        self.splitvalue = splitvalue
        self.leftchild  = leftchild
        self.rightchild = rightchild
    #returns the opposite child as the one given
    def otherChild(self, child ):
        return self.leftchild if self.rightchild == child else self.rightchild
    #takes a current child node and replaces it with the replacement
    def swap(self, child, replacement):
        if self.leftchild == child:
            self.leftchild = replacement
        elif self.rightchild == child:
            self.rightchild = replacement
    # def __eq__(self, other):
    #     if isinstance(other, NodeInternal):
    #         if other.splitindex == self.splitindex and other.splitvalue == self.splitvalue: return True
    #     return False

    def minmax(self)-> (list[int], list[int]):
        (lmin, lmax) = self.leftchild.minmax()
        (rmin, rmax) = self.rightchild.minmax()
        mins = [lmin[i] if lmin[i] <= rmin[i] else rmin[i] for i in range(0, len(lmin))]
        maxes = [lmax[i] if lmax[i] >= rmax[i] else rmax[i] for i in range(0, len(lmax))]
        return (mins, maxes)
    #returns the smallest distance from the children
    def distance(self, point : tuple[int]) -> int:
        (min, max) = self.minmax()
        distances = [0] * len(min)
        #Checks if the point is less than the min, greater than the max or somewhere inbetween
        for i in range(0, len(min)):
            if point[i] < min[i]:
                distances[i] = min[i] - point[i]
            elif point[i] > max[i]:
                distances[i] = point[i] - max[i]
            else:
                distances[i] = 0
        distance = 0
        #The overall euclidean distance is the sum of the squares of the distance in each direction
        for dist in map(lambda dist : dist * dist, distances):
            distance += dist
        return distance
    def closer(self, point: tuple[int]):
        return self.leftchild if self.leftchild.distance(point) <= self.rightchild.distance(point) else self.rightchild

    
        

# Leaf node class.
# DO NOT MODIFY. I only added internal helper methods because it made sense to do so to promote abstraction through encapsulation
class NodeLeaf():
    def  __init__(self,
                  data : List[Datum]):
        self.data = data
    #Helper function to get the dimensions of our datum coords
    def dimension(self)-> int:
        return self.data[0].dimension()
    
    #Helper function for both calculating spread and get the bounding box dimensions by giving bottom left corner top right corner
    def minmax(self) -> (list[int], list[int]):
        mins = [self.data[0].coords[i] for i in range(0, self.dimension())]
        maxes = mins.copy()
        for datum in self.data :
            #for each dimension in each coordinate
            for i in range(0, self.dimension()):
                value = datum.coords[i]
                #if the value is less than our min or greater than our max replace it
                mins[i] = value if value < mins[i] else mins[i]
                maxes[i] = value if value > maxes[i] else maxes[i]
        return (mins, maxes)
    #returns the index of the maxspread coordinate
    def maxSpreadIndex(self) -> int:
        #Stores are min and max coordinates in each dimension and initializes the default values to the fist datum
        (mins, maxes) = self.minmax()
        #stores max - min = spread
        spreads = [0 for i in range(0, self.dimension())]
        #initialize max spread (index = dimension) to 0 and iterate through the rest of the dimensions
        maxspread = 0
        for i in range(0, self.dimension()):
            spreads[i] = maxes[i] - mins[i]
            #if this dimensions spread is strictly greater than replace it
            maxspread = i if spreads[i] > spreads[maxspread] else maxspread
        #return max spread, might want to alter so we can return a tuple with max spread and the median
        return maxspread
    #ideally given the max spread index, sort this node such that datum are sorted along the index and ties broken in cycling order
    def sort(self, index : int):
        #Define our internal cycling function that given a datum returns a tuple of its coordinates in the proper order
        def cycling(original : Datum) -> tuple[int]:
            coords = [0] * self.dimension()
            OGindex = index
            for i in range(0, self.dimension()):
                coords[i] = original.coords[OGindex]
                OGindex += 1
                OGindex = OGindex if OGindex < self.dimension() else 0
            return tuple(coords)
        #Sorts the datum based on the cycled coordinates cycled at the given index, then it sets this nodes data to be this sorted data
        self.data = sorted(self.data, key=cycling)
    #returns the median but assumes is already sorted so tbh this isnt the actual median...
    def median(self, index : int) -> float :
        #Size of our leaf nodes data list
        size = len(self.data)
        if size % 2 == 1:
            medianDatum = self.data[int((size - 1) * 0.5)]
            return float(medianDatum.coords[index])
        else :
            # get the middle two coordinates and return the average
            #TODO MAKE SURE THAT CASTING TO INT DOESNT INTRODUCE ROUNDING ERRORS
            lDatum = self.data[int((size * 0.5) - 1)]
            uDatum = self.data[int((size * 0.5) + 0)]
            uVal = float(uDatum.coords[index])
            lVal = float(lDatum.coords[index])
            return float((uVal + lVal) * 0.5)
        
    # def __eq__(self, other):
    #     if isinstance(other, NodeLeaf):
    #         for datum in other.data:
    #             if self.data.count(datum) < 1:
    #                 return False
    #         return True
    #     else : return False
    #returns the distance^2 to the point
    def distance(self, point : tuple) -> int:
        (min, max) = self.minmax()
        distances = [0] * self.dimension()
        #Checks if the point is less than the min, greater than the max or somewhere inbetween
        for i in range(0, self.dimension()):
            if point[i] < min[i]:
                distances[i] = min[i] - point[i]
            elif point[i] > max[i]:
                distances[i] = point[i] - max[i]
            else:
                distances[i] = 0
        distance = 0
        #The overall euclidean distance is the sum of the squares of the distance in each direction
        for dist in map(lambda dist : dist * dist, distances):
            distance += dist
        return distance


# KD tree class.
class KDtree():
    def  __init__(self,
                  k    : int,
                  m    : int,
                  root = None):
        self.k    = k
        self.m    = m
        self.root = root

    # For the tree rooted at root, dump the tree to stringified JSON object and return.
    # DO NOT MODIFY.
    def dump(self) -> str:
        def _to_dict(node) -> dict:
            if isinstance(node,NodeLeaf):
                return {
                    "p": str([{'coords': datum.coords,'code': datum.code} for datum in node.data])
                }
            else:
                return {
                    "splitindex": node.splitindex,
                    "splitvalue": node.splitvalue,
                    "l": (_to_dict(node.leftchild)  if node.leftchild  is not None else None),
                    "r": (_to_dict(node.rightchild) if node.rightchild is not None else None)
                }
        if self.root is None:
            dict_repr = {}
        else:
            dict_repr = _to_dict(self.root)
        return json.dumps(dict_repr,indent=2)
    def _to_dict(self, node) -> dict:
        if isinstance(node, NodeLeaf):
            return {
                "p": str([{'coords': datum.coords,'code': datum.code} for datum in node.data])
            }
        else:
            return {
                "splitindex": node.splitindex,
                "splitvalue": node.splitvalue,
                "l": (self._to_dict(node.leftchild)  if node.leftchild  is not None else None),
                "r": (self._to_dict(node.rightchild) if node.rightchild is not None else None)
            }
        
    def string(self, node) -> str:
        return json.dumps(self._to_dict(node), indent=2)
                          
    
    #searches the tree for the leaf node that our point belongs in, returning the path traveled as the acc
    #This has two modes, if present then it finds the point and returns true if found false otherwise
    #if not present, then it finds the location to insert before falling out
    def search(self, point : tuple[int], acc : list, present = True) -> bool:
        if len(acc) < 1:
            print("This shouldn't occour, we have a parent acc being empty: \n" + self.dump())
        node = acc[-1]
        #If it is a leaf node and present return true iff the point is in the datum coords
        #if not present then simply return true 
        if isinstance(node, NodeLeaf):
            if present:
                for datum in node.data:
                    if datum.coords == point:
                        return True
                return False
            else : return True
        #if we are on a splitting node sort by binary tree on the splitting index and value
        elif isinstance(node, NodeInternal):
            i = node.splitindex
            value = node.splitvalue
            if point[i] < value:
                acc.append(node.leftchild)
                return self.search(point, acc, present)
            elif point[i] > value:
                acc.append(node.rightchild)
                return self.search(point, acc, present)
            #Tie behavior is dependent on if searching for insertion (present == false) versus deletion (present == true)
            #on insertion we want to always go right, while on deletion we want to search both sides
            elif point[i] == value:
                if present:
                    #Check both sides, make a copy for the left side so acc remains the same for the right side
                    leftacc = acc.copy()
                    leftacc.append(node.leftchild)
                    if self.search(point, leftacc, present):
                        acc = leftacc
                        return True
                    #if it isnt in the left side search the right side
                    else :
                        acc.append(node.rightchild)
                        return self.search(point, acc, present)
                else:
                    #always go right by convention
                    acc.append(node.rightchild)
                    return self.search(point, acc, present)
        else:
            print("while searching got a node of type: " + str(type(node)))
            

    # Insert the Datum with the given code and coords into the tree.
    # The Datum with the given coords is guaranteed to not be in the tree.
    def insert(self,point:tuple[int],code:str):
        if self.root is None:
            self.root = NodeLeaf([Datum(point, code)])
            return
        parents = [self.root] 
        if(self.search(point, parents, False)):
            node = parents[-1]
            if isinstance(node, NodeLeaf):
                node.data.append(Datum(point, code))
                #we need to split the node if it now exceeds the max size
                if len(node.data) > self.m:
                    index = node.maxSpreadIndex()
                    node.sort(index)
                    value = node.median(index)
                    #Splits the sorted node by the rounded down number of nodes
                    midpoint = math.floor(len(node.data) * 0.5 )
                    #Creates the new leaves and the proper parent node
                    leftLeaf = NodeLeaf(node.data[:midpoint])
                    rightLeaf = NodeLeaf(node.data[midpoint:])
                    parentNode = NodeInternal(index, value, leftLeaf, rightLeaf)
                    #now we need to add the parentNode to the tree inplace of the old node
                    #if there is no parent to adjust child pointers, then we need to change the tree's root node
                    if len(parents) == 1:
                        self.root = parentNode
                    else:
                        parent = parents[-2]
                        if isinstance(parent, NodeInternal):
                            #find if the node we split was (technically still is) the left or the right child, then replace it with our new internal parent node
                            if parent.leftchild == node:
                                parent.leftchild = parentNode
                            else:
                                parent.rightchild = parentNode
                        else:print("error on insertion couldn't find an Internal node for the parent\n" + self.dump())

            else: print("error on insertion couldn't find a leaf node\n" + self.dump())
        else: print("error on insertion couldn't find a leaf node probably...?\n" + self.dump())

        if debug: print("inserted: " + code + "\n" + self.dump())

    # Delete the Datum with the given point from the tree.
    # The Datum with the given point is guaranteed to be in the tree.
    def delete(self,point:tuple[int]):
        parents = [self.root]
        if (self.search(point, parents)):
            node = parents[-1]
            if debug: print("node: " + str([{'coords': datum.coords,'code': datum.code} for datum in node.data]))
            removed = None
            for datum in node.data:
                if datum.coords == point:
                    #wait till after the looping to safely remove?
                    removed = datum
            node.data.remove(removed)
            #If the new node.data has 0 length we need to delete it, this involves deleting the parent splitting node too and updating the grandparents children
            if len(node.data) == 0:
                # ##Add it back so we can evaluate comparisons properly
                # node.data.append(removed)
                if len(parents) == 1:
                    self.root = None
                elif isinstance(parents[-2], NodeInternal):
                    parent = parents[-2]
                    if len(parents) == 2:
                        self.root = parent.otherChild(node)
                    elif isinstance(parents[-3], NodeInternal):    
                        gparent = parents[-3]
                        sibling = parent.otherChild(node)
                        #I messed up on my otherChild function and kept returning the same child...
                        if debug:
                            print("parents: " + list(map(lambda x :  x.splitvalue if isinstance(x, NodeInternal) else str([{'coords': datum.coords,'code': datum.code} for datum in x.data]) , parents)).__str__())
                            print("gparent: " + str(gparent.splitindex) + ", " +  gparent.splitvalue.__str__())
                            if isinstance(sibling, NodeInternal): print("sibling: " + str(sibling.splitindex) + ", " +  sibling.splitvalue.__str__())
                            elif isinstance(sibling, NodeLeaf): print("sibling: " + str([{'coords': datum.coords,'code': datum.code} for datum in sibling.data]))
                        gparent.swap(parent, sibling)
                    else: print("When deleting " + str(point) +"we somehow have a grand parent that is a leaf?\n" + self.dump())
                else: print("When deleting " + str(point) + "we somehow have a parent that is a leaf?\n" + self.dump())
            if debug: print("Deleted " + str(point) + "\n" + self.dump())
        else: print("When deleting " + str(point) + "we couldnt find the point in the tree\n" + self.dump())
        
                        
                    


    # Find the k nearest neighbors to the point.
    def knn(self,k:int,point:tuple[int]) -> str:
        # Use the strategy discussed in class and in the notes.
        # The list should be a list of elements of type Datum.
        # While recursing, count the number of leaf nodes visited while you construct the list.
        # The following lines should be replaced by code that does the job.
        knnlist = []

        leaveschecked = self.knn_helper(k, point, 0, knnlist, self.root)

        # The following return line can probably be left alone unless you make changes in variable names.
        return(json.dumps({"leaveschecked":leaveschecked,"points":[datum.to_json() for datum in knnlist]},indent=2))
    
    #The leaves checked requirement is stupid because the algorithm is pretty vague and isn't even optimal so like either clarify or give a maximum and min and let us check between
    #the notes on the site differ from the project requirments
    def knn_helper(self, k : int, point : tuple[int], leaveschecked : int, knnlist : list, node) -> int:
        #If we are at a leaf node, increment our counter and try to update our list
        if isinstance(node, NodeLeaf):
                if debug: print("checking node:" + self.string(node))
                self.checkList(point, k, knnlist, node)
                return leaveschecked + 1 
        #If we are at an internal node if we visit each subtree depends on our fullness and our distance
        elif isinstance(node, NodeInternal):
            full = True if knnlist.__len__() == k else False
            farthest = knnlist[-1].distance(point) if knnlist.__len__() > 0 else -1
            #We start at the closest subtree defaulting to the left subtree
            subtree = node.closer(point)
            #if the closest subtree is <= farthest or the list isnt full then recurse through it
            if not full or subtree.distance(point) <= farthest:
                if debug: print("checking subtree since distance: " + str(subtree.distance(point)) + " <= " + str(farthest) + "\n" + self.string(node))
                leaveschecked = self.knn_helper(k, point, leaveschecked, knnlist, subtree)
                #Check again for the second subtree, but first recalculate full, farthest and set subtree to being the other child
                full = True if knnlist.__len__() == k else False
                farthest = knnlist[-1].distance(point) if knnlist.__len__() > 0 else -1
                subtree = node.otherChild(subtree)
                if not full or subtree.distance(point) <= farthest:
                    if debug: print("checking subtree at distance: " + str(subtree.distance(point)) + " <= " + str(farthest) + "\n" + self.string(node))
                    return self.knn_helper(k, point, leaveschecked, knnlist, subtree)
                else: 
                    return leaveschecked
            return leaveschecked
    #returns True if the list was updated and false if otherwise
    def checkList(self, point : tuple[int], k :int, knnList : list, node :NodeLeaf):
        oldlist = knnList.copy()
        #sorts datum by their distance to the point and code secondary
        def distance(datum : Datum ):
            return (datum.distance(point), datum.code)
        #adds all the datum togther then sorts and trims
        knnList.extend(node.data)
        knnList.sort(key=distance)
        while knnList.__len__() > k:
            knnList.pop()
        return False if oldlist == knnList else True
    