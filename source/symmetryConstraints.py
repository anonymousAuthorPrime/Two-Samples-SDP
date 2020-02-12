import numpy as np
import cvxpy as cp

from indexingFunctions import *

def symmetryConstraints(n, x):
    constr = []
    #bSymConstr = np.zeros((n**2, n**2))
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if (i > j):
                    constr += [x[index(n, i, j, k)] == x[index(n, j, i, k)]]
                if (j > k):
                    #bSymConstr[index(n, i, j, k)] = 1
                    #bSymConstr[index(n, i, k, j)] = -1
                    constr += [x[index(n, i, j, k)] == x[index(n, i, k, j)]]
                #constr += [x[index(n, i, j, k)] == x[index(n, j, k, i)]]
                #constr += [x[index(n, i, j, k)] == x[index(n, k, i, j)]]
                #constr += [x[index(n, i, j, k)] == x[index(n, k, j, i)]]

    #constr += [bSymConstr*x == 0]
    # for i in range(n):
    #     for j in range(n):
    #         constr += [y[i, j] == cp.sum(x[marginal_1_3(n, i, j)])]
    #         constr += [y[i, j] == cp.sum(x[marginal_2_3(n, i, j)])]
    #
    # for i in range(n):
    #     constr += [z[i] == cp.sum(x[marginal_2(n, i)])]
    #     constr += [z[i] == cp.sum(x[marginal_3(n, i)])]

    return constr

def checkSymmetryConstraints(n, x, y, z, acc, verbose=False):
    constr = True
    for i in range(n):
        for j in range(n):
            for k in range(n):
                constr = constr and (np.abs(x[index(n, i, j, k)] - x[index(n, j, i, k)]) <= acc)
                constr = constr and (np.abs(x[index(n, i, j, k)] - x[index(n, i, k, j)]) <= acc)
                constr = constr and (np.abs(x[index(n, i, j, k)] - x[index(n, j, k, i)]) <= acc)
                constr = constr and (np.abs(x[index(n, i, j, k)] - x[index(n, k, i, j)]) <= acc)
                constr = constr and (np.abs(x[index(n, i, j, k)] - x[index(n, k, j, i)]) <= acc)

                if verbose:
                    print("x[", i, ", ", j, ", ", k, "] = ", x[index(n, i, j, k)], ", x[", j, ", ", i, ", ", k, "] = ", x[index(n, j, i, k)])
                    print("x[", i, ", ", j, ", ", k, "] = ", x[index(n, i, j, k)], ", x[", i, ", ", k, ", ", j, "] = ", x[index(n, j, i, k)])
                    print("x[", i, ", ", j, ", ", k, "] = ", x[index(n, i, j, k)], ", x[", j, ", ", k, ", ", i, "] = ", x[index(n, j, k, i)])
                    print("x[", i, ", ", j, ", ", k, "] = ", x[index(n, i, j, k)], ", x[", k, ", ", i, ", ", j, "] = ", x[index(n, k, i, j)])
                    print("x[", i, ", ", j, ", ", k, "] = ", x[index(n, i, j, k)], ", x[", k, ", ", j, ", ", i, "] = ", x[index(n, k, j, i)])

    for i in range(n):
        for j in range(n):
            constr = constr and (np.abs(y[i, j] - np.sum(x[marginal_1_3(n, i, j)])) <= acc)
            constr = constr and (np.abs(y[i, j] - np.sum(x[marginal_2_3(n, i, j)])) <= acc)

            if verbose:
                print("y[", i, ", ", j, "] = ", y[i, j], ", x_marginal_1_3[", i, ", ", j, "] = ", np.sum(x[marginal_1_3(n, i, j)]))
                print("y[", i, ", ", j, "] = ", y[i, j], ", x_marginal_w_3[", i, ", ", j, "] = ", np.sum(x[marginal_w_3(n, i, j)]))

    for i in range(n):
        constr = constr and (np.abs(z[i] - np.sum(x[marginal_2(n, i)])) <= acc)
        constr = constr and (np.abs(z[i] - np.sum(x[marginal_3(n, i)])) <= acc)

        if verbose:
            print("z[", i, "] = ", z[i], ", x_marginal_2[", i, "] = ", np.sum(x[marginal_2(n, i, j)]))
            print("z[", i, "] = ", z[i], ", x_marginal_3[", i, "] = ", np.sum(x[marginal_3(n, i, j)]))

    return constr

def printDualSymmetryVariables(sconstr):
    print("Printing Symmetry Dual Variables")
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

    for i in range(len(sconstr)):
        print("i : ", i, " = ", sconstr[i].dual_value)
