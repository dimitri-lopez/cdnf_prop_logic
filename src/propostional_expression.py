#!/usr/bin/env python3

from node import *
from special_characters import *
from fancy_print import *

class PropExpression:
    def __init__(self):
        self.root = None
        self.literals = set()
        self.expression = None
        self.fp = None
    def setRoot(self, root):
        self.root = root
    def getRoot(self):
        return self.root
    def addLiteral(self, literal):
        self.literals.add(literal)
    def getEval(self): # TODO
        return
    def addFancyPrint(self, fp):
        self.fp = fp
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
    # def getExpression(self):
    #     # if self.expression is None:
    #     self.nodeExpression(self.root)
    #     return self.expression

    def getExpression(self):
        return self.root.getExpression()

    def sortByExpression(self, node = None):
        if node is None: node = self.root
        for i in node.children:
            self.sortByExpression(i)
        node.children.sort()

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

    def algebraStep(self, fn, message, node = None):
        if node is None: node = self.root
        node_fn = "node." + fn
        changed = eval(node_fn)
        if changed:
            self.fp.addRow(self.getExpression(), message)
            self.algebraStep(fn, message, self.root) # recurse back to the root
            return
        for i in node.children:
            self.algebraStep(fn, message, i)





    def dnf(self):
        self.nnf() # get into nnf first
        self.root.distribution()
    def cdnf(self):
        # Get rid of TAUT and CONT
        exp = self.getExpression()
        prev_exp = ""
        while exp != prev_exp:
            self.algebraStep("inverse()", "Inverse")
            self.algebraStep("identity()", "Identity")
            self.algebraStep("annihilation()", "Annihilation")
            prev_exp = exp
            exp = self.getExpression()
        return




        self.dnf()
        self.root.adjacency()
        # implicit commutation step
        self.root.idempotence()
        self.root.complement()
        self.root.annihilation()
        self.root.identity()
        self.root.idempotence()
