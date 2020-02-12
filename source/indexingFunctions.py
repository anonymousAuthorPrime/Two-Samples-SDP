import numpy as np
import scipy.special as sps

import settings

# Fill partialSumsIndices
def fillPartialSumsIndices(n):
    bucketSizes = []
    for i in range(n):
        bucket = (n - i + 1)*(n - i)/2
        bucketSizes.append(bucket)

    settings.partialSumsIndices = np.zeros(n)
    for i in range(n):
        settings.partialSumsIndices[i] = np.sum(bucketSizes[:i])

    print("===== Partial Sums Indices Computed!")

# Return the index in the 1-d array that corresponds
# to the index (i, j, k) in the compressed 3-d tensor
def index(n, i, j, k):
    if (type(settings.partialSumsIndices) == type(None)):
        fillPartialSumsIndices(n)

    indLst = [i, j, k]
    indLst.sort()
    i = indLst[0]
    j = indLst[1]
    k = indLst[2]
    sBucket = ((n - i + 1)*(n - i)/2) - ((n - j + 1)*(n - j)/2)
    #print("sBucket :", sBucket)
    xindx = int(settings.partialSumsIndices[i]) + int(sBucket) + (k - j)
    return xindx

# Return the list that sums x[ii, jj, kk]
# with respect to ii from 0 to n
# with respect to jj from 0 to n
# with respect to kk from 0 to n
def allIndex(n):
    ind = []
    for ii in range(n):
        for jj in range(n):
            for kk in range(n):
                indd = index(n, ii, jj, kk)
                #print(ii, jj, kk, ":", indd)
                ind.append(indd)

    return ind

# Return the list that sums x[ii, jj, k]
# with respect to ii from 0 to i
# with respect to jj from 0 to j
def c12index3(n, i, j, k):
    ind = []
    for ii in range(i):
        for jj in range(j):
            ind.append(index(n, ii, jj, k))

    return ind

# Return a list of indecies whose sum is the
# marginal distribution with respect to the 1st coordinate
# at point i
def marginal_1(n, i):
    ind = []
    for j in range(n):
        for k in range(n):
            ind.append(index(n, i, j, k))

    return ind

# Return a list of indecies whose sum is the
# marginal distribution with respect to the 2nd coordinate
# at point j
def marginal_2(n, j):
    ind = []
    for i in range(n):
        for k in range(n):
            ind.append(index(n, i, j, k))

    return ind

# Return a list of indecies whose sum is the
# marginal distribution with respect to the 3rd coordinate
# at point k
def marginal_3(n, k):
    ind = []
    for i in range(n):
        for j in range(n):
            ind.append(index(n, i, j, k))

    return ind

# Return a list of indecies whose sum is the
# marginal distribution with respect to the tuple
# of (1st, 2nd) coordinate at point (i, j)
def marginal_1_2(n, i, j):
    ind = []
    for k in range(n):
        ind.append(index(n, i, j, k))

    return ind

# Return a list of indecies whose sum is the
# marginal distribution with respect to the tuple
# of (1st, 3rd) coordinate at point (i, k)
def marginal_1_3(n, i, k):
    ind = []
    for j in range(n):
        ind.append(index(n, i, j, k))

    return ind

# Return a list of indecies whose sum is the
# marginal distribution with respect to the tuple
# of (2nd, 3rd) coordinate at point (j, k)
def marginal_2_3(n, j, k):
    ind = []
    for i in range(n):
        ind.append(index(n, i, j, k))

    return ind
