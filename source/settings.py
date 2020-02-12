import numpy as np

pathToDictionary = './log/dictionary.d'
pathToLog = './log/plain.txt'
pathToMathematica = './log/mathematica'
pathToLastID = './log/lastId.txt'

def printpaths():
    print(pathToDictionary)

def init(big):
    global partialSumsIndices
    partialSumsIndices = None
    #
    # global pathToDictionary
    # global pathToLog
    # global pathToMathematica
    # global pathToLastID

    if big:
        global pathToDictionary
        pathToDictionary = './amazonLog/dictionary.d'
        global pathToLog
        pathToLog = './amazonLog/plain.txt'
        global pathToMathematica
        pathToMathematica = './amazonLog/mathematica'
        global pathToLastID
        pathToLastID = './amazonLog/lastId.txt'

    global lastID

    with open(pathToLastID, 'r') as inp:
        lastID = int(eval(inp.read()))
