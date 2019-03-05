from random import randint

import numpy as np

from state import State

ncells = 9
totcells = 81
p = np.ones((totcells, ncells))/ncells
q = np.zeros((totcells, ncells))

def init(board):
    global p, totcells
    initBoard(board)

def initBoard(board):
    global ncells, p

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
                    prob[int(k)-1] = randint(1,n)
            prob = prob/np.sum(prob)
            p[i * ncells + j] = prob

def printBoard():
    global ncells, p

    for i in range(ncells):
        for j in range(ncells):
            print(str(p[i*ncells + j]), end="\n")
        print("\n\n")


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


def computeQ():
    global ncells, p, q
    q = np.zeros((totcells, ncells))

    for i in range(totcells):
        for lb in range(ncells):
            for j in range(totcells):
                for mu in range(ncells):
                    q[i][lb] = q[i][lb] + compatibility(i, j, lb, mu) * p[j][mu]
    return q

def updateP():
    global p, totcells
    q = computeQ()
    numerator = p * q

    # normalize vector
    row_sums = numerator.sum(axis=1)
    numerator = numerator / row_sums[:, np.newaxis]
    return numerator

def averageConsistency():
    global ncells, p
    return np.sum(p*q)

def updateProbabilities():
    global ncells, p

    prev = 0
    diff = 1
    t = 0
    while diff > 0.01:
        p = updateP()
        avg = averageConsistency()
        diff = avg-prev
        print("Average diff: "+ str(diff)+" t: "+str(t)+"")
        prev = avg
        t+=1

def printCandidates():
    global totcells, ncells
    for i in range(totcells):
        pos = np.argmax(p[i])
        if i % ncells == 0:
            print("")
        print(str(pos+1)+" ", end ="")

def solve_relaxationLabeling(board):
    global ncells,totcells, p
    init(board)

    updateProbabilities()
    cells = []
    for i in range(totcells):
        pos = np.argmax(p[i])
        cells.append(pos + 1)

    for i in range(totcells):
        if i % ncells == 0:
            print("")
        print(cells[i], end=" ")
