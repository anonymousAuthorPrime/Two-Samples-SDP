import numpy as np
import cvxpy as cp

from indexingFunctions import *

# TODO : checkExtentedOptimalityConstraints

def optimalityConstraints(n, z, opt, iopt, w, eps):
    constr = []
    for i in range(n):
        constr += [w[i]*(1 - cp.sum(z[:(i + 1)])) <= opt]

    constr += [w[iopt]*(1 - cp.sum(z[:(iopt + 1)])) >= opt - eps]

    return constr

def extendedOptimalityConstraints(n, x, opt, iopt, w, eps):
    constr = []
    for l in range(n):
        for i in range(n):
            constr += [w[i]*(cp.sum(x[marginal_1(n, l)]) - cp.sum(x[c12index3(n, i + 1, n, l)])) <= opt*(cp.sum(x[marginal_1(n, l)]))]

        constr += [w[iopt]*(cp.sum(x[marginal_1(n, l)]) - cp.sum(x[c12index3(n, iopt + 1, n, l)])) >= \
                        (opt - eps)*(cp.sum(x[marginal_1(n, l)]))]

    return constr

def optimalityConstraintsDual(oconstr):
    o = []
    for i in range(len(oconstr)):
        o += [oconstr[i].dual_value]

    return o

def checkOptimalityConstraints(n, z, opt, iopt, w, eps, acc, verbose=False):
    constr = True
    for i in range(n):
        constr = constr and (w[i]*(1 - np.sum(z[:(i + 1)])) <= opt + acc)

        if verbose:
            print("revenue at ", i, " with price ", w[i], " : ", w[i]*(1 - np.sum(z[:(i + 1)])))

    constr = constr and (w[iopt]*(1 - np.sum(z[:(iopt + 1)])) >= opt - eps - acc)

    if verbose:
        print("revenue at optimal point ", iopt, " with price ", w[iopt], " : ", w[iopt]*(1 - np.sum(z[:(iopt + 1)])))

    return constr
