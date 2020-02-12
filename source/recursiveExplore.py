import numpy as np
import cvxpy as cp

from xyzImplementation import *

from saveSolutions import *
from saveMetaSolutions import *
from readMetaSolutions import *

def recursiveExplore(n, w, goal=0.6, lowOpt=None, hiOpt=None, iopt=None, opt=None, err=-1, log=False, stopPrec=-1):
    print("Recursive Call with n =", n, ", error = ", err, ", stop precision = ", stopPrec)
    print("and w =", w)
    print("----------------------------------------------------------------\n")
    err = err if err > 0 else 1.0/n
    stopPrec = stopPrec if stopPrec > 0 else 3.0/n
    lopt = []
    liopt = []

    # Setting the exploration space for opt
    lowOpt = 0.0 if (lowOpt == None) else lowOpt
    hiOpt = 1.0 if (hiOpt == None) else hiOpt
    rangeOpt = hiOpt - lowOpt
    m = int(np.ceil(rangeOpt*1.0/err))

    if (opt == None):
        for opt in (lowOpt + err*np.array(list(range(1, m + 1)))):
            if (opt >= stopPrec):
                lopt += [opt]
    else:
        lopt = [opt]

    # Setting the exploration space for iopt
    if (iopt == None):
        for i in range(1, n):
            if (w[i] >= stopPrec):
                liopt += [i]
    else:
        liopt = [iopt]

    alsol = dict()
    metaDict = dict()
    minValue = 1.0
    for iopt in liopt:
        for opt in lopt:
            result = optimize(n, opt, iopt, w, eps=err)
            value = result[0]
            tempId = result[1]
            metaNeeded = False

            if (tempId > 0) and (value < goal):
                result = recursiveExplore(n, w, goal=goal, lowOpt=opt-err, hiOpt=opt, iopt=iopt, err=err/2.0, log=log, stopPrec=stopPrec)
                metaNeeded = True
                value = result[0]

            alsol[(opt, iopt)] = result
            metaDict[(opt, iopt)] = metaNeeded
            minValue = minValue if (tempId < 0) else min(minValue, value)

    printTableSolutions(n, lopt, liopt, alsol, err, metaDict=metaDict, stopPrec=stopPrec)

    metaId = getMetaId() + 1
    saveMetaSolutions(n, lopt, liopt, alsol, err, metaId, metaDict=metaDict, stopPrec=stopPrec)
    print("\n----------------------------------------------------------------")

    return (minValue, metaId)
