import queue
from random import randint


class AssignQueue:
    assign_queue = queue.Queue(0)

    @staticmethod
    def push(value):
        AssignQueue.assign_queue.put(value)
        return True

    @staticmethod
    def pop():
        value = AssignQueue.assign_queue.get()
        return value

    @staticmethod
    def empty():
        return AssignQueue.assign_queue.empty()

class Value:
    def __init__(self, value, x, y):
        self.val = value
        self.x = x
        self.y = y

class State:

    def __init__(self, board):
        ncells = len(board)
        self.blockSize = ncells  # blocks have dimension ncells x ncells
        self.counter = 0
        self.initBoard(board)
        if not self.boardHasSolution():
            raise Exception("No possible solutions can be found for this configuration")

    def initBoard(self, board):
        ncells = self.blockSize
        self.cells = []
        for i in range(0, ncells*ncells):
            self.cells.append(['0',[str(i) for i in range(1,ncells+1)]])

        for i in range(0,self.blockSize):
            for j in range(0, self.blockSize):
                if board[i][j] != '0':
                    value = Value(str(board[i][j]),i,j)
                    if not self.assignValue(value):
                        return False
        return True

    def boardHasSolution(self):
        for i in range(0, self.blockSize):
            for j in range(0, self.blockSize):
                domainSet = self.cells[i * self.blockSize + j][1]
                val = self.cells[i * self.blockSize + j][0]
                if len(domainSet) == 0 and val == '0':
                    return False
        return True

    def assignValue(self, value):
        if self.satisfyConstraints(value):
            self.cells[value.x * self.blockSize + value.y] = [str(value.val),[]]
            self.counter = self.counter + 1
            return True
        # Not valid! Value doesn't satisfy domain constraints!
        return False

    def satisfyConstraints(self, value):
        return self.isEmpty(value.x,value.y) and self.squareConstraint(value) and self.propagateColumn(value) and self.propagateRow(value)

    def propagateColumn(self, value):
        columns = list(range(0, self.blockSize))

        for j in columns:
            if not self.removeConstraintValue(value.x, j, value):
                return False
        return True

    def propagateRow(self, value):
        rows = list(range(0, self.blockSize))
        for i in rows:
            if not self.removeConstraintValue(i, value.y, value):
                return False
        return True

    def squareConstraint(self, value):
        start_x = value.x - value.x%3
        start_y = value.y - value.y%3

        for i in range(start_x, start_x +3):
            for j in range(start_y, start_y + 3):
                if not self.removeConstraintValue(i,j,value):
                    return False
        return True

    def indirectConstraint(self):
        indirect = False
        for i in [0,3,6]:
            for j in [0,3,6]:
                occ = [Value(0, 0, 0)] * self.blockSize
                for x in range(i,i+3):
                    for y in range(j,j+3):
                        domainSet = self.cells[x * self.blockSize + y][1]
                        for k in domainSet:
                            k = int(k)
                            occ[k-1] = Value(occ[k-1].val+1,x,y)
                u = 0
                valid = False
                while u < self.blockSize and not valid:
                    if occ[u].val == 1:
                        self.assignValue(Value(str(u+1), occ[u].x, occ[u].y))
                        valid = indirect = True
                    u = u + 1
        return indirect


    def removeConstraintValue(self, i, j, value):
        domainSet = self.cells[i * self.blockSize + j][1]
        val = self.cells[i * self.blockSize + j][0]

        if val == value.val:
            return False

        if value.val in domainSet:
            domainSet.remove(value.val)

        if len(domainSet) == 1:
            assign = Value(domainSet[0],i,j)
            AssignQueue.push(assign)
        return True

    def print(self):
        for i in range(0,self.blockSize):
            print("")
            for j in range(0, self.blockSize):
                print(str(self.cells[i*self.blockSize + j][0]), end = " ")

    def printDomains(self):
        for i in range(0,self.blockSize):
            print("")
            for j in range(0, self.blockSize):
                print(str(self.cells[i*self.blockSize + j][1]), end = "\t\t")

    def indexMinDomain(self):
        min = 10
        x, y = -1, -1
        #print("\n===========(==========================\n")
        for i in range(0,self.blockSize):
            for j in range(0, self.blockSize):
                domainSet = self.cells[i * self.blockSize + j][1]
                l = len(domainSet)
                if l < min and l > 0:
                    min = l
                    x = i
                    y = j
        return x,y

    def guess(self, i, j):
        domainSet = self.cells[i * self.blockSize + j][1]
        #val = domainSet[0] # Deterministic approach
        r = randint(0, len(domainSet)-1) # random approach
        val = domainSet[r]
        domainSet.remove(val)
        return Value(val, i, j)

    def isUnique(self, i,j):
        return len(self.cells[i * self.blockSize + j][1])== 1

    def getDomainSet(self, i,j):
        return self.cells[i * self.blockSize + j][1]

    def getValue(self,i,j):
        return self.cells[i * self.blockSize + j][0]

    def isEmpty(self, i,j):
        return (self.cells[i * self.blockSize + j][0] == '0')

    def isFinish(self):
        return self.counter == 81
