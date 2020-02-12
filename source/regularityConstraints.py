import numpy as np
import cvxpy as cp
import scipy.special as sps

from indexingFunctions import *

# TODO : checkExtentedRegularityConstraints

def regularityConstraints(n, y, z, w, iopt = 0):
    constr = []

    # regularity constraints with respect to matrix y
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(n):
                if (k < i) or (k > j):
                    constr += [w[j]*(cp.sum(z[:(k + 1)]) \
                                     - cp.sum(y[:(j + 1), :(k + 1)])) \
                             - w[i]*(cp.sum(z[:(k + 1)]) \
                                     - cp.sum(y[:(i + 1), :(k + 1)])) \
                             + w[i]*(cp.sum(z[:(j + 1)]) \
                                     - cp.sum(y[:(j + 1), :(i + 1)])) \
                             - w[j]*(cp.sum(z[:(i + 1)]) \
                                    - cp.sum(y[:(i + 1), :(j + 1)])) >= \
                               w[k]*(cp.sum(z[:(j + 1)]) \
                                     - cp.sum(y[:(k + 1), :(j + 1)])) \
                             - w[k]*(cp.sum(z[:(i + 1)]) \
                                     - cp.sum(y[:(k + 1), :(i + 1)]))]

                if (i < k) and (k < j):
                    constr += [w[j]*(cp.sum(z[:(k + 1)]) \
                                     - cp.sum(y[:(j + 1), :(k + 1)])) \
                             - w[i]*(cp.sum(z[:(k + 1)]) \
                                     - cp.sum(y[:(i + 1), :(k + 1)])) \
                             + w[i]*(cp.sum(z[:(j + 1)]) \
                                     - cp.sum(y[:(j + 1), :(i + 1)])) \
                             - w[j]*(cp.sum(z[:(i + 1)]) \
                                    - cp.sum(y[:(i + 1), :(j + 1)])) <= \
                               w[k]*(cp.sum(z[:(j + 1)]) \
                                     - cp.sum(y[:(k + 1), :(j + 1)])) \
                             - w[k]*(cp.sum(z[:(i + 1)]) \
                                     - cp.sum(y[:(k + 1), :(i + 1)]))]
    return constr

def extendedRegularityConstraintsMFast(n, x, w, iopt = 1):
    constr = []

    # regularity constraints with respect to each of the matrices x[:, :, l]
    for l in range(n):
        i = 0
        j = iopt
        for k in range(n):
            rb = np.zeros(int(sps.binom(n + 2, 3)))
            for ii in range(n):
                for jj in range(n):
                    rb[index(n, ii, jj, l)] += w[j] if (ii <= k) and (j < jj) else 0
                    rb[index(n, ii, jj, l)] += - w[i] if (ii <= k) and (i < jj) else 0
                    rb[index(n, ii, jj, l)] += w[i] if (ii <= j) and (i < jj) else 0
                    rb[index(n, ii, jj, l)] += - w[j] if (ii <= i) and (j < jj) else 0
                    rb[index(n, ii, jj, l)] += - w[k] if (ii <= j) and (k < jj) else 0
                    rb[index(n, ii, jj, l)] += w[k] if (ii <= i) and (k < jj) else 0
            if (k < i) or (k > j):
                constr += [rb*x >= 0]

            if (i < k) and (k < j):
                constr += [rb*x <= 0]

    return constr

