from collections import deque

def topological_sorting(r_graph: dict, c_graph: dict, g: dict):
    """
    Topological sorting
    """

    # nodes without any other node with a edge
    q = deque()

    for key, value in c_graph.items():
        if value == 0:
            q.append(key)
            c_graph[key] -= 1

    top_sort = []

    while len(q):

        item = q.popleft()
        top_sort.append(item)

        for key in r_graph[item]:
            c_graph[key] -= 1

            if c_graph[key] == 0:
                q.append(key)

    return top_sort

