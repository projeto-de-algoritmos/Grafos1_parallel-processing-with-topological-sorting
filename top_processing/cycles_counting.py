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

# def count_cycles(topological_sort: list, graph: dict, available_cores: int):
#     operation_status = {}
#     PENDING = 1
#     PERFORMED = 0

#     for operation in topological_sort:
#         operation_status[operation] = PENDING

#     print("operation status:", operation_status)

#     cycles = 1

#     print('Graph:', graph)
    
#     curr_perfoming_operations = []
#     curr_available_cores = available_cores
#     operations = deque(topological_sort)

#     print('Deque:', operations)

#     while len(operations) > 0:
#         # If there is no cores left
#         if curr_available_cores < 1:
#             curr_available_cores = available_cores
#             cycles += 1

#             # Sign every operation performed in this cycle
#             for operation in curr_perfoming_operations:
#                 operation_status[operation] = PERFORMED
#             curr_perfoming_operations = []
        
#         curr_operation = operations[0]

#         # Check if current operation has dependencies being performed at the same cycle
#         continue_to_next_cycle = False
#         for operation in graph[curr_operation]:
#             print('Checking', operation)
#             sleep(1)
#             # If there is such dependency, insert bubbles inside each core left
#             if operation_status[operation] == PENDING:
#                 curr_available_cores = 0
#                 continue_to_next_cycle = True
#                 break

#         if continue_to_next_cycle == True:
#             print('Continuei pro proximo')
#             continue

#         operations.popleft()
#         curr_perfoming_operations.append(curr_operation)
#         curr_available_cores -= 1

#     return cycles

def count_cycles(topological_sort: list, graph: dict, available_cores: int):
    dependencies_count = {}

    for node in topological_sort:
        dependencies_count[node] = 0

    for node in topological_sort:
        for operation in graph[node]:
            dependencies_count[operation] += 1

    # print('Topological sort:', topological_sort)
    # print('Graph:', graph)
    # print('Dependencies:', dependencies_count)

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