def extendedRegularityConstraints(n, x, w, iopt = 1):
    constr = []

    # regularity constraints with respect to each of the matrices x[:, :, l]
    for l in range(n):
        for i in [0]:#, iopt - 1, int(iopt/2)]:
            for j in [iopt]:#range(i + 1, i + 2):#(i + 2, i + 3):#n):
                for k in range(n):#(i + 1, i + 2):
                    if (k < i) or (k > j):
                        constr += [w[j]*(cp.sum(x[c12index3(n, k + 1, n, l)]) \
                                   - cp.sum(x[c12index3(n, j + 1, k + 1, l)])) \
                                 - w[i]*(cp.sum(x[c12index3(n, k + 1, n, l)]) \
                                   - cp.sum(x[c12index3(n, i + 1, k + 1, l)])) \
                                 + w[i]*(cp.sum(x[c12index3(n, j + 1, n, l)]) \
                                   - cp.sum(x[c12index3(n, j + 1, i + 1, l)])) \
                                 - w[j]*(cp.sum(x[c12index3(n, i + 1, n, l)]) \
                                   - cp.sum(x[c12index3(n, i + 1, j + 1, l)])) \
                                   >= \
                                   w[k]*(cp.sum(x[c12index3(n, j + 1, n, l)]) \
                                   - cp.sum(x[c12index3(n, k + 1, j + 1, l)])) \
                                 - w[k]*(cp.sum(x[c12index3(n, i + 1, n, l)]) \
                                   - cp.sum(x[c12index3(n, k + 1, i + 1, l)]))]

                    if (i < k) and (k < j):
                        constr += [w[j]*(cp.sum(x[c12index3(n, k + 1, n, l)]) \
                                   - cp.sum(x[c12index3(n, j + 1, k + 1, l)])) \
                                 - w[i]*(cp.sum(x[c12index3(n, k + 1, n, l)]) \
                                   - cp.sum(x[c12index3(n, i + 1, k + 1, l)])) \
                                 + w[i]*(cp.sum(x[c12index3(n, j + 1, n, l)]) \
                                   - cp.sum(x[c12index3(n, j + 1, i + 1, l)])) \
                                 - w[j]*(cp.sum(x[c12index3(n, i + 1, n, l)]) \
                                   - cp.sum(x[c12index3(n, i + 1, j + 1, l)])) \
                                   <= \
                                   w[k]*(cp.sum(x[c12index3(n, j + 1, n, l)]) \
                                   - cp.sum(x[c12index3(n, k + 1, j + 1, l)])) \
                                 - w[k]*(cp.sum(x[c12index3(n, i + 1, n, l)]) \
                                   - cp.sum(x[c12index3(n, k + 1, i + 1, l)]))]

    return constr

def regularityConstraintsDual(rconstr):
    r = []
    for i in range(len(rconstr)):
        r += [rconstr[i].dual_value]

    return r

