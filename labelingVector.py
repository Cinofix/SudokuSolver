from random import randint

import numpy as np

from state import State

ncells = 9
totcells = 81
p = np.ones((totcells*ncells, 1))/ncells
rij = np.zeros((totcells*ncells,totcells*ncells))

def createRij():
    global ncells, totcells, rij

    for i in range(totcells):
        for lb in range(ncells):
            for j in range(totcells):
                for mu in range(ncells):
                    rij[i*ncells + lb][j*ncells + mu] = compatibility(i,j,lb,mu)
    np.savetxt('rij.csv', rij, delimiter=',')

def initVector(board):
    global p, totcells
    initBoardVector(board)

def initBoardVector(board):
    global ncells, p, totcells

    board = State(board)
    ncells = board.blockSize

    for i in range(ncells):
        for j in range(ncells):
            domainSet = board.getDomainSet(i,j)
            n = len(domainSet)
            prob = np.zeros((1, ncells))[0]
            if not board.isEmpty(i,j):# value just assigned
                val = int(board.getValue(i,j))
                prob[val-1] = 1
            else:
                for k in domainSet:
                    prob[int(k) - 1] = 1/n + randint(0,20)/100.0
            prob = prob/np.sum(prob)
            p.reshape(ncells,ncells,ncells)[i][j] = prob

def compatibility(i, j, lb, mu):
    if i == j:
        return 0
    if lb != mu:
        return 1
    if inSameRow(i,j) or inSameColumn(i,j) or inSameBlock(i,j):
        return 0
    return 1


def inSameColumn(i, j):
    global ncells
    return i%ncells == j%ncells

def inSameRow(i,j):
    global ncells
    return i//ncells == j//ncells

def inSameBlock(i, j):
    global ncells

    i_x = i // ncells
    i_y = i % ncells
    j_x = j // ncells
    j_y = j % ncells
    start_i_x = i_x - i_x%3
    start_i_y = i_y - i_y%3
    start_j_x = j_x - j_x%3
    start_j_y = j_y - j_y%3
    return start_i_x == start_j_x and start_i_y == start_j_y


def averageConsistency(q):
    global ncells, p
    return np.sum(p*q)

def relaxationLabeling():
    global rij, p
    diff = 1
    avg_b = 0
    t = 0
    while diff > 0.001:
        q = np.dot(rij, p)
        num = p * q
        row_sums = num.reshape(ncells*ncells,ncells).sum(axis=1)
        p = (num.reshape(ncells*ncells,ncells)/row_sums[:, np.newaxis]).reshape(729,1)
        avg = averageConsistency(q)
        diff = avg - avg_b
        avg_b = avg
        t += 1
    p = p.reshape(totcells, ncells)

def solve_relaxationLabeling(board, create = False):
    global ncells,totcells, p, rij
    if create: createRij() # create matrix Rij when it is necessary
    initVector(board)

    rij = np.loadtxt("rij.csv", delimiter=",") # createRij()
    relaxationLabeling()
    for i in range(totcells):
        pos = np.argmax(p[i])
        if i % ncells == 0:
            print("")
        print(pos+1, end=" ")


def printBoard():
    global ncells, p

    for i in range(totcells*ncells):
        if i % ncells == 0:
            print("\n")
        print(str(p[i]), end="\n")
    print("\n\n")

def printCandidates():
    global totcells, ncells
    for i in range(totcells):
        pos = np.argmax(p[i])
        if i % ncells == 0:
            print("")
        print(str(pos+1)+" ", end ="")

