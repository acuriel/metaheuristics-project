from TSP_heuristic import TSP_heuristic
from utils import initialize_array, PriorityQueue, euclidean_distance
import random

class GRASP_TSP(TSP_heuristic):
    def __init__(self, coordinates, RCL_lenght=15, iterations=50):
        super(GRASP_TSP, self).__init__(coordinates)

        self.RCL_lenght = RCL_lenght
        self.iterations = iterations
        # self.best_iteration = None

    def cities_count(self):
        return len(self.coordinates)

    def __construction(self):
        # la lista RLC contiene los k mejores candidatos
        # la otra lista contiene el resto de las arista que no pertenecen al camino ni a la RLC

        RCL = []
        visited = initialize_array(self.cities_count())
        other_edges = PriorityQueue()
        for i in range(0, len(self.coordinates) - 1):
            for j in range(i + 1, len(self.coordinates)):
                x, y = self.coordinates[i], self.coordinates[j]
                distance = euclidean_distance(x, y)
                other_edges.push((x, y), distance)

        for i in range(0, self.RCL_lenght):
            if other_edges.isEmpty():
                break
            RCL.append(other_edges.pop())

        tour = {}
        edges = 0
        while edges != self.cities_count() - 1:
            r = int(round(random.uniform(0, len(RCL) - 1)))
            (city1, city2) = RCL[r]

            if visited[self.mapped_cities[city1]] < 2 and visited[self.mapped_cities[city2]] < 2:
                if not city1 in tour:
                    tour[city1] = []
                if not city2 in tour:
                    tour[city2] = []

                tour[city1].append(city2)
                tour[city2].append(city1)
                if not self.__DFS(tour):
                    edges += 1
                    visited[self.mapped_cities[city1]] += 1
                    visited[self.mapped_cities[city2]] += 1
                else:
                    tour[city1].remove(city2)
                    tour[city2].remove(city1)

            # ya sea porque la arista se agrego al tour o porque la ciudad ya estaba visitada, removerla de la lista de candidatos y agregar otro elemento
            RCL.remove((city1, city2))
            if not other_edges.isEmpty():
                RCL.append(other_edges.pop())

        result = []
        for i in range(0, len(visited)):
            if visited[i] == 1:
                result = self.sort_tour(tour, current=self.mapped_cities[i])
                break

        return result

    def __DFS(self, tour, father=None):
        visited = initialize_array(self.cities_count())

        for i in range(0, len(visited)):
            if visited[i] is 0 and self.mapped_cities[i] in tour:
                if self.__DFS_for_loop_detection(tour, self.mapped_cities[i], visited):
                    return True
        return False

    def __DFS_for_loop_detection(self, tour, current_city, visited, father=None, ):
        for c in tour[current_city]:
            if c is father:
                continue
            if visited[self.mapped_cities[c]] is not 0:
                return True
            visited[self.mapped_cities[c]] = 1
            if self.__DFS_for_loop_detection(tour, c, visited, current_city, ):
                return True
        return False

    def calculate(self):
        self.create_mapped_cities()
        best_solution = None
        best_cost = None
        best_iteration = None
        i = 0
        while i < self.iterations:
            sol = self.__construction()
            better_sol = self.local_search(sol)
            current_cost = self.calculate_cost(better_sol)

            if best_solution is None or current_cost < best_cost:
                best_cost = current_cost
                best_solution = better_sol
                best_iteration = i

            i += 1

        return self.convert_to_mapped_cities(best_solution), best_cost, best_iteration, best_solution

    def sort_tour(self, tour, current, father=None):
        # convertir el diccionario en un ciclo de hamilton
        result = [current]
        father = current
        current = tour[current][0]
        result.append(current)
        while len(tour[current]) != 1:
            next1, next2 = tour[current]
            if father == next1:
                result.append(next2)
                father = current
                current = next2
            else:
                result.append(next1)
                father = current
                current = next1

        return result

        # if len(tour[current]) == 2:
        #     next = []
        #     neigh1, neigh2 = tour[current]
        #     if neigh1 != father:
        #         next = self.sort_tour(tour, neigh1, current)
        #     elif neigh2 != father:
        #         next = self.sort_tour(tour, neigh2, current)
        #
        #     next.append(current)
        #     return next
        #
        # else:  # solo tengo un vecino
        #     neigh1 = tour[current][0]
        #     if neigh1 != father:
        #         result = self.sort_tour(tour, neigh1, current)
        #         result.append(current)
        #         return result
        #     else:
        #         return [current]

