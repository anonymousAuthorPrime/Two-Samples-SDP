import numpy as np
import cvxpy as cp

from indexingFunctions import *

def psdConstraints(n, x):
    constr = []
    for i in range(n):
        constr += [cp.reshape(x[marginal_1(n, i)], (n, n)) >> 0]

    return constr

def psdConstraintsDual(pconstr):
    p = []
    for i in range(len(pconstr)):
        p += [pconstr[i].dual_value]

    return p

def checkPsdConstraints(n, x, acc, verbose=False):
    constr = True
    for i in range(n):
        eigen = np.linalg.eigvals(np.reshape(x[marginal_1(n, i)], (n, n)))
        isPos = eigen >= - acc
        constr = constr and isPos.all()

        if verbose:
            print("marginal : ", i)
            print(eigen)

    return constr
