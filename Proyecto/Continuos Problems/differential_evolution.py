from math import pi
from random import uniform, random


class Differential_evolution:
    # DE/rand/1/bin
    def __init__(self, function, k=60, d=30, x_low=-100, x_high=100, f=0.4, cr=0.9, generations_number=600):
        # NOTA: parameter F\in[0,1] and parameter CR\in[0,1]
        self.function = function
        self.D = d
        self.k = k #items in population
        self.F = f #scaling factor
        self.x_low = x_low
        self.x_high = x_high
        self.CR = cr #probability
        self.generations_number = generations_number
        self.plot_x = []  # saves gen_number
        self.plot_y = []  # saves_costs
        # initializing population
        self.population = []
        for i in range(0, k):
            new_vector = []
            for j in range(0, d):
                new_vector.append(uniform(x_low, x_high))
            self.population.append(new_vector)


    def recombination_operator(self, i, r_1, r_2, r_3):  # NOTA: they are indexes of the population
        j_rand = int(round(uniform(0, self.D - 1)))
        u_i = []
        for j in range(0, self.D):
            if random() < self.CR or j == j_rand:
                next_value = self.population[r_3][j] + self.F * (self.population[r_1][j] - self.population[r_2][j])

                # repair the value if is gretter or less than max and min values
                if next_value < self.x_low:
                    next_value = (self.population[i][j] + self.x_low) / 2
                elif next_value > self.x_high:
                    next_value = (self.population[i][j] + self.x_high) / 2
                else:
                    pass

                u_i.append(next_value)
            else:
                u_i.append(self.population[i][j])

        return u_i

    def calculate(self):
        j = 0
        while j <= self.generations_number:
            for i in range(0, self.k):
                # selecting 3 members of the population randomly
                r_1 = self.__random_populations_item()
                while i == r_1:
                    r_1 = self.__random_populations_item()

                r_2 = self.__random_populations_item()
                while r_1 == r_2 or i == r_2:
                    r_2 = self.__random_populations_item()

                r_3 = self.__random_populations_item()
                while r_3 == r_1 or r_3 == r_2 or r_3 == i:
                    r_3 = self.__random_populations_item()

                # Mutate and recombinate
                u_i = self.recombination_operator(i, r_1, r_2, r_3)
                # Replace
                eval_ = self.function(u_i)
                if self.function(self.population[i]) > eval_:
                    self.population[i] = u_i

                    # this is for the plot arrays
                    if len(self.plot_x) == 0 or self.plot_x[len(self.plot_x) - 1] != j:
                        # if the current generation does not have an eval cost in the plot array it must be added
                        self.plot_x.append(j)
                        self.plot_y.append(eval_)
                    elif self.plot_y[len(self.plot_y) - 1] > eval_:
                        # if the eval of the current gen is worst in the plot array, change it to better
                        self.plot_y[len(self.plot_y) - 1] = eval_

            j += 1

        # finding the minimun member of the population
        min_sol = None
        for i in range(0, len(self.population)):
            if min_sol is None or self.function(self.population[i]) < self.function(min_sol):
                min_sol = self.population[i]

        return min_sol, self.plot_x, self.plot_y

    def __random_populations_item(self):
        return int(round(uniform(0, len(self.population) - 1)))
