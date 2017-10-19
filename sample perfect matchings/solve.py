import os
import pickle
import numpy as np
import itertools
from os import listdir
from os.path import isfile, join
from MatchingOnLattice import *
from plotFunctions import *

moves = [(-1, 0), (1, 0), (0, 1), (0, -1)]
move_func = lambda x, y: (x[0] + y[0], x[1] + y[1])

def findCrossings(init_edges_list, final_edges_dict):
    count, crossings = 0, []
    valid_init_edges = [(p, q) for p, q in init_edges_list if isUnitDiagonal(p, q)]
    for p1, q1 in valid_init_edges:
        p2_candidates = [p2 for p2 in map(move_func, [p1] * len(moves), moves) if p2 in final_edges_dict]
        for p2 in p2_candidates:
            q2 = final_edges_dict[p2]
            if isUnitDiagonal(p2, q2) and len(set([p1, p2, q1, q2])) == 4 and doIntersect(p1, q1, p2, q2):
                crossings.append(line_intersection((p1, q1), (p2, q2)))
    return set(crossings)

def generateMatchings(size, mixingTime, numSamples, horizontal = True):
    print('Generating matchings on lattice of size %d start from %s matching' % (size, 'horizontal' if horizontal else 'vertical'))
    return MatchingOnLattice(size, size, horizontal).getSamples(mixingTime = mixingTime, numSamples = numSamples)

def combineInitAndFinal(size, init_samples, final_samples, init_final_path_and_file):
    print('Generating pairs of initial and final matching on lattice of size %d.' % (size))
    crossing_list = []
    init_edges, init_point2point = zip(*init_samples)
    final_edges, final_point2point = zip(*final_samples)
    for i, j in itertools.product([i for i in range(len(init_edges))], [j for j in range(len(final_edges))]):
        if sorted(init_edges[i]) != sorted(final_edges[j]):
            crossings = findCrossings(init_edges[i], final_point2point[j])
            if len(crossings) > 0:
                crossing_list.append((init_edges[i], final_edges[j], crossings))
    if len(crossing_list) > 0:
        with open(init_final_path_and_file, 'wb') as handle:
            pickle.dump((size, crossing_list), handle)

def analyze(pair_folder, stat_folder):
    files = sorted([f for f in listdir(pair_folder) if isfile(join(pair_folder, f))])
    max_num_crossing = {}
    for file in files:
        with open(pair_folder + file, 'rb') as handle:
            size, crossing_list = pickle.load(handle)
        _, _, crossings = zip(*crossing_list)
        max_num_crossing[size] = max([len(x) for x in crossings])
    sizes = np.array(sorted(list(max_num_crossing.keys())))
    num_crossings = [max_num_crossing[size] for size in sizes]
    ratios = num_crossings / sizes ** 2
    with open(stat_folder + 'data.txt', 'w') as f:
        f.write('\n'.join(map(str, zip(sizes, num_crossings, ratios))))

def plotPairs(pair_file, image_folder, save_image = False):
    max_num_crossing, exist = {}, {}
    with open(pair_file, 'rb') as handle:
        size, crossing_list = pickle.load(handle)
    initials, finals, crossings = zip(*crossing_list)
    max_num_crossing[size] = max([len(x) for x in crossings])
    if save_image:
        max_pairs_indices = [i for i in range(len(crossings)) if len(crossings[i]) == max_num_crossing[size]]
        image_count = 0
        for i in max_pairs_indices:
            init_key, final_key = tuple(sorted(initials[i])), tuple(sorted(finals[i]))
            if init_key not in exist and final_key not in exist:
                exist[init_key], exist[final_key] = True, True
                plotTwoMatchings(size, initials[i], finals[i], crossings[i], save_image, image_folder, str(image_count)+'.png')
                image_count += 1

def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def main():
    mixingTime = [i for i in range(1000, 1001, 1000)]
    numSamples = [i for i in range(100, 101, 100)]
    sub_path = 'mixingTime-%d-numOfSamples-%d/'
    for t, num in itertools.product(mixingTime, numSamples):
        pair_folder = 'pairs/' + sub_path % (t, num)
        create_folder(pair_folder)
        image_folder = 'images/' + sub_path % (t, num)
        create_folder(image_folder)
        stat_folder = 'stat/' + sub_path % (t, num)
        create_folder(stat_folder)
        for size in range(4, 7, 2):
            # generate pairs
            samples_horizontal = generateMatchings(size, t, num, horizontal=True)
            samples_vertical = generateMatchings(size, t, num, horizontal=False)
            # # put them together
            pair_file = '%d.pickle' % (size)
            combineInitAndFinal(size, samples_horizontal, samples_vertical, pair_folder + pair_file)
            # generate images
            image_subfoler = image_folder + str(size) + '/'
            create_folder(image_subfoler)
            plotPairs(pair_folder + pair_file, image_subfoler, save_image = True)
            # analyze the result
            analyze(pair_folder, stat_folder)

main()
