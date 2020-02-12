import numpy as np
import cvxpy as cp

from indexingFunctions import *

def distributionConstraints(n, x):
    constr = []
    constr += [x >= 0]
    constr += [cp.sum(x[allIndex(n)]) == 1]
    constr += [cp.sum(x[marginal_1(n, 0)]) == 0]

    return constr

def distributionConstraintsDual(dconstr):
    d = []
    for i in range(len(dconstr)):
        d += [dconstr[i].dual_value]

    return d

def checkDistributionConstraints(n, x, y, z, acc, verbose=True):
    constr = True
    constr = constr and (y >= -acc).all()
    constr = constr and (np.abs(np.sum(x) - 1) <= acc)
    constr = constr and (np.abs(np.sum(y) - 1) <= acc)
    constr = constr and (np.abs(np.sum(z) - 1) <= acc)
    constr = constr and (np.abs(z[0]) <= acc)

    if verbose:
        print("sum x : ", np.sum(x))
        print("sum y : ", np.sum(y))
        print("sum z : ", np.sum(z))
        print("########## value of x ##########")
        print(x)
        print("========== value of y ==========")
        print(y)
        print("---------- value of z ----------")
        print(z)

    return constr
