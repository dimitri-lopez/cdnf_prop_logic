#!/usr/bin/env python3

from tabulate import tabulate
from parse import *

class FancyPrint:
    def __init__(self, columns):
        self.rows = []

    def addRow(self, first, second):
        self.rows.append([first, second])
    def print(self):
        print(tabulate(self.rows, colalign = ("right",)))
