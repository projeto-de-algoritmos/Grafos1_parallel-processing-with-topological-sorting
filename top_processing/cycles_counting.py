from collections import deque
from top_processing.topological import topological_sorting

def count_cycles(topological_sort: list, graph: dict, available_cores: int):
    '''
    This function greedily Walk through topological_sort list counting
    how many CPU cycles are needed to perform all operations
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

