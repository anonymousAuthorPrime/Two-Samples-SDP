import sys
import os
import argparse

import numpy as np
import cvxpy as cp

import settings

from xyzImplementation import *
from explore import *
from recursiveExplore import *

from saveSolutions import *
from saveMetaSolutions import *
from readMetaSolutions import *


# TODO : output id
# TODO : change path
# TODO : evaluate based on id

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Reserves Factor Releaving SDP')

    # Arguments for maintance
    parser.add_argument('-c', action='store_const', const=True, default=False, help='clean logs')
    parser.add_argument('-cm', action='store_const', const=True, default=False, help='clean meta-logs')
    parser.add_argument('-p', type=str, default='', help='change log path')

    # Arguments on what to run
    parser.add_argument('-e', action='store_const', const=True, default=False, help='run evaluation')
    parser.add_argument('-o', action='store_const', const=True, default=False, help='run optimization')
    parser.add_argument('-x', action='store_const', const=True, default=False, help='run exploration')
    parser.add_argument('-xr', action='store_const', const=True, default=False, help='run recursive exploration')
    parser.add_argument('-big', action='store_const', const=True, default=False, help='use big logs')

    # Arguments with parameters
    parser.add_argument('-n', type=int, default=-1, help='price discretization number')
    parser.add_argument('-m', type=int, default=-1, help='optimum discretization number')
    parser.add_argument('-opt', type=float, default=-1, help='optimum value')
    parser.add_argument('-iopt', type=int, default=-1, help='position of optimum')
    parser.add_argument('-eps', type=float, default=-1, help='relaxation of optimality constraint')
    parser.add_argument('-id', type=int, default=-1, help='solution to evaluate')
    parser.add_argument('-log', action='store_const', const=True, default=False, help='discretize logarithmically')
    parser.add_argument('-lo', type=float, default=-1, help='lower value of optimum')
    parser.add_argument('-rel', type=float, default=-1, help='multiplicative increase factor')

    parser.add_argument('-g', type=float, default=-1, help='goal of recursive exploration')
    parser.add_argument('-sp', type=float, default=-1, help='stop precision of recursive exploration >= 1')
    parser.add_argument('-mm', type=int, default=-1, help='the parameter m_-')

    # Verbose Arguments
    parser.add_argument('-yV', action='store_const', const=True, default=False, help='y constraints verbose')
    parser.add_argument('-zV', action='store_const', const=True, default=False, help='z constraints verbose')
    parser.add_argument('-dV', action='store_const', const=True, default=False, help='distribution constraints verbose')
    parser.add_argument('-sV', action='store_const', const=True, default=False, help='symmetry constraints verbose')
    parser.add_argument('-pV', action='store_const', const=True, default=False, help='PSD constraints verbose')
    parser.add_argument('-rV', action='store_const', const=True, default=False, help='regularity constraints verbose')
    parser.add_argument('-oV', action='store_const', const=True, default=False, help='optimality constraints verbose')
    parser.add_argument('-dualV', action='store_const', const=True, default=False, help='dual variables verbose')

    # Printing Arguments
    parser.add_argument('-prm', type=int, default=-1, help='print table with given meta-id')

    # Parameters of Optimization
    parser.add_argument('-mi', type=int, default=-1, help='maximum number of iterations')
    parser.add_argument('-solver', type=str, default="", help='select solver')

    args = parser.parse_args()

    # Initialize Global Variables
    settings.init(args.big)

    # Parameters
    n = args.n if args.n > 0 else 4
    m = args.m if args.m > 0 else n
    mm = args.mm if args.mm > 0 else int((n - 2)/2)
    mp = (n - 2) - mm
    opt = args.opt if args.opt > 0 else \
            ((1.0/args.rel)**mp if args.rel > 0 else 0.5)
    iopt = args.iopt if args.iopt > 0 else 2
    goal = args.g if args.g > 0 else 0.6
    stopPrec = args.sp if args.sp > 0 else 3.0/n

    # Program to run
    evalt = args.e
    optm = args.o
    expl = args.x
    rexpl = args.xr
    clean = args.c
    big = args.big

    printMeta = args.prm
    cleanMeta = args.cm
    id = args.id
    logB = args.log
    lowOpt = args.lo if args.lo > 0 else opt
    rel = args.rel if args.rel > 0 else 2

    path = args.p
    yVerbose = args.yV
    zVerbose = args.zV
    dVerbose = args.dV
    sVerbose = args.sV
    pVerbose = args.pV
    rVerbose = args.rV
    oVerbose = args.oV
    dualVerbose = args.dualV

    # Solver Parameters
    solver = args.solver if (args.solver != "") else "SCS"
    maxIters = args.mi

    if clean:
        emptyLog()
        emptyDictionary()
        restartID()
        sys.exit()

    if cleanMeta:
        emptyMetaLog()
        emptyMetaDictionary()
        sys.exit()

    if evalt:
        if id < 0:
            evaluate(n, yVerbose=yVerbose, zVerbose=zVerbose, dVerbose=dVerbose, sVerbose=sVerbose, pVerbose=pVerbose, rVerbose=rVerbose, oVerbose=oVerbose)
        else:
            evaluate(-1, id=id, yVerbose=yVerbose, zVerbose=zVerbose, dVerbose=dVerbose, sVerbose=sVerbose, pVerbose=pVerbose, rVerbose=rVerbose, oVerbose=oVerbose)
        sys.exit()

    if printMeta > 0:
        printFromMetaDictionary(printMeta)
        sys.exit()

    if optm:
        if (not logB):
            eps = args.eps if args.eps > 0 else 1.0/(n - 1)
            w = np.zeros(n)
            for i in range(n):
                w[i] = (1.0/(n - 1))*i

            print("Optimization in arithmetic scale with n =", n, "low optimum value =", lowOpt, "eps =", eps)
            print("w =", w)
            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n")
        if logB:
            eps = args.eps if args.eps > 0 else (opt - opt/rel)
            w = [0]
            tempW = []
            tempIopt = lowOpt*1.0/rel
            for i in range(mm):
                tempW += [tempIopt]
                tempIopt = tempIopt/rel

            tempW.reverse()
            w += tempW

            tempIopt = lowOpt
            while (tempIopt < 1.0):
                w += [tempIopt]
                tempIopt = tempIopt*rel
            w += [1.0]

            print("Optimization in geometric scale with n =", n, "low optimum value =", lowOpt, "eps =", eps)
            print("w =", w)
            print("********************************************************************************\n\n")

        optimize(n, opt, iopt, w, eps=eps, yVerbose=yVerbose, zVerbose=zVerbose, dVerbose=dVerbose, sVerbose=sVerbose, pVerbose=pVerbose, rVerbose=rVerbose, oVerbose=oVerbose, dualVerbose=dualVerbose, maxIters=maxIters, solver=solver)
        sys.exit()

    if expl:
        if (not logB):
            eps = args.eps if args.eps > 0 else 1.0/(n - 1)

            w = np.zeros(n)
            for i in range(n):
                w[i] = (1.0/(n - 1))*i

            print("Exploration in arithmetic scale with n =", n, "eps =", eps)
            print("w =", w)
            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n")

            explore(n, w, err=1.0/m)
            sys.exit()
        if logB:
            eps = args.eps if args.eps > 0 else (opt - opt/rel)
            w = [0]
            tempW = []
            tempIopt = lowOpt*1.0/rel
            for i in range(mm):
                tempW += [tempIopt]
                tempIopt = tempIopt/rel

            tempW.reverse()
            w += tempW

            tempIopt = lowOpt
            while (tempIopt < 1.0):
                w += [tempIopt]
                tempIopt = tempIopt*rel
            w += [1.0]

            print("Exploration in geometric scale with n =", n, "low optimum value =", lowOpt, "eps =", eps)
            print("w =", w)
            print("********************************************************************************\n\n")

            if (opt == 0.5):
                explore(n, w, rel=rel, log=True, lowOpt=lowOpt)
            else:
                explore(n, w, opt=opt, rel=rel, log=True, lowOpt=lowOpt, lowIopt=mm, maxIters=maxIters)
            sys.exit()
    if rexpl:
        eps = args.eps if args.eps > 0 else 0.5
        w = np.zeros(n)
        for i in range(n):
            w[i] = (1.0/(n - 1))*i

        recursiveExplore(n, w, err=eps, goal=goal, stopPrec=stopPrec)
        sys.exit()

    parser.print_help()