def checkRegularityConstraints(n, y, z, w, acc, verbose=False):
    constr = True
    # middle regularity constraints
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(n):
                if (k < i) or (k > j):
                    constr = constr and (w[j]*(np.sum(z[:(k + 1)]) \
                                     - np.sum(y[:(j + 1), :(k + 1)])) \
                             - w[i]*(np.sum(z[:(k + 1)]) \
                                     - np.sum(y[:(i + 1), :(k + 1)])) \
                             + w[i]*(np.sum(z[:(j + 1)]) \
                                     - np.sum(y[:(j + 1), :(i + 1)])) \
                             - w[j]*(np.sum(z[:(i + 1)]) \
                                     - np.sum(y[:(i + 1), :(j + 1)])) >= \
                               w[k]*(np.sum(z[:(j + 1)]) \
                                     - np.sum(y[:(k + 1), :(j + 1)])) \
                             - w[k]*(np.sum(z[:(i + 1)]) \
                                     - np.sum(y[:(k + 1), :(i + 1)])) - acc)
                    if verbose:
                        print("first", i, j, k, (w[j]*(np.sum(z[:(k + 1)]) \
                                         - np.sum(y[:(j + 1), :(k + 1)])) \
                                 - w[i]*(np.sum(z[:(k + 1)]) \
                                         - np.sum(y[:(i + 1), :(k + 1)])) \
                                 + w[i]*(np.sum(z[:(j + 1)]) \
                                         - np.sum(y[:(j + 1), :(i + 1)])) \
                                 - w[j]*(np.sum(z[:(i + 1)]) \
                                         - np.sum(y[:(i + 1), :(j + 1)])) >= \
                                   w[k]*(np.sum(z[:(j + 1)]) \
                                         - np.sum(y[:(k + 1), :(j + 1)])) \
                                 - w[k]*(np.sum(z[:(i + 1)]) \
                                         - np.sum(y[:(k + 1), :(i + 1)])) - acc))
                        print(" + w[", j, "] = ", w[j], ", sum(z[:", k + 1, "]) = ", np.sum(z[:(k + 1)]), ", sum(y[:", j + 1, ", :", k + 1, "]) = ", np.sum(y[:(j + 1), :(k + 1)]))
                        print(" - w[", i, "] = ", w[i], ", sum(z[:", k + 1, "]) = ", np.sum(z[:(k + 1)]), ", sum(y[:", i + 1, ", :", k + 1, "]) = ", np.sum(y[:(i + 1), :(k + 1)]))
                        print(" + w[", i, "] = ", w[i], ", sum(z[:", j + 1, "]) = ", np.sum(z[:(j + 1)]), ", sum(y[:", j + 1, ", :", i + 1, "]) = ", np.sum(y[:(j + 1), :(i + 1)]))
                        print(" - w[", j, "] = ", w[j], ", sum(z[:", i + 1, "]) = ", np.sum(z[:(i + 1)]), ", sum(y[:", i + 1, ", :", j + 1, "]) = ", np.sum(y[:(i + 1), :(j + 1)]))
                        print(">=")
                        print(" + w[", k, "] = ", w[k], ", sum(z[:", j + 1, "]) = ", np.sum(z[:(j + 1)]), ", sum(y[:", k + 1, ", :", j + 1, "]) = ", np.sum(y[:(k + 1), :(j + 1)]))
                        print(" - w[", k, "] = ", w[k], ", sum(z[:", i + 1, "]) = ", np.sum(z[:(i + 1)]), ", sum(y[:", k + 1, ", :", i + 1, "]) = ", np.sum(y[:(k + 1), :(i + 1)]))
                        print()

                if (i < k) and (k < j):
                    constr = constr and (w[j]*(np.sum(z[:(k + 1)]) \
                                     - np.sum(y[:(j + 1), :(k + 1)])) \
                             - w[i]*(np.sum(z[:(k + 1)]) \
                                     - np.sum(y[:(i + 1), :(k + 1)])) \
                             + w[i]*(np.sum(z[:(j + 1)]) \
                                     - np.sum(y[:(j + 1), :(i + 1)])) \
                             - w[j]*(np.sum(z[:(i + 1)]) \
                                     - np.sum(y[:(i + 1), :(j + 1)])) <= \
                               w[k]*(np.sum(z[:(j + 1)]) \
                                     - np.sum(y[:(k + 1), :(j + 1)])) \
                             - w[k]*(np.sum(z[:(i + 1)]) \
                                     - np.sum(y[:(k + 1), :(i + 1)])) + acc)

                    if verbose:
                        print("second", i, j, k, (w[j]*(np.sum(z[:(k + 1)]) \
                                         - np.sum(y[:(j + 1), :(k + 1)])) \
                                 - w[i]*(np.sum(z[:(k + 1)]) \
                                         - np.sum(y[:(i + 1), :(k + 1)])) \
                                 + w[i]*(np.sum(z[:(j + 1)]) \
                                         - np.sum(y[:(j + 1), :(i + 1)])) \
                                 - w[j]*(np.sum(z[:(i + 1)]) \
                                         - np.sum(y[:(i + 1), :(j + 1)])) <= \
                                   w[k]*(np.sum(z[:(j + 1)]) \
                                         - np.sum(y[:(k + 1), :(j + 1)])) \
                                 - w[k]*(np.sum(z[:(i + 1)]) \
                                         - np.sum(y[:(k + 1), :(i + 1)])) + acc))

                        print(" + w[", j, "] = ", w[j], ", sum(z[:", k + 1, "]) = ", np.sum(z[:(k + 1)]), ", sum(y[:", j + 1, ", :", k + 1, "]) = ", np.sum(y[:(j + 1), :(k + 1)]))
                        print(" - w[", i, "] = ", w[i], ", sum(z[:", k + 1, "]) = ", np.sum(z[:(k + 1)]), ", sum(y[:", i + 1, ", :", k + 1, "]) = ", np.sum(y[:(i + 1), :(k + 1)]))
                        print(" + w[", i, "] = ", w[i], ", sum(z[:", j + 1, "]) = ", np.sum(z[:(j + 1)]), ", sum(y[:", j + 1, ", :", i + 1, "]) = ", np.sum(y[:(j + 1), :(i + 1)]))
                        print(" - w[", j, "] = ", w[j], ", sum(z[:", i + 1, "]) = ", np.sum(z[:(i + 1)]), ", sum(y[:", i + 1, ", :", j + 1, "]) = ", np.sum(y[:(i + 1), :(j + 1)]))
                        print("<=")
                        print(" + w[", k, "] = ", w[k], ", sum(z[:", j + 1, "]) = ", np.sum(z[:(j + 1)]), ", sum(y[:", k + 1, ", :", j + 1, "]) = ", np.sum(y[:(k + 1), :(j + 1)]))
                        print(" - w[", k, "] = ", w[k], ", sum(z[:", i + 1, "]) = ", np.sum(z[:(i + 1)]), ", sum(y[:", k + 1, ", :", i + 1, "]) = ", np.sum(y[:(k + 1), :(i + 1)]))
                        print()

    return constr
