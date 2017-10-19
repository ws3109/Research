def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    return 0 if val == 0 else 1 if val > 0 else 2

def onSegment(p, q, r):
    return q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1])

def doIntersect(p1, q1, p2, q2):
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)
    if o1 != o2 and o3 != o4:
        return True
    if o1 == 0 and onSegment(p1, p2, q1):
        return True
    if o2 == 0 and onSegment(p1, q2, q1):
        return True
    if o3 == 0 and onSegment(p2, p1, q2):
        return True
    if o4 == 0 and onSegment(p2, q1, q2):
        return True
    return False

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])  # Typo was here
    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]
    div = det(xdiff, ydiff)
    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return (x, y)

def isUnitDiagonal(p, q):
    return abs(p[0] - q[0]) == 1 and abs(p[1] - q[1]) == 1

def l1_dist(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1])