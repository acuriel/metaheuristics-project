import os.path as os
import heapq
from math import pow, sqrt
from os import linesep
from os.path import join


def read_TSP_file(path):
    file = open(path)
    coordinates = []

    while True:
        current_line = file.readline().split()
        if len(current_line) == 0:
            continue

        if current_line[0].startswith('DIMENSION'):
            dimension = int(current_line[len(current_line) - 1])
        if current_line[0].startswith('NODE_COORD_SECTION'):
            break

    while True:
        current_line = file.readline().split()
        if len(current_line)==0:
            continue
        coordinates.append((float(current_line[1]), float(current_line[2])))
        if int(current_line[0]) == dimension:
            break
    file.close()
    return coordinates


def write_TSP_file(path, test_case, result, cost):
    result_path = join(path, 'Results')
    file = open(join(result_path, test_case), 'w')  # creating result file

    file.write(cost + linesep)

    for c in result:
        file.write(c + linesep)

    file.close()


def read_TSP_opt_file(path):
    file = open(path)
    result = []
    dimension = 0
    while True:
        current_line = file.readline().split()
        if current_line[0] == 'DIMENSION':
            dimension = current_line[2]

        if current_line[0] == 'TOUR_SECTION':
            break

    while True:
        current_line = file.readline().split()[0]
        if current_line == '-1':
            break
        result.append(int(current_line) - 1)

    file.close()
    return result


def euclidean_distance(x, y):
    (x1, y1) = x
    (x2, y2) = y
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def initialize_array(count):
    list = []
    while len(list) != count:
        list.append(0)
    return list


def list_copy(list):
    new = []
    for c in list:
        new.append(c)

    return new


def convert_to_windows_line_sep(path):
    file = open(path, 'r')
    content = file.read()
    file.close()

    file = open(path, 'w')
    # content = content.replace('\n', '\n\r')
    content = content.replace('  ', '\n\r')
    file.write(content)
    file.close()


def checking_result(lenght, result):
    if lenght != len(result):
        return False

    list = []
    for i in range(0, lenght):
        list.append(False)

    try:
        for c in result:
            if list[c - 1] is True:
                return False
            list[c - 1] = True

    except:
        return False

    # no hago ningun ciclo despues para verificar que todos estan en True porque eso se infiere de que el lenght sea igual al de la lista y no visite ninguno dos veces
    return True


class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """

    def __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)
