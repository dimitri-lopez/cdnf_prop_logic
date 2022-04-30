#!/usr/bin/env python3

from tabulate import tabulate
from parse import *

class FancyPrint:
    def __init__(self, columns):
        self.rows = []

    def addRow(self, first, second):
        self.rows.append([first, second])
        self.print()
    def print(self):
        # for i in range(len(self.rows)):
        #     self.rows[i][0] = toSpecialChar(self.rows[i][0])
        print(tabulate(self.rows, colalign = ("right",)))
        # for i in self.rows:
        #     print(i[1] + ": " + i[0])

