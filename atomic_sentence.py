#!/usr/bin/env python3

from parse import *

class Sentence:
    def __init__(self, rep, literal):
        self.rep = rep
        self.literal = literal



operators = ["&", "|"] #TODO ads
def parse(sentence, level):
    print(("    " * level) + "Sentence: {}".format(sentence))
    print(("    " * level) + "---------------------")
    index = 0
    sub_sentences = []
    operator = ""

    if sentence[0] == "~": # Entire sentence is negated
        lastNegSentIndex = getNegationSentence(sentence, 0)
        if lastNegSentIndex == (len(sentence) - 1):
            print(("    " * level) + "Negation Sentence!!!")
            index = len(sentence) # skip for loop



    while index < len(sentence):
        char = sentence[index]
        if char == "(":
            matchingIndex = getEnclosingParantheses(sentence, index)
            sub_sentences.append((index + 1, matchingIndex))
            print(("    " * level) + "Sub-Sent: {}".format(sentence[index + 1:matchingIndex]))

            index = matchingIndex + 1; continue
        elif char in operators:
            if operator == "": operator = char
            elif char != operator:
                raise Exception("Invalid propositional logic expression. Undefined behavior when mixing operators. Try wrapping things in parantheses.")
            print(("    " * level) + "Operator: {}".format(char))
        elif char == "~": # treat as if entire thing is wrapped in () eg. ~A -> (~A)
            print(("    " * level) + "Negation: {}".format(char))
            lastNegSentIndex = getNegationSentence(sentence, index)
            sub_sentences.append((index, lastNegSentIndex + 1))
            index = lastNegSentIndex + 1; continue
        elif char != " ": # linear search to get entire constant name
            endCharIndex = getConst(sentence, index)
            sub_sentences.append((index, endCharIndex + 1))
            index = endCharIndex + 1; continue

            print(("    " * level) + "Constant: {}".format(char))
        elif char != " ":
            raise Exception("Encountered weird character {}.".format(char))

        index += 1
    for subs in sub_sentences:
        parse(sentence[subs[0]:subs[1]], level + 1)



def main():
    file1 = open("./sample_input/example.txt")
    # file1 = open("./sample_input/bad_chars.txt")
    sentence = file1.readlines()[0]
    sentence = getWorkingString(sentence)
    validChars(sentence)
    print("Original Sentence: {}".format(sentence))
    parse(sentence, 0)

main()
