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
    '''
    This function generates a list which represents the topological sort of operations graph from left to right
    '''
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

def count_cycles(topological_sort: list, graph: dict, available_cores: int):
    '''
    This function greedily Walk through topological_sort list counting how many CPU cycles are needed to perform all operations
    The answer may vary according to available_cores
    '''
    dependencies_count = {}

    for node in topological_sort:
        dependencies_count[node] = 0

    for node in topological_sort:
        for operation in graph[node]:
            dependencies_count[operation] += 1

    cores_left = available_cores
    cycles_total = 1

    to_visit = deque(topological_sort)

    operations_being_perfomed = []

    while len(to_visit) > 0:
        if cores_left < 1:
            cores_left = available_cores
            cycles_total += 1

            for node in operations_being_perfomed:
                for operation in graph[node]:
                    dependencies_count[operation] -= 1
            
            operations_being_perfomed = []

        curr_operation = to_visit[0]

        if dependencies_count[curr_operation] > 0:
            cores_left = 0
            continue

        to_visit.popleft()
        operations_being_perfomed.append(curr_operation)
        cores_left -= 1
    
    return cycles_total
        

def consume(node):
    return node()
