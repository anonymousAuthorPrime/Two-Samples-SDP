import datetime
import numpy as np

from indexingFunctions import *
from saveMetaSolutions import *

pathToMetaDictionary = './log/metaDictionary.d'

def readFromMetaDictionary(metaId, filename=pathToMetaDictionary):
    dct = dict()
    with open(filename, 'r') as inp:
        dct = eval(inp.read())

    return dct[metaId]

def getMetaId(filename=pathToMetaDictionary):
    dct = dict()
    with open(filename, 'r') as inp:
        dct = eval(inp.read())

    return len(dct)

def printFromMetaDictionary(metaId, filename=pathToMetaDictionary):
    dct = dict()
    with open(filename, 'r') as inp:
        dct = eval(inp.read())

    params = dct[metaId]
    n = params[1]
    lopt = params[2]
    liopt = params[3]
    err = params[4]
    log = params[5]
    alsol = params[6]
    metaDict = params[7]
    stopPrec = params[8]

    printTableSolutions(n, lopt, liopt, alsol, err, log=log, metaDict=metaDict, stopPrec=stopPrec)
