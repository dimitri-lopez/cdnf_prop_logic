#!/usr/bin/env python3
import re
from special_characters import *
from node import *


def removeSpaces(string):
    return string.repalace(" ", "")

# remove the special characthers and replace with plain text
def toPlainText(string):
    new_string = string.replace("∧", "&")
    new_string = new_string.replace("∨", "|")
    new_string = new_string.replace("¬", "~")
    new_string = new_string.replace("⊥", "^")
    new_string = new_string.replace("⊤", "#")
    return new_string


# remove the plain text operators with their special character equivalents
def toSpecialChar(string):
    new_string = string.replace("&", "∧")
    new_string = new_string.replace("|", "∨")
    new_string = new_string.replace("~", "¬")
    new_string = new_string.replace("^", "⊥")
    new_string = new_string.replace("#", "⊤")
    return new_string

def validChars(string):
    regex = re.compile(r'[ \(\)a-zA-Z0-9&\|~^#]')
    for i in string:
        if regex.search(i) is None:
            raise Exception("Invalid character {} found within propositional expression.".format(i))
    paran_count = 0
    for i in string:
        if i == "(":   paran_count += 1;
        elif i == ")": paran_count -= 1;
        if paran_count < 0:
            raise Exception("Invalid expression. Unmatched parantheses.")

def getWorkingString(string):
    new_string = string.strip()
    # new_string = new_string.replace(" ", "")
    new_string = new_string.replace("\n", "")
    new_string = new_string.replace("\t", "")
    return toPlainText(new_string)

# finds the index of the closing parantheses, returns the index on top of the
# closing parantheses. So for "()" it will return 1.
def getEnclosingParantheses(string, index):
    count = 1
    for i in range(index + 1, len(string)):
        char = string[i]
        if char == "(":
            count += 1
        elif char == ")":
            count -= 1
            if count < 0: raise Exception("Invalid propositional logic expression inputted. Check parantheses")
            elif count == 0: return i
    raise Exception("Invalid propositional logic expression inputted. Check parantheses")

# After a negation one of two things can happen
# 1. We run into a constant
# 2. We run into a parantheses
# 3. We run into another negation symbol
# Will return the index of the last included index
def getNegationSentence(sentence, index):
    assert(sentence[index] == "~")
    index += 1

    illegal_chars = [")", "&", "|"]
    while index < len(sentence):
        char = sentence[index]
        if char == "~":
            return getNegationSentence(sentence, index) # return the same end char
        elif char == "(":
            matchingIndex = getEnclosingParantheses(sentence, index)
            return matchingIndex + 1 # because enclosing returns an index on top of )
        elif char in illegal_chars:
            raise Exception("Invalid propositional logic expression. Illegal character {} encountered in negation term.".format(char))
        elif char != " ":
            # print("debug: {} - {}".format(index, sentence))
            endCharIndex = getConst(sentence, index)
            # print("Const found: {}".format(sentence[index:endCharIndex + 1]))

            return endCharIndex
    raise Exception("Invalid propositional logic expression. Negation operator is missing terms.")



# includes the first letter of the constant. White space is used as a delimiter.
# The index returned will include the last char of the constant.
def getConst(sentence, index):
    # assert(False)
    # print("get const debug: {} - {}".format(index, sentence))
    original_index = index
    index += 1
    while index < len(sentence):
        char = sentence[index]

        illegal_chars = ["(", ")", "^", "⊤", "~"]
        operators = ["&", "|"]
        if char in illegal_chars:
            raise Exception("Invalid propositional logic expression inputted. Illegal character after a constant.")
        elif char in operators or char == " ": # do a linear search to make sure that an operator is found
            for j in sentence[index:]:
                if j == " ":
                    continue
                elif j in operators: # A proper expression
                    break
                else:
                    raise Exception("Invalid propositional logic expression inputted. Missing a binary operator after a constant. Found {} instead".format(j))
            return index - 1

        index += 1
    return index - 1 # constant is the entire sentence

# This is called when a set of parantheses is found, trying to ensure that it
# runs into a binary operator at some point
def checkForBinaryOperator(sentence, index):
    operators = ["&", "|"]
    illegal_chars = ["(", ")", "^", "⊤", "~"]
    index += 1; # original index is a )
    for char in sentence[index:]:
        if char in operators: return
        if char in illegal_chars:
            raise Exception("Invalid propositional logic expression inputted. Missing a binary operator after a set of parantheses. Found {} instead".format(char))
    return




class Sentence:
    def __init__(self, sent = "", operator = "", literal = False):
        self.sent = sent
        self.operator = operator
        self.literal = literal

def printTree(statement, level):
    return
    print(("|   " * level) + statement)


def parse(s, level, parentNode, exp):
    sentence = s.sent.strip()
    printTree("Sentence: {}".format(sentence), level)
    printTree("s.operator: {}".format(s.operator), level)
    printTree("---------------------", level)
    index = 0
    to_eval = []
    node = Node("", parentNode, [])

    if exp.getRoot() is None: exp.setRoot(node)
    if parentNode is not None: parentNode.children.append(node)


    if s.operator == NOT: # Entire Sentence is negate. Evaluate inner sentence
        node.setValue(NOT)
        parse(Sentence(sentence[1:]), level + 1, node, exp)
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
        elif char in [AND, OR]:
            if s.operator == "": s.operator = char
            elif char != s.operator:
                raise Exception("Invalid propositional logic expression. Undefined behavior when mixing operators. Try wrapping things in parantheses.")
            node.setValue(char)
            printTree("Operator: {}".format(char), level)
        elif char == NOT: # treat as if entire thing is wrapped in () eg. ~A -> (~A)
            printTree("Negation: {}".format(char), level)
            lastNegSentIndex = getNegationSentence(sentence, index)
            to_eval.append(Sentence(sentence[index:(lastNegSentIndex + 1)], NOT, False))
            index = lastNegSentIndex + 1; continue
        elif char != " ": # linear search to get entire constant name
            endConstIndex = getConst(sentence, index)
            # TODO this is putting a literal into the subsentence?
            # idk if that is the right thing to do? I don't think it is. Maybe add a rec
            constant = sentence[index:endConstIndex + 1]
            if node.getValue() == "" and endConstIndex == len(sentence) - 1: # this is a literal
                node.setValue(constant)
            else:
                node.addChild(Node(constant, node, []))
            index = endConstIndex + 1; continue

        elif char != " ":
            raise Exception("Encountered weird character {}.".format(char))
        index += 1

    for subs in to_eval:
        parse(subs, level + 1, node, exp)
