from random import uniform
from utils import euclidean_distance


class Random_TSP():
    def __init__(self, coordinates):
        self.coordinates = coordinates

    def random_solution(self):
        cost = 0
        pending = []
        result = []
        mapped_result = []
        mapped = {}

        for i in range(0, len(self.coordinates)):
            pending.append(self.coordinates[i])
            mapped[self.coordinates[i]] = i

        while len(pending) != 0:
            pos = int(round(uniform(0, len(pending) - 1)))
            result.append(pending[pos])
            mapped_result.append(mapped[pending[pos]] + 1)
            pending.remove(pending[pos])

            if len(result) >= 2:
                cost += euclidean_distance(result[len(result) - 1], result[len(result) - 2])

        if len(result) >= 2:
            cost += euclidean_distance(result[0], result[len(result) - 1])

        return result, cost
