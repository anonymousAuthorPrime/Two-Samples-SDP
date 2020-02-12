import datetime
import numpy as np

pathToMetaLog = './log/metaPlain.txt'
pathToMetaDictionary = './log/metaDictionary.d'

def emptyMetaDictionary(filename=pathToMetaDictionary):
    dct = dict()

    with open(filename, 'w') as out:
        out.write(str(dct))

    return

def emptyMetaLog(filename=pathToMetaLog):
    with open(filename, 'w') as out:
        out.write('')

    return

def printTableSolutions(n, lopt, liopt, alsol, err, log=False, metaDict=None, stopPrec=-1):
    scl = "logarithmic" if log else "linear"
    print("\nTable for n =", n, "and opt step =", err, ", scale", scl)
    print("     and stop precision =", stopPrec, "\n")

    print(" i - o |", end="")
    for opt in lopt:
        print("   {:4.2f}  ".format(opt), end="")
    print()
    print("--------", end="")
    for opt in lopt:
        print("---------", end="")
    print()

    for iopt in liopt:
        print("  {:3d}  |".format(iopt), end="")
        for opt in lopt:
            toPr = alsol[(opt, iopt)]
            toPr = np.abs(toPr[0])
            print("   {:4.2f}  ".format(toPr), end="")
        print()

        print("       |".format(iopt), end="")
        for opt in lopt:
            toPr = alsol[(opt, iopt)]
            toPr = toPr[1]
            metaStr = " " if metaDict == None else \
                        ("*" if metaDict[(opt, iopt)] else " ")
            print(" "+metaStr+" {:4d}  ".format(toPr), end="")
        print("\n")

def getStringTableSolutions(n, lopt, liopt, alsol, metaDict=None):
    rstr = "\n\n"

    rstr += " i - o |"
    for opt in lopt:
        rstr += "   {:4.2f}  ".format(opt)
    rstr += "\n--------"
    for opt in lopt:
        rstr += "---------"
    rstr += "\n"

    for iopt in liopt:
        rstr += "  {:3d}  |".format(iopt)
        for opt in lopt:
            toPr = alsol[(opt, iopt)]
            toPr = np.abs(toPr[0])
            rstr += "   {:4.2f}  ".format(toPr)
        rstr += "\n"

        rstr += "       |".format(iopt)
        for opt in lopt:
            toPr = alsol[(opt, iopt)]
            toPr = toPr[1]
            metaStr = " " if metaDict == None else \
                        ("*" if metaDict[(opt, iopt)] else " ")
            rstr += " "+metaStr+" {:4d}  ".format(toPr)
        rstr += "\n\n"

    return rstr

def addToMetaLog(n, lopt, liopt, alsol, err, metaId, filename=pathToMetaLog, log=False, metaDict=None, stopPrec=-1):
    scl = "logarithmic" if log else "linear"
    minLopt = -1 if (lopt == []) else min(lopt)
    maxLopt = -1 if (lopt == []) else max(lopt)

    minLiopt = -1 if (liopt == []) else min(liopt)
    maxLiopt = -1 if (liopt == []) else max(liopt)

    with open(filename, 'a') as out:
        out.write('\n')
        out.write('\n')
        out.write('********************************************************\n')
        out.write(str(datetime.datetime.now()) + '\n')
        out.write('\n')
        out.write('meta-id: ' + str(metaId) + '\n')
        out.write('\n')
        out.write('n: ' + str(n) + '\n')
        out.write('\n')
        out.write('range opt: ' + str(minLopt) + ' - ' + str(maxLopt) + '\n')
        out.write('\n')
        out.write('range iopt: ' + str(minLiopt) + ' - ' + str(maxLiopt) + '\n')
        out.write('\n')
        out.write('opt step: ' + str(err) + '\n')
        out.write('\n')
        out.write('stop precision: ' + str(stopPrec) + '\n')
        out.write('\n')
        out.write('scale ' + scl + '\n')
        out.write('\n')
        rstr = getStringTableSolutions(n, lopt, liopt, alsol, metaDict=metaDict)
        out.write(rstr + '\n')
        out.write('********************************************************\n')
        out.write('\n')
        out.write('\n')

def addToMetaDictionary(n, lopt, liopt, alsol, err, metaId, filename=pathToMetaDictionary, log=False, metaDict=None, stopPrec=-1):
    dct = dict()
    with open(filename, 'r') as inp:
        dct = eval(inp.read())

    dct[metaId] = (datetime.datetime.now(), n, list(lopt), list(liopt), err, log, alsol, metaDict, stopPrec)

    with open(filename, 'w') as out:
        out.write(str(dct))

def saveMetaSolutions(n, lopt, liopt, alsol, err, metaId, filenamel=pathToMetaLog, filenamed=pathToMetaDictionary, log=False, metaDict=None, stopPrec=-1):
    addToMetaDictionary(n, lopt, liopt, alsol, err, metaId, filename=filenamed, log=log, metaDict=metaDict, stopPrec=stopPrec)
    addToMetaLog(n, lopt, liopt, alsol, err, metaId, filename=filenamel, log=log, metaDict=metaDict, stopPrec=stopPrec)

    scl = "logarithmic" if log else "linear"
    print("Solution with n =", n)
    print(" -- lopt =", lopt)
    print(" -- liopt =", liopt)
    print(" -- opt step =", err)
    print(" -- scale", scl)
    print(" saved with meta-id =", metaId, ".")

    return metaId
