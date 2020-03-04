from TSP_heuristic import TSP_heuristic
from utils import euclidean_distance
import random


class Ant_colony_TSP(TSP_heuristic):
    def __init__(self, coordinates, ants=10, a=2, b=3, p=0.6, iterations=100, do_local_search=True):
        self.a = a  # a->influencia de la feronoma
        self.b = b  # b->influencia de la heuristica
        self.p = p  # p->evaporacion de la feromona
        self.ants = ants
        super(Ant_colony_TSP, self).__init__(coordinates)

        self.iterations = iterations
        self.best_solution = []
        self.best_cost = None
        self.do_local_search = do_local_search

    def pheromone_update(self, solution_list, costs):
        # evaporation
        for i in range(0, len(self.pheromone)):
            for j in range(0, len(self.pheromone)):
                self.pheromone[i][j] = (1 - self.p) * self.pheromone[i][j]

        # reinforcement
        j = 0
        for solution in solution_list:
            for i in range(0, len(solution) - 1):
                self.pheromone[solution[i]][solution[i + 1]] += 100 / costs[j]
            j += 1

    def calculate(self):
        self.create_mapped_cities()

        # iniciar matriz de feromonas
        self.pheromone = []
        for i in range(0, len(self.coordinates)):
            self.pheromone.append([])
            for j in range(0, len(self.coordinates)):
                self.pheromone[i].append(1.0 / (float(len(self.coordinates) - 1)) * float(len(self.coordinates) - 1))

        for i in range(0, self.iterations):
            solutions = []
            costs = []
            for j in range(0, self.ants):
                solution = []
                cost = 0
                # create set of cities to select
                S = []
                for k in range(0, len(self.coordinates)):
                    S.append(k)
                # select start city
                r = S[int(round(random.uniform(0, len(S) - 1)))]
                solution.append(S[r])
                S.remove(S[r])

                # add cities to current solution
                while len(S) != 0:
                    r = random.random()
                    aux = 0
                    for k in range(0, len(S)):
                        aux += self.probability(solution[len(solution) - 1], S[k], S)
                        if aux >= r:
                            break

                    solution.append(S[k])
                    cost += euclidean_distance(self.mapped_cities[solution[len(solution) - 1]],
                                               self.mapped_cities[solution[len(solution) - 2]])
                    S.remove(S[k])

                solutions.append(solution)
                costs.append(cost)

                if self.best_cost is None or cost < self.best_cost:
                    # print (str(i) + ' ' + str(self.best_cost))
                    self.best_cost = cost
                    self.best_solution = solution

            # update pheromone
            self.pheromone_update(solutions, costs)

        result_edges = []
        for i in self.best_solution:
            result_edges.append(self.mapped_cities[i])

        if self.do_local_search:
            result_edges = self.local_search(result_edges)

        return self.convert_to_mapped_cities(result_edges), result_edges, self.best_cost

    def probability(self, i, j, S):
        den = 0
        for k in S:
            if k == i:
                continue
            den += (self.pheromone[i][k] ** self.a) * (self.nabla(i, k) ** self.b)

        if den == 0:
            return 0

        return (self.pheromone[i][j] ** self.a) * (self.nabla(i, j) ** self.b) / den

    def nabla(self, i, k):
        return 1.0 / euclidean_distance(self.mapped_cities[i], self.mapped_cities[k])

