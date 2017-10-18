import matplotlib.pyplot as plt

def plot(size, lines1, lines2, crossings, save_image = False, image_folder = None, image_name = None):
    lines1, lines2 = set(lines1), set(lines2)
    x, y = zip(*[(x, y) for x in range(size) for y in range(size)])
    plt.plot([x for x in range(size)], [y for _ in range(size)], 'ko', markersize = 2)
    if len(crossings) > 0:
        cx, cy = zip(*crossings)
        plt.plot(cx, cy, 'o', markersize = 10, color = 'k', mfc ='none', markeredgewidth= 1)
    for p, q in lines1.intersection(lines2):
        plt.plot([p[0], q[0]], [p[1], q[1]], 'g')
    for p, q in lines1.symmetric_difference(lines2):
        if (p, q) in lines1:
            plt.plot([p[0], q[0]], [p[1], q[1]], 'b')
        else:
            plt.plot([p[0], q[0]], [p[1], q[1]], 'r')
    plt.axis([-2, size + 2, -2, size + 2])
    plt.title('There are %d crossings.' % (len(crossings)))
    if save_image:
        plt.savefig(image_folder + image_name)
    else:
        plt.show()
    plt.cla()
