import copy

from labeling import solve_relaxationLabeling
from labelingVector import solve_relaxationLabeling
from state import *


def readSudoku(filename):
    with open(filename) as f:
        board = f.read().splitlines()
    board = [list(line) for line in board]
    return board

def cpb_sudoku_solver(board):
    isFinish = False
    StatesStack = list()
    current_state = State(board)
    while not isFinish:
        if not AssignQueue.empty():
            value = AssignQueue.pop()
            current_state.assignValue(value)
        else:
            indirect = current_state.indirectConstraint()
            if not(indirect):
                x, y = current_state.indexMinDomain()
                if x== -1 and y == -1:
                    if not (len(StatesStack) == 0):
                        current_state = StatesStack.pop()
                    else:
                        current_state.print()
                        raise Exception("No possible solution are discovered")
                else:
                    if current_state.isUnique(x, y):
                        current_state.assignValue(Value(current_state.getDomainSet(x, y)[0], x, y))
                    else:
                        guess = current_state.guess(x,y)
                        copy_state = copy.deepcopy(current_state)
                        StatesStack.append(copy_state)
                        current_state.assignValue(guess)
        isFinish = current_state.isFinish()
    current_state.print()

def findSolution(filename):
    board = readSudoku(filename)
    print("===========================\nConstraint propagation and backtracking")
    cpb_sudoku_solver(board)
    print("\n\n===========================\nRelaxation Labeling")
    solve_relaxationLabeling(board)

def main():
    findSolution("configurations/easy1.txt")

if __name__ == '__main__':
    main()