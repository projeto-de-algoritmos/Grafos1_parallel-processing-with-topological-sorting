from top_processing import lazy, relational_graph, count_graph, graph
from multiprocessing import Pool, Process, Barrier, Semaphore
from collections import deque
from time import sleep

def delay(function):

    def decorated(*args, **kwargs):

        #sleep(1)

        response = function(*args, **kwargs)

        return response

    return decorated


@lazy
@delay
def add(x, y):
    return x  + y

@lazy
@delay
def mult(x, y):
    return x*y

@lazy
@delay
def attr_val(x):
    return x

def dummy_topological_sorting(r_graph, c_graph, g):

    top_sort = []

    q = deque()

    for key, value in c_graph.items():
        if value == 0:
            q.append(key)
            c_graph[key] -= 1

    while len(q):

        item = q.popleft()

        top_sort.append(item)

        for key in r_graph[item]:
            c_graph[key] -= 1

            if c_graph[key] == 0:

                q.append(key)

    return top_sort


def consume(node):
    return node()

def counting_cicles_topological_sorting(r_graph, c_graph, g, processors: int) -> list:

    top_sort = []

    q = deque()

    for key, value in c_graph.items():
        if value == 0:
            q.append(key)
            c_graph[key] -= 1

    while len(q):

        item = q.popleft()

        top_sort.append(item)

        for key in r_graph[item]:
            c_graph[key] -= 1

            if c_graph[key] == 0:

                q.append(key)

    return top_sort

if __name__ == '__main__':


    ev = add(add(attr_val(5),attr_val(4)), mult(attr_val(10), attr_val(4)))
    print(dummy_topological_sorting(relational_graph, count_graph, graph))
