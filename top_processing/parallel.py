from top_processing import lazy, relational_graph, count_graph, graph, Evaluate
from multiprocessing import Pool, Process, Barrier, Semaphore
from collections import deque
from time import sleep
from multiprocessing import Manager, Queue
from top_processing.topological import topological_sorting

def evaluate_task(function, args, kwargs, node_id, queue):
    """
    Execute a Evaluate node and insert the response
    on the queue
    """

    response = function(*args, **kwargs)

    queue.put((node_id, response))

def process(nodes, c_graph, r_graph):
    """
    Process algebric statements
    """

    cache = {}
    queue = deque()
    m_queue = Queue()
    last_key = None

    while True:

        # adding nodes with 0 references
        for key, count in c_graph.items():
            if count == 0:

                queue.append(key)

                c_graph[key] -=1
        
        # if don't have any, break
        if len(queue) == 0:
            break

        processes = []

        while len(queue):

            item = queue.popleft()
            item_id = item
            item = graph[item]

            function = item.function
            args = item.args
            args2 = []

            for arg in args:
                if isinstance(arg, Evaluate):
                    args2.append(cache[id(arg)] )
                else:
                    args2.append(arg)

            kwargs = item.kwargs

            p = Process(target=evaluate_task, args=(function, args2, kwargs, item_id, m_queue))
            processes.append(p)
            p.start()

        # joint all processes
        for process in processes:
            p.join()

        while not m_queue.empty():

            k = m_queue.get()
            node, response = k
            last_key = node
            cache[node] = response


            for item in r_graph[node]:
                c_graph[item] -=1

    m_queue.close()

    return cache[last_key]

