import numpy as np
import cvxpy as cp
import scipy.special as sps

from indexingFunctions import *

from yzConstraints import *
from distributionConstraints import *
from symmetryConstraints import *
from psdConstraints import *
from regularityConstraints import *
from optimalityConstraints import *

from objectiveFunction import *

from saveSolutions import *
from readSolutions import *

import time

def optimize(n, opt, iopt, w, acc=0.005, eps=-1, solver="SCS", solverVerbose=True, maxIters=-1, yVerbose=False, zVerbose=False, dVerbose=False, sVerbose=False, pVerbose=False, rVerbose=False, oVerbose=False, jVerbose=False, dualVerbose=False):
    point = time.process_time()
    if (eps < 0):
        eps = 1.0/(n - 1)

    print("Size of Tensor with n =", n, ":", int(sps.binom(n + 2, 3)), "\n\n")
    x = cp.Variable(int(sps.binom(n + 2, 3)))

    npoint = time.process_time()
    print("Defined Variables : ", npoint - point)
    point = npoint

    #constraints on variable x
    xconstr = [] #xConstraints(n, x)

    # constraints on variable y
    yconstr = []#yConstraints(n, x, y)

    # constraints on variable z
    zconstr = []#zConstraints(n, x, z)

    npoint = time.process_time()
    print("Variable Constraints : ", npoint - point)
    point = npoint

    # constraints to force distribution
    dconstr = distributionConstraints(n, x)

    npoint = time.process_time()
    print("Distribution Constraints : ", npoint - point)
    point = npoint

    # constraints to force symmetry
    sconstr = [] #symmetryConstraints(n, x)

    npoint = time.process_time()
    print("Symmetry Constraints : ", npoint - point)
    point = npoint

    # constraints to for positive semidefinite product matrices
    pconstr = psdConstraints(n, x)

    npoint = time.process_time()
    print("PSD Constraints : ", npoint - point)
    point = npoint

    # constraints for regularity
    #rconstr = regularityConstraints(n, y, z, w)
    rconstr = extendedRegularityConstraintsMFast(n, x, w, iopt = iopt)

    npoint = time.process_time()
    print("Regularity Constraints : ", npoint - point)
    point = npoint

    # constraints for optimality
    #oconstr = optimalityConstraints(n, z, opt, iopt, w, eps)
    oconstr = extendedOptimalityConstraints(n, x, opt, iopt, w, eps)

    npoint = time.process_time()
    print("Optimality Constraints : ", npoint - point)
    point = npoint

    # all the constraints
    constraints = xconstr + yconstr + zconstr + dconstr \
                  + sconstr + pconstr + rconstr + oconstr

    # objective function coefficients
    bobj = objectiveFunction(n, w, opt, verbose=jVerbose)
    objective = cp.Minimize(bobj*x)

    npoint = time.process_time()
    print("Objective Definition : ", npoint - point)
    point = npoint

    problem = cp.Problem(objective, constraints)

    # Time to solve the problem
    if (solver == "SCS"):
        max_iters = 2500 if maxIters < 0 else maxIters

        problem.solve(solver=solver, verbose=solverVerbose, eps=1e-2, max_iters=max_iters)

    elif (solver == "CVXOPT"):
        max_iters = 100 if maxIters < 0 else maxIters

        problem.solve(solver=solver, verbose=solverVerbose, abstol=acc*1e-01, max_iters=maxIters)

    else:
        problem.solve(verbose=solverVerbose)

    id = -1

    if (type(x.value) != type(None)):
        a = xValue(n, x.value)
        b = yValue(n, x.value)
        c = zValue(n, x.value)

        print("(opt, iopt) = (",opt, ", ", iopt, ")", "value : ", problem.value, "dual value : ", - dconstr[1].dual_value)
        print("check y: ", checkYConstraints(n, x.value, b, acc, verbose=yVerbose))
        print("check z: ", checkZConstraints(n, x.value, c, acc, verbose=zVerbose))
        print("check d: ", checkDistributionConstraints(n, a, b, c, acc, verbose=dVerbose))
        print("check s: ", checkSymmetryConstraints(n, x.value, b, c, acc, verbose=sVerbose))
        print("check p: ", checkPsdConstraints(n, x.value, acc, verbose=pVerbose))
        print("check r: ", checkRegularityConstraints(n, b, c, w, acc, verbose=rVerbose))
        print("check o: ", checkOptimalityConstraints(n, c, opt, iopt, w, eps, acc, verbose=oVerbose))

        d = distributionConstraintsDual(dconstr)
        p = psdConstraintsDual(pconstr)
        r = regularityConstraintsDual(rconstr)
        o = optimalityConstraintsDual(oconstr)

        if dualVerbose:
            print("Distribution Dual")
            print(list(d), "\n")

            print("PSD Dual")
            print(p, "\n")

            print("Regularity Dual")
            print(list(r), "\n")

            print("Optimality Dual")
            print(list(o), "\n")

        #printDualSymmetryVariables(sconstr)
        id = saveSolutions(n, a, b, c, problem.value, (opt, iopt, w), d, p, r, o, b)
    else:
        if (str(problem.value) == 'inf'):
            return (0, id)
        else:
            return (5, id)

    return (problem.value, id)

