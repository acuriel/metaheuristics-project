from utils import *
import random
from operator import concat
import queue


class TSP_heuristic(object):
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.mapped_cities = {}

    def create_mapped_cities(self):
        self.mapped_cities = {}

        i = 0
        for c in self.coordinates:
            self.mapped_cities[c] = i
            self.mapped_cities[i] = c
            i += 1

    def calculate_cost(self, solution):
        cost = 0
        for i in range(0, len(solution) - 1):
            cost += euclidean_distance(solution[i], solution[i + 1])

        if len(solution) > 1:
            cost += euclidean_distance(solution[0], solution[len(solution) - 1])

        return cost

    def calculate_cost_edges(self, solution):
        cost = 0
        for c1, c2 in solution:
            cost += euclidean_distance(c1, c2)

        return cost

    def calculate_cost_mapped_cities(self, solution):
        cost = 0
        for i in range(0, len(solution) - 1):
            cost += euclidean_distance(self.mapped_cities[solution[i]], self.mapped_cities[solution[i + 1]])

        if len(solution) > 1:
            cost += euclidean_distance(self.mapped_cities[solution[0]], self.mapped_cities[solution[len(solution) - 1]])

        return cost

    def convert_to_edges(self, solution):
        edges = []
        for i in range(len(solution) - 1):
            edges.append((solution[i], solution[i + 1]))

        edges.append((solution[len(solution) - 1], solution[0]))

        return edges

    def convert_to_cities(self, solution):
        c1, search = solution[0]
        cities = [c1, search]
        solution.remove((c1, search))
        i = 0
        while i < len(solution) - 1:
            c1, c2 = solution[i]
            if c1 is search:
                search = c2
                cities.append(c2)
                solution.remove((c1, c2))
                i = -1
            elif c2 is search:
                search = c1
                cities.append(c1)
                solution.remove((c1, c2))
                i = -1
            i += 1

        return cities

    def convert_to_mapped_cities(self, solution):
        if len(self.mapped_cities.keys()) == 0:
            self.create_mapped_cities()

        result = []
        for t in solution:
            result.append(self.mapped_cities[t] + 1)

        return result

    def local_search(self, solution):
        # para cada par de aristas, las reconecta de la unica forma diferente posible, esto define un neighborhood
        # se toma el de menos costo del vecindario y se considera que es 2-opt, xq ningunc ambio de 2 aristas da mejor solucion
        best_solution = self.convert_to_edges(solution)
        best_cost = self.calculate_cost_edges(best_solution)
        test = self.calculate_cost(solution)
        change = True

        while change:
            change = False
            for i in range(0, len(best_solution) - 1):
                for j in range(i + 2, len(best_solution)):
                    city1, city2 = best_solution[i]
                    city3, city4 = best_solution[j]
                    dist_ant = euclidean_distance(city1, city2) + euclidean_distance(city3, city4)
                    dist_desp = euclidean_distance(city1, city3) + euclidean_distance(city4, city2)
                    if dist_ant > dist_desp:
                        change = True
                        best_solution[i] = (city1, city3)
                        best_solution[j] = (city2, city4)
                        best_solution = self.invert(i, j, best_solution)
                        best_cost -= dist_ant
                        best_cost += dist_desp

        return self.convert_to_cities(best_solution)

    def invert(self, i, j, sol):
        r = []
        for k in range(i + 1, j):
            x, y = sol[k]
            r.append((y, x))

        for k in range(0, len(r)):
            sol[j - k - 1] = r[k]

        return sol
