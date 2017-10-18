import random
from Geometry import *

class MatchingOnLattice:
    def __init__(self, row, column, horizontal = True):
        self.row, self.column, self.numV = row, column, row * column
        self.points = [(x, y) for x in range(column) for y in range(row)]
        if horizontal:
            us, vs = zip(*[((x, y), (x+1, y)) for x in range(0, column, 2) for y in range(0, row)])
        else:
            us, vs = zip(*[((x, y), (x, y + 1)) for x in range(0, column) for y in range(0, row, 2)])
        us, vs = list(us), list(vs)
        self.ptop = dict(zip(us + vs, vs + us))
        self.edges = dict.fromkeys(list(zip(us, vs)))

    def neighbors(self, p):
        candidates = []
        for mx in range(-1, 2):
            for my in range(-1, 2):
                tx, ty = mx + p[0], my + p[1]
                if (tx, ty) != (p[0], p[1]) and tx >= 0 and tx < self.column and ty >= 0 and ty < self.row:
                    candidates.append((tx, ty))
        return candidates

    def valid(self, p, q):
        l1_len = l1_dist(p, q)
        if l1_len > 2 or l1_len == 2 and not isUnitDiagonal(p, q):
            return False
        if l1_len == 1:
            return True
        nbors= [x for x in self.neighbors(p) if x != q]
        lines = [(x, self.ptop[x]) for x in nbors]
        for a, b in lines:
            if doIntersect(p, q, a, b):
                return False
        return True

    # Swap lines (u1, v1) and (u2, v2) to (u1, u2) and (v1, v2)
    def swap(self, u1, v1, u2, v2):
        self.edges.pop(tuple(sorted([u1, v1])))
        self.edges.pop(tuple(sorted([u2, v2])))
        self.edges[tuple(sorted([u1, u2]))] = True
        self.edges[tuple(sorted([v1, v2]))] = True
        self.ptop[u1], self.ptop[u2], self.ptop[v1], self.ptop[v2] = u2, u1, v2, v1

    def randomWalk(self):
        # First line segment
        index = random.randint(0, self.numV - 1)
        u1 = (index % self.column, index // self.column)
        v1 = self.ptop[u1]
        u1_nbors = self.neighbors(u1)
        u2 = random.choice(u1_nbors)
        if u2 != v1:
            v2 = self.ptop[u2]
            # we try to connect (u1, u2) and (v1, v2), remove first then to see if new edges are valid.
            self.swap(u1, v1, u2, v2)
            if not self.valid(u1, u2) or not self.valid(v1, v2):
                self.swap(u1, u2, v1, v2)

    def getSamples(self, mixingTime = 10000, numSamples = 100):
        i, samples = 0, []
        while len(samples) < numSamples:
            self.randomWalk()
            if i % mixingTime == 0:
                samples.append((list(self.edges), dict(self.ptop)))
            i += 1
        return samples
