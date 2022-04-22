#!/usr/bin/env python3
import re


def removeSpaces(string):
    return string.repalace(" ", "")

# remove the special characthers and replace with plain text
def toPlainText(string):
    new_string = string.replace("∧", "&")
    new_string = new_string.replace("∨", "|")
    new_string = new_string.replace("¬", "~")
    return new_string


# remove the plain text operators with their special character equivalents
def toSpecialChar(string):
    new_string = string.replace("&", "∧")
    new_string = new_string.replace("|", "∨")
    new_string = new_string.replace("~", "¬")
    return new_string

def validChars(string):
    regex = re.compile(r'[ \(\)a-zA-Z0-9&\|~]')
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
            endCharIndex = getConst(sentence, index)
            return endCharIndex
    raise Exception("Invalid propositional logic expression. Negation operator is missing terms.")



# includes the first letter of the constant. White space is used as a delimiter.
# The index returned will include the last char of the constant.
def getConst(sentence, index):
    consts = [sentence[index]]
    index += 1
    while index < len(sentence):
        char = sentence[index]

        illegal_chars = ["(", ")", "^", "⊤", "~"]
        operators = ["&", "|"]
        if char in illegal_chars:
            raise Exception("Invalid propositional logic expression inputted.")
        elif char in operators or char == " ": # do a linear search to make sure that an operator is found
            for j in sentence[index:]:
                if j == " " or j in operators:
                    continue
                else:
                    raise Exception("Invalid propositional logic expression inputted. Missing a binary operator after a constant")
            return index

        index += 1
    return index - 1 # constant is the entire sentence
