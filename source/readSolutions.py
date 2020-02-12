import datetime
import numpy as np

from indexingFunctions import *

pathToDictionary = './log/dictionary.d'

def readFromDictionary(id, filename=pathToDictionary):
    dct = dict()
    with open(filename, 'r') as inp:
        dct = eval(inp.read())

    return dct[id]
