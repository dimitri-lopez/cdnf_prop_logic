#!/usr/bin/env python3

import sys
from parse import *
from binary_expression import *
from special_characters import *
from node import *

class Sentence:
    def __init__(self, sent = "", operator = "", literal = False):
        self.sent = sent
        self.operator = operator
        self.literal = literal

def printTree(statement, level):
    print(("|   " * level) + statement)


operators = ["&", "|"] #TODO ads
def parse(s, level, parentNode, exp):
    sentence =  s.sent
    printTree("Sentence: {}".format(sentence), level)
    printTree("---------------------", level)
    index = 0
    to_eval = []
    node = Node("", parentNode, [])

    if exp.getRoot() is None: exp.setRoot(node)
    if parentNode is not None: parentNode.addChild(node)

    # exp.print()
    # print("Start:")
    # print(node)

    if s.operator == "~": # Entire Sentence is negate. Evaluate inner sentence
        node.setValue("~")
        to_eval.append(Sentence(sentence[1:]))
        index = len(sentence)
    if s.literal: # A literal, no need to do further parsing
        printTree("This sentence is a literal!", level)
        return

    while index < len(sentence):
        char = sentence[index]
        if char == "(": # TODO need to check ahead to ensure that a binary operator exists after it
            matchingIndex = getEnclosingParantheses(sentence, index)
            checkForBinaryOperator(sentence, matchingIndex)
            to_eval.append(Sentence(sentence[index + 1:matchingIndex])) # not including parantheses
            printTree("Sub-Sent: {}".format(sentence[index + 1:matchingIndex]), level)

            index = matchingIndex + 1; continue
        elif char in operators:
            if s.operator == "": s.operator = char
            elif char != s.operator:
                raise Exception("Invalid propositional logic expression. Undefined behavior when mixing operators. Try wrapping things in parantheses.")
            node.setValue(char)
            printTree("Operator: {}".format(char), level)
        elif char == "~": # treat as if entire thing is wrapped in () eg. ~A -> (~A)
            printTree("Negation: {}".format(char), level)
            lastNegSentIndex = getNegationSentence(sentence, index)
            to_eval.append(Sentence(sentence[index:(lastNegSentIndex + 1)], "~", False))
            index = lastNegSentIndex + 1; continue
        elif char != " ": # linear search to get entire constant name
            endConstIndex = getConst(sentence, index)
            # TODO this is putting a literal into the subsentence?
            # idk if that is the right thing to do? I don't think it is. Maybe add a rec
            constant = sentence[index:endConstIndex + 1]
            # constant = sentence[index:endConstIndex]
            if node.getValue() == "" and endConstIndex == len(sentence) - 1: # this is a literal
                node.setValue(constant)
            else:
                node.addChild(Node(constant, node, []))
            printTree("Constant: {}".format(constant), level)
            # to_eval.append(Sentence(sentence[index:(endCharIndex + 1)], "", True))
            index = endConstIndex + 1; continue

        elif char != " ":
            raise Exception("Encountered weird character {}.".format(char))
        index += 1
        # parentNode.addChild(node)

    # print(("|   " * level) + "Sentence: {}".format(sentence))
    # print("End:")
    # print(node)
    # input("...")

    # print("EVAL: {}".format(to_eval))
    for subs in to_eval:
        parse(subs, level + 1, node, exp)



def main():
    # file1 = open("./sample_input/small_neg.txt")
    file1 = open(str(sys.argv[1]))
    # file1 = open("./sample_input/small_example.txt")
    # file1 = open("./sample_input/bad_chars.txt")
    sentence = file1.readlines()[0]
    sentence = getWorkingString(sentence)
    validChars(sentence)
    print("Original Sentence: {}".format(sentence))
    exp = BinaryExpression()
    s = Sentence(sentence)
    parse(s, 0, None, exp)
    print("------------ Finished Parsing: -------------")

    exp.clean()
    exp.print()
    print("Original Sentence:  {}".format(sentence))
    print("Converted Sentence: {}".format(exp.getExpression()))
    # exp.nnf()
    exp.applyOperations()
    print("New Sentence: {}".format(exp.getExpression()))



main()
