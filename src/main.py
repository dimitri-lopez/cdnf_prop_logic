#!/usr/bin/env python3

import sys
from parse import *
from propostional_expression import *
from special_characters import *
from node import *
from fancy_print import *

def main():
    file1 = open(str(sys.argv[1]))
    sentence = file1.readlines()[0]
    sentence = getWorkingString(sentence)
    validChars(sentence)
    exp = PropExpression() # create expression object
    fp = FancyPrint(2)
    exp.addFancyPrint(fp)

    fp.addRow(sentence, "Original Sentence")

    # Parse user input
    s = Sentence(sentence)
    parse(s, 0, None, exp)

    exp.clean()
    fp.addRow(exp.getExpression(), "Commutation")
    exp.cdnf()

    fp.print()

main()
