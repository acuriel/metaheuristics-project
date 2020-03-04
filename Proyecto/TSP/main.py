from utils import read_TSP_file, write_TSP_file, read_TSP_opt_file, convert_to_windows_line_sep
from os import listdir
from os.path import join, isfile, exists, splitext

from GRASP_TSP import GRASP_TSP
from Ant_colony_TSP import Ant_colony_TSP
from Random import Random_TSP
from TSP_heuristic import TSP_heuristic

import matplotlib.pyplot as plt


# plt.ion()


def plot_edges(tour, test_case, cost):
    x = []
    y = []

    for x1, y1 in tour:
        x.append(x1)
        y.append(y1)

    x.append(x[0])
    y.append(y[0])

    plt.title(test_case + ' - cost: ' + str(cost))
    plt.plot(x, y, 'o')
    plt.plot(x, y)
    plt.show()


def test_TSP(path, plot_=True):
    tests = listdir(path)
    opt_path = ''
    i = 1

    print('***Testing TSP***')
    for test_case in tests:
        file_path = join(path, test_case)

        if not isfile(file_path):
            continue

        try:
            coordinates = read_TSP_file(file_path)
        except:
            continue

        print('    file: {}'.format(file_path))
        opt_path = '{}.opt.tour'.format(file_path)

        random_with_2opt(coordinates, test_case)
        ant_colony(coordinates, test_case)
        grasp(coordinates, test_case, opt_path)

        print('======================================================')


def convert_to_string(list):
    l = []
    for i in list:
        l.append(str(i))

    return l


def grasp(coordinates, test_case, opt_path):
    g = GRASP_TSP(coordinates)
    g.RCL_lenght = int(round(len(coordinates) / 4)) + 1
    opt_tour_cities, cost_grasp, iteration, best_tour_grasp = g.calculate()
    print('        GRASP solution cost:       {} iter: {}'.format(cost_grasp, iteration))
    write_TSP_file(path, test_case + '.GRASP', convert_to_string(opt_tour_cities), str(cost_grasp))
    plot_edges(best_tour_grasp, test_case + ' GRASP', cost_grasp)

    if exists(opt_path):
        opt_tour = read_TSP_opt_file(opt_path)
        opt_cost = g.calculate_cost_mapped_cities(opt_tour)
        print('        Optimum cost:              {} '.format(opt_cost))

    return opt_cost


def ant_colony(coordinates, test_case):
    a = Ant_colony_TSP(coordinates)
    a.coordinates = coordinates
    result_cities, result_edges, cost_ant = a.calculate()
    print('        Ant colony solution cost:  {}'.format(cost_ant))
    write_TSP_file(path, test_case + '.ACO', convert_to_string(result_cities), str(cost_ant))
    plot_edges(result_edges, test_case + ' Ant Colony', cost_ant)


def random_with_2opt(coordinates, test_case):
    r = Random_TSP([])
    r.coordinates = coordinates

    result_random, cost_random = r.random_solution()
    print('        Random solution cost:      {}'.format(cost_random))
    plot_edges(result_random, test_case + ' Random', cost_random)

    tsp = TSP_heuristic(coordinates)

    tour_2opt = tsp.local_search(result_random)
    cities_2opt = tsp.convert_to_mapped_cities(tour_2opt)
    cost_2opt = tsp.calculate_cost(tour_2opt)
    print('        Local search 2opt:         {}'.format(cost_2opt))
    write_TSP_file(path, test_case + '.2opt', convert_to_string(cities_2opt), str(cost_2opt))
    plot_edges(tour_2opt, test_case + ' 2-opt', cost_2opt)


path = 'test_TSP'
test_TSP(path)
