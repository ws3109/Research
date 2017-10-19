import random
from Geometry import *
from plotFunctions import *
import matplotlib.pyplot as plt

class MatchingOnLattice:
    def __init__(self, row, column, horizontal = True):
        self.row, self.column = row, column
        us, vs = zip(*[((x, y), (x + horizontal, y + (1 - horizontal))) for x in range(0, column, 1 + horizontal) for y in range(0, row, 2 - horizontal)])
        self.ptop = dict(zip(us + vs, vs + us))
        self.edges = dict.fromkeys(list(zip(us, vs)))
        self.moves = [(i, j) for i in range(-1, 2) for j in range(-1, 2) if not (i == 0 and j == 0)]
        self.move_to_neighbor = lambda p: [(p[0] + m[0], p[1] + m[1]) for m in self.moves]
        self.rightOder = lambda p, q: (p, q) if p < q else (q, p)

    def neighbors(self, p):
        return [q for q in self.move_to_neighbor(p) if q[0] in range(0, self.column) and q[1] in range(0, self.row)]

    def valid(self, p, q):
        if l1_dist(p, q) > 1 and not isUnitDiagonal(p, q):
            return False
        lines = [self.rightOder(x, self.ptop[x]) for x in self.neighbors(p) if x != q]
        result = True not in [doIntersect(p, q, l[0], l[1]) for l in lines]
        return result

    def swap(self, u1, v1, u2, v2):
        self.edges.pop(self.rightOder(u1, v1))
        self.edges.pop(self.rightOder(u2, v2))
        self.edges[self.rightOder(u1, u2)] = True
        self.edges[self.rightOder(v1, v2)] = True
        self.ptop[u1], self.ptop[u2], self.ptop[v1], self.ptop[v2] = u2, u1, v2, v1

    def randomWalk(self):
        u1 = (random.randint(0, self.column - 1), random.randint(0, self.row - 1))
        v1 = self.ptop[u1]
        u2 = random.choice(self.neighbors(u1))
        if u2 != v1:
            v2 = self.ptop[u2]
            self.swap(u1, v1, u2, v2)
            if not self.valid(u1, u2) or not self.valid(v1, v2):
                self.swap(u1, u2, v1, v2)

    def getSamples(self, mixingTime = 10000, numSamples = 100):
        samples = []
        while len(samples) < numSamples:
            for i in range(mixingTime):
                self.randomWalk()
            samples.append((list(self.edges), dict(self.ptop)))
        return samples

