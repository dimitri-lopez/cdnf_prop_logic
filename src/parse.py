#!/usr/bin/env python3
import re
from special_characters import *


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