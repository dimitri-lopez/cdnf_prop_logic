#!/usr/bin/env python3

from special_characters import *
from misc import *
import copy

# TODO Distribution
# TODO Complement
# TODO Identity
# TODO Annihilation

class Node:
    def __init__(self, value, parent, children):
    #     if type(value) == Node("", None, []): # copy constructor
    #         self.copyConstructor(value, parent)
    #     else: self.defaultConstructor(value, parent, children)
    # def defaultConstructor(value, parent, children):
        self.value = value
        self.parent = parent
        self.children = children
        self.expression = None
    def copy(self, parent):
        new_node = Node(self.getValue(), parent, [])
        to_add = []
        for i in self.children:
            to_add.append(i.copy(new_node))
        for i in to_add:
            new_node.addChild(i)
        return new_node
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
        self.clearExpression()
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
    def getExpression(self):
        if self.expression != None: return self.expression
        value = self.getValue()

        if value == NOT:
            assert(self.children[0].getValue() != "")
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
        if self.getValue() in [AND, OR] and len(self.children) == 1:
            self.setValue(self.children[0].getValue())
            self.children = self.children[0].children
    def association(self):
        pass
    def commutation(self):
        pass

    def double_negation(self):
        if self.getValue() != NOT: return False
        if self.children[0].getValue() != NOT: return False
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

    # This is not going to do all the distribution at once. Just a single application at a time
    def distribution(self):
        if self.getValue() not in [AND, OR]: return False
        found = False
        for i in self.children:
            if i.getValue() in [AND, OR] and i.getValue() != self.getValue():
                found = True; break
        if not found: return False

        # print("distribuuuuuuuuuuuuution")
        # print(self.getExpression())
        # return True

        kids = self.children
        self.children = []
        kid_lengths = []
        for i in kids:
            lchild = len(i.children)
            if lchild in [0, 1]: kid_lengths.append(1)
            else: kid_lengths.append(lchild)

        inside_operator = self.getValue()
        outside_operator = kids[0].getValue()

        self.setValue(outside_operator) # flop the values
        new_parent = self

        # Add nodes for the new distributions
        sub_node_vals = iterate_number_bases(kid_lengths)
        for index_set in sub_node_vals:
            new_node = Node(inside_operator, new_parent, [])
            for j in range(len(index_set)):
                kid_index = index_set[j]
                if len(kids[j].children) in [0, 1]: new_node.addChild(kids[j].copy(new_parent)) # for literals and NOT
                else: new_node.addChild(kids[j].children[kid_index].copy(new_parent))
            new_parent.addChild(new_node)
        return True


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
            if child.getValue() == NOT:
                cexp = child.children[0].getExpression()
                if cexp in exps: to_remove.add(exp) # seen in non negated
                nexps.add(cexp)
            else:
                exp = child.getExpression()
                if exp in nexps: to_remove.add(exp) # seen in negations
                exps.add(exp)

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
        if len(self.children) == 0:
            if self.getValue() == AND: self.addChild(Node(TAUT, self, []))
            if self.getValue() == OR: self.addChild(Node(CONT, self, []))

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
        if self.getValue() != NOT: return False
        if self.children[0].getValue() == TAUT:
            self.setValue(CONT)
            self.children = []
        elif self.children[0].getValue() == CONT:
            self.setValue(TAUT)
            self.children = []
        else: return False
        return True

    # make sure to run idempotence before running this. Otherwise weird shit
    # might happen?
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
    # This should really only be called on the root node.
    def adjacency(self):
        if self.getValue() not in [AND, OR]: return False
        # Gather Literals
        literals = {}
        for i in self.children:
            if len(i.children) == 0: # subcase when the term has only a literal
                literals[i.getExpression()] = i
            for j in i.children:
                literals[j.getExpression()] = j

        # Duplicate nodes
        nodes_to_add = []
        index = 0
        while index < len(self.children):
            i = self.children[index]
            new_node = Node(i.getValue(), self, [])
            unused_literals = literals.copy()
            if len(i.children) in [0, 1]: # if one of the terms is a literal
                if self.getValue() == AND: new_node.setValue(OR) # set to the correct value
                elif self.getValue() == OR: new_node.setValue(AND) # set to the correct value
                del unused_literals[i.getExpression()]
                for j in unused_literals.values():
                    new_node.addChild(j.copy(new_node))
                nodes_to_add.append(new_node)
                self.removeChild(index)
                print("Literal value: {}".format(new_node.getExpression()))
                continue
            # for j in i.children:
            #     jexp = j.getExpression()
            #     if jexp in unused_literals:
            #         del unused_literals[jexp]
            #         new_node.addChild(j.copy(new_node))
            # for j in unused_literals.values(): # add non-negated literals
            #     i.addChild(j.copy(i))
            # for j in unused_literals.values(): # add negated literals
            #     if j.getValue() == NOT:
            #         new_node.addChild(j.children[0].copy(new_node)) # Get rid of a negation
            #     else:
            #         to_be_negated = j.copy(None)
            #         neg_node = Node(NOT, new_node, [to_be_negated])
            #         to_be_negated.parent = neg_node
            #         new_node.addChild(neg_node)

            # nodes_to_add.append(new_node)
            index += 1

        # print("nodes_to_add: {}".format(nodes_to_add))
        for i in nodes_to_add:
            print("adding: {}".format(i))
            self.addChild(i)
        return True
    def association(self): # This is to get rid of things like (A|B) | C
        if self.getValue() not in [AND, OR]: return False

        changed = False
        index = 0
        to_add = []
        while index < len(self.children):
            i = self.children[index]
            if self.getValue() == i.getValue(): # matching binary operator
                print("matching binary operator")
                for j in i.children:
                    j.parent = self
                    to_add.append(j)
                changed = True
                self.removeChild(index)
                continue
            index += 1
        for i in to_add:
            self.addChild(i)
        return changed
