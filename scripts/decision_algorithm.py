"""Code for the decision tree generation and getting nodes.
"""

import numpy as np
import pandas as pd
from numpy import log2 as log
from random import randint
eps = np.finfo(float).eps

class decTree():
    """

    A class used to represent a decision tree.

    attributes
    ----------------
    nodes : list
        A list of alternating attributes and their values.
    df : dataframe
        Required pandas dataframe.

    Methods
    ----------------
    getTree()
        Returns tree.

    getNextNode(nodes : list)
        Returns (bool, node) according to user input and previously generated decision tree.
        First value is 1 if returning a suggestion, 0 if returning the next attribute to question
    
    fit(df : dataframe, maxDepth=6)
        Call initially to generate tree, no return value but generates tree.

    calcEnt(attr : str, df : dataframe)
        Calculates and returns entropy.

    buildTreeRec(df : dataframe, currDepth : int, maxDepth : int)
        Recursively generates tree with recursion depth controlled by maxDepth.

    createTree(df : dataframe, maxDepth : int)
        Gives initial call for the recursive function and returns decision tree.


    """
    def __init__(self):
        """
        
        Constructor for decTress class. Sets class attributes.
        
        parameters
        ----------------
        None
        
        returns
        ----------------
        None
        
        """
        self.tree = {}
        self.df = None
        
    def getTree(self):
        """D
        
        Defines getTree.

        parameters
        -------------------
        None
        
        returns
        -------------------
        tree
        
        """
        return self.tree
    
    def getNextNode(self, nodes):
        """
        
        Called iteratively by frontend to traverse decision tree according to user input. 
        Nodes is a list of alternating attributes and their values, that frontend has gone through till now.
        Returns (bool, node). first value is 1 if returning a suggestion, 0 if returning the next attribute to question.

        parameters
        -------------------
        nodes : list
            A list of alternating attributes and their values.
        
        returns
        -------------------
        bool, node
        
        """
        if len(nodes) == 0:
            nn = list(self.tree.keys())[0]
            nodes.append(nn)
            return (0, nn)
        currDict = self.tree
        for node in nodes:
            currDict = currDict[node]
        if isinstance(currDict, dict):
            nn = list(currDict.keys())[0]
            nodes.append(nn)
            return (0, nn)
        else:
            if isinstance(currDict, list):
                r = randint(0, len(currDict)-1)
                currDict = currDict[r]
            return (1, currDict)
        
    def fit(self, df, maxDepth=6):
        """
        
        Call initially to generate tree.
        Df is required pandas dataframe, maxDepth is the maximum depth of the generated tree.
        No return value but generates tree.

        parameters
        -------------------
        df : dataframe
            Required pandas dataframe.
        maxDepth : int
            The maximum depth of the generated tree.
        
        returns
        -------------------
        None
        
        """
        self.df = df
        self.tree = self.createTree(df, maxDepth)
    
    def calcEnt(self, attr, df):
        """
        
        Calculates entropy.

        parameters
        -------------------
        attr : str
            The column name for which to calculate entropy on.
        df : dataframe
            Required pandas dataframe.
        
        returns
        -------------------
        ent
        
        """
        num = len(df.loc[df[attr] == 1])
        den = len(df)
        ent = 2*(0.5 - abs(0.5 - num/den))
        return ent
    
    def buildTreeRec(self, df, currDepth, maxDepth):
        """
        
        Recursively generates tree, recursion depth controlled by maxDepth.

        parameters
        -------------------
        df : dataframe
            Required pandas dataframe.
        currDepth : int
            Current depth of recursion.
        maxDepth : int
            The maximum depth of the generated tree.

        returns
        -------------------
        tree
        
        """
        tree = {}
        node = {}
        attrs = list(df.columns)
        ents = {}
        for attr in attrs[1:]:
            ent = self.calcEnt(attr, df)
            ents[attr] = ent
        maxEntAttr = max(ents, key = ents.get)
        #print("depth: ", currDepth, "attribute: ", maxEntAttr, "rows: ", len(df), "columns: ", len(attrs))
        df0 = df.loc[df[maxEntAttr] == 0].drop([maxEntAttr], axis = 1)
        df1 = df.loc[df[maxEntAttr] == 1].drop([maxEntAttr], axis = 1)
        
        if len(df0) == 0 or len(df1) == 0 or currDepth > maxDepth:
            return list(df["HolidayPlace"])
        
        if len(df0) == 1:
            node[0] = list(df0["HolidayPlace"])[0]
             
        else:
            node[0] = self.buildTreeRec(df0, currDepth+1, maxDepth)
            
        if len(df1) == 1:
            node[1] = list(df1["HolidayPlace"])[0]
        else:
            node[1] = self.buildTreeRec(df1, currDepth+1, maxDepth)
            
        tree[maxEntAttr] = node
        
        return tree
    
    def createTree(self, df, maxDepth):
        """
        
        Gives initial call for the recursive function and returns tree.

        parameters
        -------------------
        df : dataframe
            Required pandas dataframe.
        maxDepth : int
            The maximum depth of the generated tree.

        returns
        -------------------
        tree
        
        """
        maxDepth = maxDepth - 1
        tree = self.buildTreeRec(df, 0, maxDepth)
        return tree
    
        