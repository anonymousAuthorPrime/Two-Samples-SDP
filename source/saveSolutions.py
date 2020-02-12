import datetime
import numpy as np
#import settings

from indexingFunctions import *

# variable params format:
# 0 -> opt
# 1 -> position of opt
# 2 -> array w

def emptyDictionary(filename=settings.pathToDictionary):
    dct = dict()

    with open(filename, 'w') as out:
        out.write(str(dct))

    return

def emptyLog(filename=settings.pathToLog):
    with open(filename, 'w') as out:
        out.write('')

    return

def restartID(filename=settings.pathToLastID):
    with open(filename, 'w') as out:
        out.write('1')

    return

def addToLog(n, x, y, z, value, params, id, filename=settings.pathToLog):
    with open(filename, 'a') as out:
        out.write('\n')
        out.write('\n')
        out.write('********************************************************\n')
        out.write(str(datetime.datetime.now()) + '\n')
        out.write('\n')
        out.write('id: ' + str(id) + '\n')
        out.write('\n')
        out.write('value: ' + str(value) + '\n')
        out.write('\n')
        out.write('discretization: ' + str(n) + ' hyperparameters: ' + str(params) + '\n')
        out.write('\n')
        out.write('########### value of x ##########\n')
        out.write(str(x) + '\n')
        out.write('=========== value of y ==========\n')
        out.write(str(y) + '\n')
        out.write('----------- value of z ----------\n')
        out.write(str(z) + '\n')
        out.write('\n')
        out.write('********************************************************\n')
        out.write('\n')
        out.write('\n')

def addToDictionary(n, x, y, z, value, params, filename=settings.pathToDictionary):
    dct = dict()
    with open(filename, 'r') as inp:
        dct = eval(inp.read())

    k = len(dct)
    dct[k + 1] = (datetime.datetime.now(), n, list(x), list(y), list(z), value, (params[0], params[1], list(params[2])))

    with open(filename, 'w') as out:
        out.write(str(dct))

    return k + 1

def addValueToMathematica(value, id, filepath=settings.pathToMathematica):
    filename = filepath + '/' + str(id) + '_value.dat'
    npval = np.array(value)
    npval.astype('float32').tofile(filename)

def addOptToMathematica(opt, id, filepath=settings.pathToMathematica):
    filename = filepath + '/' + str(id) + '_opt.dat'
    npopt = np.array(opt)
    npopt.astype('float32').tofile(filename)

def addIoptToMathematica(iopt, id, filepath=settings.pathToMathematica):
    filename = filepath + '/' + str(id) + '_iopt.dat'
    npiopt = np.array(iopt)
    npiopt.astype('float32').tofile(filename)

def addWToMathematica(w, id, filepath=settings.pathToMathematica):
    filename = filepath + '/' + str(id) + '_w.dat'
    nw = np.array(w)
    nw.astype('float32').tofile(filename)

def addXToMathematica(x, id, filepath=settings.pathToMathematica):
    filename = filepath + '/' + str(id) + '_x.dat'
    nx = np.array(x)
    nx.astype('float32').tofile(filename)

def addYToMathematica(y, id, filepath=settings.pathToMathematica):
    filename = filepath + '/' + str(id) + '_y.dat'
    ny = np.array(y)
    ny.astype('float32').tofile(filename)

def addZToMathematica(z, id, filepath=settings.pathToMathematica):
    filename = filepath + '/' + str(id) + '_z.dat'
    nz = np.array(z)
    nz.astype('float32').tofile(filename)

def addDToMathematica(d, id, filepath=settings.pathToMathematica):
    filename1 = filepath + '/' + str(id) + '_d1.dat'
    filename2 = filepath + '/' + str(id) + '_d2.dat'
    filename3 = filepath + '/' + str(id) + '_d3.dat'

    nd1 = np.array(d[0])
    nd2 = np.array(d[1])
    nd3 = np.array(d[2])

    nd1.astype('float32').tofile(filename1)
    nd2.astype('float32').tofile(filename2)
    nd3.astype('float32').tofile(filename3)

def addPToMathematica(p, id, filepath=settings.pathToMathematica):
    filename = filepath + '/' + str(id) + '_p.dat'
    npsd = np.array(p)
    npsd.astype('float32').tofile(filename)

def addRToMathematica(r, id, filepath=settings.pathToMathematica):
    filename = filepath + '/' + str(id) + '_r.dat'
    nr = np.array(r)
    nr.astype('float32').tofile(filename)

def addOToMathematica(o, id, filepath=settings.pathToMathematica):
    filename = filepath + '/' + str(id) + '_o.dat'
    no = np.array(o)
    no.astype('float32').tofile(filename)

def addBToMathematica(b, id, filepath=settings.pathToMathematica):
    filename = filepath + '/' + str(id) + '_b.dat'
    nb = np.array(b)
    nb.astype('float32').tofile(filename)

def addToMathematica(n, x, y, z, value, params, d, p, r, o, b, id, filepath=settings.pathToMathematica):
    opt = params[0]
    iopt = params[1]
    w = params[2]

    addValueToMathematica(opt, id, filepath=settings.pathToMathematica)
    addOptToMathematica(opt, id, filepath=settings.pathToMathematica)
    addIoptToMathematica(iopt, id, filepath=settings.pathToMathematica)
    addWToMathematica(w, id, filepath=settings.pathToMathematica)
    addXToMathematica(x, id, filepath=settings.pathToMathematica)
    addYToMathematica(y, id, filepath=settings.pathToMathematica)
    addZToMathematica(z, id, filepath=settings.pathToMathematica)
    addDToMathematica(d, id, filepath=settings.pathToMathematica)
    addPToMathematica(p, id, filepath=settings.pathToMathematica)
    addRToMathematica(r, id, filepath=settings.pathToMathematica)
    addOToMathematica(o, id, filepath=settings.pathToMathematica)
    addBToMathematica(b, id, filepath=settings.pathToMathematica)

def saveSolutionsFull(n, x, y, z, value, params, filenamel=settings.pathToLog, filenamed=settings.pathToDictionary, filenamem=settings.pathToMathematica):
    y = np.reshape(y, n**2)
    id = addToDictionary(n, x, y, z, value, params, filename=filenamed)
    addToLog(n, x, y, z, value, params, id, filename=filenamel)
    addToMathematica(n, x, y, z, value, params, id, filepath=filenamem)

    print("Solution with n =", n, ", opt =", params[0], ", iopt =", params[1], ", value =", value, " saved with id =", id, ".")

    return id

def increaseLastID():
    settings.lastID += 1
    with open(settings.pathToLastID, 'w') as out:
        out.write(str(settings.lastID))

    return settings.lastID

def readLastID():
    with open(settings.pathToLastID, 'r') as inp:
        return int(eval(inp.read()))

def saveSolutions(n, x, y, z, value, params, d, p, r, o, b, filenamel=settings.pathToLog, filenamed=settings.pathToDictionary, filenamem=settings.pathToMathematica, filenamei=settings.pathToLastID):
    y = np.reshape(y, n**2)
    id = increaseLastID()
    addToMathematica(n, x, y, z, value, params, d, p, r, o, b, id, filepath=filenamem)

    print("Solution with n =", n, ", opt =", params[0], ", iopt =", params[1], ", value =", value, " saved with id =", id, ".")

    return id
