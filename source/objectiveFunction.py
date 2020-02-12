import numpy as np
import cvxpy as cp
import scipy.special as sps

from indexingFunctions import *

def objectiveFunction(n, w, opt, verbose=False):
    b = np.zeros(int(sps.binom(n + 2, 3)))

    for i in range(1, n):
        for j in range(1, n):
            for k in range(1, n):
                pmax = max(w[i - 1], w[j - 1])
                pmin = min(w[i - 1], w[j - 1])
                if (pmin > 0) or (pmax >= 2*w[1]):
                    if (pmax >= 2*pmin):
                        if (w[k] > pmax):
                            b[index(n, i, j, k)] += (1.0/opt)*max(pmax, w[1])
                    if (pmax < 2*pmin):
                        if (w[k] > pmin):
                            b[index(n, i, j, k)] += (1.0/opt)*max(pmin, w[1])

    if verbose:
        print("objective function coefficients:")
        print(b)

    return b
