#!/usr/bin/env python3

from special_characters import *

# TODO Distribution
# TODO Complement
# TODO Identity
# TODO Annihilation
# TODO

class Node:
    def __init__(self, value, parent, children):
        self.value = value
        self.parent = parent
        self.children = children
        self.expression = None
    def setValue(self, v):
        self.value = v
        self.clearExpression()
    def clearExpression(self):
        self.expression = None
        if self.parent != None:
            self.parent.clearExpression()
    def getValue(self):
        return self.value
    def addChild(self, child):
        self.children.append(child)
        self.children.sort() # This essentially does commutation
    def removeChild(self, index):
        self.clearExpression()
        return self.children.pop(index)
    def isLiteral(self):
        return len(children) == 0
    def __repr__(self):
        string = "Value: {}\n".format(self.value)
        for i in self.children:
            string += "\tChildren: {}\n".format(i.value)
        return string
    def __lt__(self, other):
        return self.getExpression() < other.getExpression()
    def getExpression(self): # TODO fix this so it doesn't get updated so often
        # print("v: {}".format(self.getValue()))
        if self.expression != None: return self.expression
        value = self.getValue()

        if value == "~":
            assert(len(self.children) == 1)
            if self.children[0].getValue() in binary_operators:
                self.expression = "~({})".format(self.children[0].getExpression())
            else:
                self.expression = "~{}".format(self.children[0].getExpression())
        elif value in binary_operators:
            join_str = " {} ".format(value)
            children_strs = []
            for i in self.children:
                child_str = i.getExpression()
                if len(i.children) > 1: # wrap all non literals in parantheses
                    child_str = "({})".format(child_str)
                children_strs.append(child_str)
            children_strs.sort() # This will make disjuncts later easier to parse
            self.expression = join_str.join(children_strs)
        else:
            assert(len(self.children) == 0 or self.value == "")
            self.expression = self.getValue()

        return self.expression

    def cleanNode(self):
        if self.getValue() in ["&", "|"] and len(self.children) == 1:
            self.setValue(self.children[0].getValue())
            self.children = self.children[0].children
    def association(self):
        pass
    def commutation(self):
        pass

    def double_negation(self):
        if self.getValue() != "~": return False
        if self.children[0].getValue() != "~": return False
        self.setValue(self.children[0].children[0].getValue())
        self.children[0].children = []
        self.children = []
        return True

    def neg_demorgan(self):
        if self.getValue() != NOT: return False
        if self.children[0].getValue() not in [AND, OR]: return False

        cvalue = self.children[0].getValue()
        gchildren = self.children[0].children
        self.children = []
        for i in range(len(gchildren)):
            negNode = Node(NOT, self, [])
            negNode.addChild(gchildren[i])
            self.addChild(negNode)

        if cvalue == AND:  self.setValue(OR)
        elif cvalue == OR: self.setValue(AND)

        return True

    def distribution(self):
        pass

    # A & A -> A
    def idempotence(self):
        expressions = set()
        index = 0
        changed = False
        while index < len(self.children):
            exp = self.children[index].getExpression()
            if exp in expressions:
                self.removeChild(index)
                changed = True
                continue
            expressions.add(exp)
            index += 1
        self.cleanNode()
        return changed
    # A & ~A -> CONT
    # TODO: Aris requires that this must be done in two steps.
    # First by association and then you can apply the relevant step
    def complement(self):
        if self.getValue() not in [AND, OR]: return False
        exps = set()
        nexps = set()

        to_remove = set()
        index = 0
        for child in self.children:
            if child.getValue() == "~":
                cexp = child.children[0].getExpression()
                if cexp in exps: to_remove.add(exp) # seen in non negated
                nexps.add(cexp)
            else:
                exp = child.getExpression()
                if exp in nexps: to_remove.add(exp) # seen in negations
                exps.add(exp)

        print("to_remove: {}".format(to_remove))
        index = 0
        if len(to_remove) == 0: return False
        while index < len(self.children): # remove everything within to_remove
            child = self.children[index]
            if child.getExpression() in to_remove:
                self.removeChild(index)
                continue
            if child.getValue() == NOT and child.children[0].getExpression() in to_remove:
                self.removeChild(index)
                continue
            index += 1
        if self.getValue() == AND:  self.addChild(Node(CONT, self, []))
        elif self.getValue() == OR: self.addChild(Node(TAUT, self, []))
        self.cleanNode()

        return True
    # A & TAUT -> A
    # A | CONT -> A
    def identity(self):
        if self.getValue() not in [AND, OR]: return False

        value = False
        index = 0
        while index < len(self.children): # remove all TAUT
            child = self.children[index]
            if self.getValue() == AND and child.getValue() == TAUT:
                self.removeChild(index)
                value = True
                continue
            elif self.getValue() == OR and child.getValue() == CONT:
                self.removeChild(index)
                value = True
                continue
            index += 1
        self.cleanNode()
        return value
    def annihilation(self):
        if self.getValue() not in [AND, OR]: return False

        for i in self.children:
            if self.getValue() == AND and i.getValue() == CONT:
                # continue if child value is cont
                self.children = []
                self.setValue(CONT)
                return True
            elif self.getValue() == OR and i.getValue() == TAUT:
                # continue if child value is cont
                self.children = []
                self.setValue(TAUT)
                return True
        return False
    def inverse(self):
        if self.getValue() != "~": return False
        if self.children[0].getValue() == "#":
            self.setValue("^")
            self.children = []
        elif self.children[0].getValue() == "^":
            self.setValue("#")
            self.children = []
        return True
    # TODO make sure to run idempotence before running this. Otherwise weird
    # shit might happen?
    def absorption(self):
        if self.getValue() not in [AND, OR]: return False
        top_exps = set()
        for i in self.children:
            top_exps.add(i.getExpression())

        value = False
        index = 0
        while index < len(self.children):
            i = self.children[index]
            if not ((self.getValue() == AND and i.getValue() == OR) \
                 or (self.getValue() == OR  and i.getValue() == AND)):
                index += 1; continue;

            found = False
            for gchild in i.children:
                gexp = gchild.getExpression()
                if gexp in top_exps:
                    found = True
                    value = True
                    break
            if found:
                self.removeChild(index)
                continue
            index += 1

        return value

    def reduction(self):
        pass
    def adjacency(self):
        pass
