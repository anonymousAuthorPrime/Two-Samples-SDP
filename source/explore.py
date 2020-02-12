import numpy as np
import cvxpy as cp

from xyzImplementation import *

from saveSolutions import *
from saveMetaSolutions import *
from readMetaSolutions import *

def explore(n, w, opt=None, iopt=None, err=-1, log=False, rel=-1, lowOpt=1.0, lowIopt=-1, maxIters=2500):
    err = err if err > 0 else 1.0/n
    lopt = []
    liopt = []
    m = int(np.ceil(1.0/err))

    if (opt == None):
        if (not log):
            lopt = err*np.array(list(range(1, m + 1)))
        else:
            tempOpt = lowOpt
            while (tempOpt <= 1.0):
              lopt += [tempOpt]
              tempOpt = tempOpt*rel
    else:
        lopt = [opt]

    if (iopt == None):
        if (lowIopt < 0):
            liopt = list(range(1, n - 1))
        else:
            liopt = list(range(lowIopt, n - 1))
    else:
        liopt = [iopt]

    alsol = dict()
    for iopt in liopt:
        for opt in lopt:
            if (not log):
                alsol[(opt, iopt)] = optimize(n, opt, iopt, w, eps=err, maxIters=maxIters)
            if log:
                err = 1.0*(opt - opt/rel)
                alsol[(opt, iopt)] = optimize(n, opt, iopt, w, eps=err, maxIters=maxIters)

    printTableSolutions(n, lopt, liopt, alsol, rel, log=log)

    metaId = getMetaId() + 1
    saveMetaSolutions(n, lopt, liopt, alsol, rel, metaId, log=log)

    return metaId
