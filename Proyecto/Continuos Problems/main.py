from math import sin, cos, pi
from differential_evolution import Differential_evolution
from matplotlib import pyplot


def return_spaces(n):
    s = ''
    for i in range(0, n):
        s += ' '

    return s


def proccess(func, dim):
    dif_func1 = Differential_evolution(func, d=dim)
    best_sol1, plot_x, plot_y = dif_func1.calculate()
    print 'Best solution:'

    if len(best_sol1) % 3 == 0:
        for i in range(0, len(best_sol1) - 2, 3):
            spa1 = 20
            spa2 = 20
            str1 = str(best_sol1[i])
            str2 = str(best_sol1[i + 1])
            str3 = str(best_sol1[i + 2])

            spa1 -= len(str1)
            spa2 -= len(str2)

            print str1 + return_spaces(spa1) + str2 + return_spaces(spa2) + str3

    print 'Cost:'
    print func(best_sol1)

    if len(plot_x) >= 150:
        # if the number of generation is big reduce dimension to plot
        new_x = []
        new_y = []
        for i in range(len(plot_x)):
            if i % 2 == 0:
                new_x.append(plot_x[i])
                new_y.append(plot_y[i])
    else:
        new_x = plot_x
        new_y = plot_y

    pyplot.plot(new_x, new_y)
    pyplot.plot(new_x, new_y, 'o')
    pyplot.show()


def test_function1(x):
    prod = 1
    sum = 0
    for i in range(0, len(x)):
        prod *= sin((x[i] ** 2))
        sum += x[i] ** 2 - 10 * cos(2 * pi * x[i])

    if prod == 1:
        return sum

    return prod + sum


def test_function2(x):
    prod = 1
    outter_sum = 0
    for i in range(0, len(x)):
        inner_sum = 0
        for j in range(0, len(x)):
            inner_sum += (x[i] ** 2) - 10 * cos(2 * pi * x[i])
        prod *= inner_sum

        outter_sum += cos(2 * pi * x[i])

    if prod == 1:
        return outter_sum

    return prod + outter_sum


def test_function3(x):
    sum = 0
    for c in x:
        sum += c * c

    return sum



# proccess(test_function1, 30)
# proccess(test_function2, 30)
# proccess(test_function3, 10)
