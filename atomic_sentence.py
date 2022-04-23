#!/usr/bin/env python3

from parse import *

class Node:
    def __init__(self, value = "", children = []):
        self.value = value
        self.children = children
    def addChild(self, child):
        children.append(child)
    def isLiteral(self):
        return len(children) == 0

class BinaryExpression:
    def __init__(self):
        self.root = None
        self.literals = set()
    def setRoot(self, root):
        self.root = root
    def getRoot(self):
        return self.root
    def addLiteral(self, literal):
        self.literals.add(literal)
    def getEval(self): # TODO
        return


class Sentence:
    def __init__(self, sent = "", operator = "", literal = False):
        self.sent = sent
        self.operator = operator
        self.literal = literal



operators = ["&", "|"] #TODO ads
def parse(s, level, parentNode, exp):
    sentence =  s.sent
    print(("|   " * level) + "Sentence: {}".format(sentence))
    print(("|   " * level) + "---------------------")
    index = 0
    to_eval = []
    node = Node()

    if exp.getRoot() is None: exp.setRoot(node)
    if parentNode is not None: parentNode.add

    if s.operator == "~": # Entire Sentence is negate. Evaluate inner sentence
        to_eval.append(Sentence(sentence[1:]))
        index = len(sentence)
    if s.literal: # A literal, no need to do further parsing
        print(("|   " * level) + "This sentence is a literal!")
        return

    while index < len(sentence):
        char = sentence[index]
        if char == "(":
            matchingIndex = getEnclosingParantheses(sentence, index)
            to_eval.append(Sentence(sentence[index + 1:matchingIndex])) # not including parantheses
            print(("|   " * level) + "Sub-Sent: {}".format(sentence[index + 1:matchingIndex]))

            index = matchingIndex + 1; continue
        elif char in operators:
            if s.operator == "": s.operator = char
            elif char != s.operator:
                raise Exception("Invalid propositional logic expression. Undefined behavior when mixing operators. Try wrapping things in parantheses.")
            print(("|   " * level) + "Operator: {}".format(char))
        elif char == "~": # treat as if entire thing is wrapped in () eg. ~A -> (~A)
            print(("|   " * level) + "Negation: {}".format(char))
            lastNegSentIndex = getNegationSentence(sentence, index)
            to_eval.append(Sentence(sentence[index:(lastNegSentIndex + 1)], "~", False))
            index = lastNegSentIndex + 1; continue
        elif char != " ": # linear search to get entire constant name
            endCharIndex = getConst(sentence, index)
            # TODO this is putting a literal into the subsentence?
            # idk if that is the right thing to do? I don't think it is. Maybe add a rec
            print(("|   " * level) + "Constant: {}".format(sentence[index:endCharIndex + 1]))
            to_eval.append(Sentence(sentence[index:(endCharIndex + 1)], "", True))
            index = endCharIndex + 1; continue

        elif char != " ":
            raise Exception("Encountered weird character {}.".format(char))

        index += 1
    for subs in to_eval:
        parse(subs, level + 1, None, exp)



def main():
    # file1 = open("./sample_input/small_neg.txt")
    file1 = open("./sample_input/example.txt")
    # file1 = open("./sample_input/bad_chars.txt")
    sentence = file1.readlines()[0]
    sentence = getWorkingString(sentence)
    validChars(sentence)
    print("Original Sentence: {}".format(sentence))
    exp = BinaryExpression()
    s = Sentence(sentence)
    parse(s, 0, None, exp)

main()
