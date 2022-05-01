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
    # A user can have levels that are just nested parantheses without any actual
    # information there can also be just blank nodes? Gonna clean those up too.
    # TODO: With the input "# | ~~^ | ~~~#" some weird parsing is done and blank
    # nodes are introduced
    def clean(self):
        # print("testing equality {}".format(self.root.getValue() == ""))
        while self.root.getValue() == "":
            assert(len(self.root.children) == 1)
            self.root = self.root.children[0]
            self.root.parent = None
        self.removeEmpties(self.root)
        self.getExpression() # Build the tree from the bottom, then we are gonna sort thie lists
        self.sortByExpression()


    def removeEmpties(self, parentNode):
        if parentNode.getValue() == "":
            assert(len(parentNode.children) == 1)
            assert(False)
        for index in range(len(parentNode.children)):
            i = parentNode.children[index]
            if i.getValue() == "": # remove this node
                assert(len(i.children) == 1)
                parentNode.children[index] = i.children[0]
                parentNode.children[index].parent = parentNode
                i = parentNode.children[index]
            self.removeEmpties(i)

    def getExpression(self):
        return self.root.getExpression()

    def sortByExpression(self, node = None):
        if node is None: node = self.root
        for i in node.children:
            self.sortByExpression(i)
        node.children.sort()

    def nnf(self):
        exp = self.getExpression()
        prev_exp = ""
        while exp != prev_exp:
            self.algebraStep("neg_demorgan()", "DeMorgan")
            self.algebraStep("double_negation()", "Double Negation")
            prev_exp = exp
        self.fp.addRow(self.getExpression(), "Negation Normal Form")


    def dist(self, node):
        for i in node.children:
            if self.dist(i): return True# go to top
        # print("dist: {}".format(node))
        changed = node.distribution()
        if changed:
            self.fp.addRow(self.getExpression(), "Distribution")
        return changed
    def check_dnf(self):
        max_depth = self.get_max_depth()
        if max_depth <= 2: return True
        else: return False

    def get_max_depth(self, node = None, depth = 0):
        if node is None: node = self.root
        if node.getValue() == NOT: return depth # should be nnf
        max_depth = depth
        for i in node.children:
            max_depth = max(self.get_max_depth(i, depth + 1), max_depth)
        return max_depth

    def cdnf(self):
        # Get rid of TAUT and CONT
        exp = self.getExpression()
        prev_exp = ""
        while exp != prev_exp:
            self.algebraStep("inverse()", "Inverse")
            self.algebraStep("identity()", "Identity")
            self.algebraStep("annihilation()", "Annihilation")
            self.algebraStep("idempotence()", "Idempotence")
            self.algebraStep("association()", "Association")
            prev_exp = exp
            exp = self.getExpression()

        self.nnf()

        # DNF
        exp = self.getExpression()
        prev_exp = ""
        while exp != prev_exp:
            self.algebraStep("inverse()", "Inverse")
            self.algebraStep("identity()", "Identity")
            self.algebraStep("annihilation()", "Annihilation")
            self.algebraStep("idempotence()", "Idempotence")
            self.algebraStep("association()", "Association")
            self.algebraStep("complement()", "Complement")
            self.algebraStep("identity()", "Identity")
            self.algebraStep("annihilation()", "Annihilation")
            self.algebraStep("identity()", "Identity")
            if not self.check_dnf(): self.dist(self.root)
            prev_exp = exp
            exp = self.getExpression()
        self.fp.addRow(self.getExpression(), "Disjunctive Normal Form")

        exp = self.getExpression()
        prev_exp = ""
        while exp != prev_exp:
            self.algebraStep("association()", "Association")
            self.algebraStep("idempotence()", "Idempotence")
            self.algebraStep("identity()", "Identity")
            self.algebraStep("annihilation()", "Annihilation")
            self.algebraStep("identity()", "Identity")
            prev_exp = exp
            exp = self.getExpression()
        self.fp.addRow(self.getExpression(), "Simplified Disjunctive Normal Form")

        self.root.adjacency()
        self.fp.addRow("{} terms".format(len(self.root.children)), "Adjacency")

        # implicit commutation step
        prev_exp = ""
        while exp != prev_exp:
            self.algebraStep("idempotence()", "Idempotence")
            self.algebraStep("complement()", "Complement")
            self.algebraStep("annihilation()", "Annihilation")
            self.algebraStep("identity()", "Identity")
            prev_exp = exp
            exp = self.getExpression()


        self.fp.addRow(self.getExpression(), "CDNF")

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