def evaluate(n, id=None, x=None, y=None, z=None, w=None, acc=1e-04, eps=None, yVerbose=False, zVerbose=False, dVerbose=False, sVerbose=False, pVerbose=False, rVerbose=False, oVerbose=False):
    optStar = 0
    ioptStar = 0

    if (id != None):
        data = readFromDictionary(id)
        n = data[1]
        x = np.array(data[2])
        y = np.array(data[3])
        z = np.array(data[4])
        value = data[5]
        params = data[6]
        optStar = params[0]
        ioptStar = params[1]
        w = np.array(params[2])
        print("Example with n =", n)
        print("--------------------------------------\n")

    if (type(x) == type(None)) or (type(y) == type(None)) \
      or (type(z) == type(None)):
        w = np.zeros(n)
        for i in range(n):
            w[i] = (1.0/(n - 1))*i

        x = np.zeros(n**3)
        y = np.zeros((n , n))
        z = np.zeros(n)

        for i in range(1, n):
            z[i] = 1.0/(n - 1)

        for i in range(1, n):
            for j in range(1, n):
                for k in range(1, n):
                    x[index(n, i, j, k)] = z[i]*z[j]*z[k]

                y[i, j] = z[i]*z[j]
    else:
        y = np.reshape(y, (n, n))

    r = np.zeros(n)
    opt = 0
    iopt = 0
    for i in range(n):
        r[i] = w[i]*(1 - np.sum(z[:(i + 1)]))
        if (opt < r[i]):
            opt = r[i]
            iopt = i

    if (id != None):
        print("Check the values of opt, iopt")
        print("opt  = {:4.2f} |".format(opt), "opt* =", optStar)
        print("iopt = {:4d} |".format(iopt), "iopt* =", ioptStar)
        print()

    b = np.zeros(n**3)
    for i in range(1, n):
        for j in range(1, n):
            for k in range(1, n):
                pmax = max(w[i - 1], w[j - 1])
                pmin = min(w[i - 1], w[j - 1])
                if (pmax >= 2*pmin):
                    if (w[k] > max(pmax, w[1])):
                        b[index(n, i, j, k)] = (1.0/opt)*max(pmax, w[1])* \
                          x[index(n, i, j, k)]
                if (pmax < 2*pmin):
                    if (w[k] > max(pmin, w[1])):
                        b[index(n, i, j, k)] = (1.0/opt)*max(pmin, w[1])* \
                          x[index(n, i, j, k)]

    value = np.sum(b)
    if (type(eps) == type(None)):
        eps = 1.0/(n - 1)

    print("value : ", value)
    print("check y: ", checkYConstraints(n, x, y, acc, verbose=yVerbose))
    print("check z: ", checkZConstraints(n, x, z, acc, verbose=zVerbose))
    print("check d: ", checkDistributionConstraints(n, x, y, z, acc, verbose=dVerbose))
    print("check s: ", checkSymmetryConstraints(n, x, y, z, acc, verbose=sVerbose))
    print("check p: ", checkPsdConstraints(n, x, acc, verbose=pVerbose))
    print("check r: ", checkRegularityConstraints(n, y, z, w, acc, verbose=rVerbose))
    print("check o: ", checkOptimalityConstraints(n, z, opt, iopt, w, eps, acc, verbose=oVerbose))
    print("\n--------------------------------------\n")

    if (id == None):
        saveSolutions(n, x, y, z, value, (opt, iopt, w))
