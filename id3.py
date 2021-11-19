# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 13:59:12 2021

@author: Krishna


* Decision tree and related functions
* Call fit() at start to generate tree
* Call getNextNode() iteratively to traverse tree
* Random suggestion in case we can't narrow it down to one is not yet implemented


"""

import numpy as np
import pandas as pd
eps = numpy.finfo(float).eps
from numpy import log2 as log
from random import randint


class decTree():
    def __init__(self):
        self.tree = {}
        self.df = None
        
    def getTree(self):
        return self.tree
    
    def getNextNode(self, nodes):
        #Called iteratively by frontend to traverse decision tree according to user input
        #nodes is a list of alternating attributes and their values, that frontend has gone through till now
        #Returns (bool, node). first value is 1 if returning a suggestion, 0 if returning the next attribute to question
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
            return (1, currDict)
        
    def fit(self, df, maxDepth=6):
        #Call initially to generate tree
        #df is required pandas dataframe, maxDepth is the maximum depth of the generated tree
        #No return value but generates tree
        self.df = df
        self.tree = self.createTree(df, maxDepth)
    
    def calcEnt(self, attr, df):
        #Calculates entropy
        #May not use the exact correct formula for entropy, but it works
        num = len(df.loc[df[attr] == 1])
        den = len(df)
        ent = 2*(0.5 - abs(0.5 - num/den))
        return ent
    
    def buildTreeRec(self, df, currDepth, maxDepth):
        #Recursively generates tree, recursion depth controlled by maxDepth
        tree = {}
        node = {}
        attrs = list(df.columns)
        ents = {}
        for attr in attrs[1:]:
            ent = self.calcEnt(attr, df)
            ents[attr] = ent
        maxEntAttr = max(ents, key = ents.get)
        #print("depth: ", currDepth, "attribute: ", maxEntAttr, "rows: ", len(df), "columns: ", len(attrs))
        df0 = df.loc[df2[maxEntAttr] == 0].drop([maxEntAttr], axis = 1)
        df1 = df.loc[df2[maxEntAttr] == 1].drop([maxEntAttr], axis = 1)
        
        if len(df0) == 0 or len(df1) == 0:
            return list(df["HolidayPlace"])[0]
        
        if len(df0) == 1 or currDepth > maxDepth:
            s = list(df0["HolidayPlace"])[0]
            node[0] = s
        else:
            node[0] = self.buildTreeRec(df0, currDepth+1, maxDepth)
        if len(df1) == 1 or currDepth > maxDepth:
            node[1] = list(df1["HolidayPlace"])[0]
        else:
            node[1] = self.buildTreeRec(df1, currDepth+1, maxDepth)
            
        tree[maxEntAttr] = node
        
        return tree
    
    def createTree(self, df, maxDepth):
        #Gives initial call for the recursive function
        #returns tree
        tree = self.buildTreeRec(df, 0, maxDepth)
        return tree
    
        