import matplotlib.pyplot as plt

def plotEdges(edges, color):
    for p, q in edges:
        plt.plot([p[0], q[0]], [p[1], q[1]], color, linewidth = 1)

def plotLattice(size):
    x, y = zip(*[(x, y) for x in range(size) for y in range(size)])
    plt.plot([x for x in range(size)], [y for _ in range(size)], 'ko', markersize = 1)
    plt.axis([-2, size + 2, -2, size + 2])

def plotTwoMatchings(size, lines1, lines2, crossings, save_image = False, image_folder = None, image_name = None):
    plotLattice(size)
    # plot crossings
    cx, cy = zip(*crossings)
    plt.plot(cx, cy, 'o', markersize=10, color='k', mfc='none', markeredgewidth=1)
    # plot two matchings
    lines1, lines2 = set(lines1), set(lines2)
    plotEdges(lines1.intersection(lines2), 'g')
    plotEdges(lines1 - lines2, 'r')
    plotEdges(lines2 - lines1, 'b')
    plt.title('There are %d crossings.' % (len(crossings)))
    if save_image:
        plt.savefig(image_folder + image_name)
    else:
        plt.show()
    plt.cla()
