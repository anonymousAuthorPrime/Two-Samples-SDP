import numpy as np
import cvxpy as cp

from indexingFunctions import *

def xConstraints(n, x):
    constr = []
    for i in range(n**2):
        for j in range(n**2):
            if (j >= int(i / n + 1)*n):
                constr += [x[i, j] == 0]

    return constr

def yConstraints(n, x, y):
    constr = []
    # for i in range(n):
    #     for j in range(n):
    #         #print(marginal_1_2(n, i, j))
    #         constr += [y[i, j] == cp.sum(x[marginal_1_2(n, i, j)])]

    constr += [y == cp.reshape((cp.sum(x, axis=0)), (n, n))]
    return constr

def xValue(n, x):
    a = np.zeros((n, n, n))
    for i in range(n):
        for j in range(n):
            for k in range(n):
                a[i, j, k] = x[index(n, i, j, k)]

    a = np.reshape(a, n**3)
    return a

def yValue(n, x):
    y = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            y[i, j] = np.sum(x[marginal_1_2(n, i, j)])

    return y

def checkYConstraints(n, x, y, acc, verbose=False):
    constr = True
    for i in range(n):
        for j in range(n):
            constr = constr and (np.abs(y[i, j] - np.sum(x[marginal_1_2(n, i, j)])) <= acc)
            if verbose:
                print("y[", i, ", ", j, "] = ", y[i, j], "  marginal[", i, ", ", j, "] = ", np.sum(x[marginal_1_2(n, i, j)]))

    return constr

def zConstraints(n, x, z):
    constr = []
    for i in range(n):
        constr += [z[i] == cp.sum(x[marginal_1(n, i)])]

    return constr

def zValue(n, x):
    z = np.zeros(n)
    for i in range(n):
        z[i] = np.sum(x[marginal_1(n, i)])

    return z

def checkZConstraints(n, x, z, acc, verbose=False):
    constr = True
    for i in range(n):
        constr = constr and (np.abs(z[i] - np.sum(x[marginal_1(n, i)])) <= acc)
        if verbose:
            print("z[", i, "] = ", z[i], "  marginal[", i, "] = ", np.sum(x[marginal_1(n, i)]))

    return constr
