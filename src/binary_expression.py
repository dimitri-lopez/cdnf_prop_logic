#!/usr/bin/env python3

binary_operators = ["&", "|"]

class Node:
    def __init__(self, value = "", children = []):
        self.value = value
        self.children = children
        self.expression = ""
    def addChild(self, child):
        self.children.append(child)
    def isLiteral(self):
        return len(children) == 0
    def __repr__(self):
        string = "Value: {}\n".format(self.value)
        for i in self.children:
            string += "\tChildren: {}\n".format(i.value)
        return string
    def __lt__(self, other):
        return self.expression < other.expression

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
            childrenStr += "{}, ".format(i.value)

        print(("|   " * level) + "Value: {} - Children ({}): {}".format(currentNode.value, len(currentNode.children), childrenStr))
        for i in currentNode.children:
            if len(i.children) > 0: self.print(i, level + 1)
    def clean(self): # A user can have levels that are just nested parantheses without any actual information
        # print("testing equality {}".format(self.root.value == ""))
        if self.root.value == "":
            assert(len(self.root.children) == 1)
            self.root = self.root.children[0]
        self.removeEmpties(self.root)
        self.getExpression() # Build the tree from the bottom, then we are gonna sort thie lists
        self.sortByExpression()
        # TODO Sort the bottom nodes


    def removeEmpties(self, parentNode):
        if parentNode.value == "":
            assert(len(parentNode.children) == 1)
        for index in range(len(parentNode.children)):
            i = parentNode.children[index]
            if i.value == "": # remove this node
                assert(len(i.children) == 1)
                parentNode.children[index] = i.children[0]
                i = parentNode.children[index]
            self.removeEmpties(i)
    def getExpression(self):
        # if self.expression is None:
        self.nodeExpression(self.root)
        return self.expression

    def nodeExpression(self, node):
        value = node.value
        string = ""

        if value == "~":
            assert(len(node.children) == 1)
            if node.children[0].value in binary_operators:
                string = "~({})".format(self.nodeExpression(node.children[0]))
            else:
                string = "~{}".format(self.nodeExpression(node.children[0]))
        elif value in binary_operators:
            join_str = " {} ".format(value)
            children_strs = []
            for i in node.children:
                child_str = self.nodeExpression(i)
                if len(i.children) > 1: # wrap all non literals in parantheses
                    child_str = "({})".format(child_str)
                children_strs.append(child_str)
            children_strs.sort() # This will make disjuncts later easier to parse
            string = join_str.join(children_strs)
        else:
            assert(len(node.children) == 0)
            string = node.value


        node.expression = string
        if node is self.root:
            self.expression = string

        return string

    def sortByExpression(self, node = None):
        if node is None: node = self.root
        for i in node.children:
            self.sortByExpression(i)
        node.children.sort()

    def applyOperations(self, node = None):
        if node is None: node = self.root
        self.inverse(node)
        self.double_negation(node)
        for i in node.children:
            self.applyOperations(i)


    def inverse(self, node):
        if node.value != "~": return False
        if node.children[0].value == "#":
            node.value = "^"
            node.children = []
        elif node.children[0].value == "^":
            node.value = "#"
            node.children = []
        return True

    def double_negation(self, node):
        print(node)
        if node.value != "~": return False
        if node.children[0].value != "~": return False
        node.value = node.children[0].children[0].value
        node.children[0].children = []
        node.children = []
        return True
