#!/usr/bin/env python3

from node import *
from special_characters import *

class BinaryExpression:
    def __init__(self):
        self.root = None
        self.literals = set()
        self.expression = None
    def setRoot(self, root):
        self.root = root
    def getRoot(self):
        return self.root
    def addLiteral(self, literal):
        self.literals.add(literal)
    def getEval(self): # TODO
        return
    def print(self, currentNode = None , level = 0):
        if currentNode is None: currentNode = self.root

        childrenStr = ""
        # Print the node
        for i in currentNode.children:
            childrenStr += "{}, ".format(i.getValue())

        print(("|   " * level) + "Value: {} - Children ({}): {}".format(currentNode.getValue(), len(currentNode.children), childrenStr))
        for i in currentNode.children:
            if len(i.children) > 0: self.print(i, level + 1)
    def clean(self): # A user can have levels that are just nested parantheses without any actual information
        # print("testing equality {}".format(self.root.getValue() == ""))
        if self.root.getValue() == "":
            assert(len(self.root.children) == 1)
            self.root = self.root.children[0]
        self.removeEmpties(self.root)
        self.getExpression() # Build the tree from the bottom, then we are gonna sort thie lists
        self.sortByExpression()
        # TODO Sort the bottom nodes


    def removeEmpties(self, parentNode):
        if parentNode.getValue() == "":
            assert(len(parentNode.children) == 1)
        for index in range(len(parentNode.children)):
            i = parentNode.children[index]
            if i.getValue() == "": # remove this node
                assert(len(i.children) == 1)
                parentNode.children[index] = i.children[0]
                i = parentNode.children[index]
            self.removeEmpties(i)
    def getExpression(self):
        # if self.expression is None:
        self.nodeExpression(self.root)
        return self.expression

    def getExpression(self):
        return self.root.getExpression()

    def sortByExpression(self, node = None):
        if node is None: node = self.root
        for i in node.children:
            self.sortByExpression(i)
        node.children.sort()

    def applyOperations(self, node = None):
        if node is None: node = self.root
        # node.inverse()
        # node.double_negation()
        # node.idempotence()
        # node.complement()
        # node.identity()
        # node.annihilation()
        # node.absorption()
        # node.neg_demorgan()
        node.distribution()
        # for i in node.children:
        #     self.applyOperations(i)
    def nnf(self, node = None):
        if node is None: node = self.root
        if node.neg_demorgan(): # go to the top of the tree and start over
            print("{}          DeMorgan --------".format(self.getExpression()))
            self.nnf()
        if node.double_negation(): # go to the top of the tree and start over
            print("{}       Double Negation ----".format(self.getExpression()))
            self.nnf()

        for i in node.children:
            self.nnf(i)

    def dnf(self):
        self.nnf() # get into nnf first
