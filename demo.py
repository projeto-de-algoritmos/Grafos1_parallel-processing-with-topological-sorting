import time
from collections.abc import Callable
from top_processing import lazy, relational_graph, count_graph, graph, Evaluate
from top_processing.parallel import process
from top_processing.topological import topological_sorting
from top_processing import count_cycles

def delay(function: Callable, seconds:int = 1):
    """
    Waite few seconds before call a function
    """

    def decorated(*args, **kwargs):

        time.sleep(seconds)

        response = function(*args, **kwargs)

        return response

    return decorated

@lazy
@delay
def add(x: int, y: int):
    return x  + y

@lazy
@delay
def mult(x: int, y: int):
    return x*y

@lazy
@delay
def attr_val(x: int):
    return x

def create_expression():
    """
    Create the expression here
    """

    #define expression
    arg1: Evaluate = attr_val(5)
    arg2: Evaluate = attr_val(4)

    add_1: Evaluate = add(arg1, arg2)

    arg3: Evaluate = attr_val(10)
    arg4: Evaluate = attr_val(4)

    mult_1: Evaluate = mult(arg3, arg4)

    expression: Evaluate = add(add_1, mult_1)

    return expression

def clear_graphs():
    """
    Clear cache and other objects
    """

    graph.clear()
    count_graph.clear()
    relational_graph.clear()

if __name__ == '__main__':
 
    # SEQUENCIAL EXECUTION
    print("Execution the expression sequentially")
    start = time.time()

    expression = create_expression()
    response = expression()

    end = time.time()

    clear_graphs()

    print(f"Result of expression: {response}")
    print(f"Time of execution: {end - start:.2f}s")

    expression = create_expression()

    # PARALLEL EXECUTION
    print("Execution the expression in parallel")

    start = time.time()

    # running topological sorting
    t_sort = topological_sorting(relational_graph.copy(), count_graph.copy(), graph.copy())

    response = process(t_sort, count_graph.copy(), relational_graph.copy())

    end = time.time()

    # Number of CPUs to be used in cicles measurement
    CPUS = 4
    cicles = count_cycles(t_sort, relational_graph.copy(), CPUS)

    print(f"Number of cicles: {cicles}")
    print(f"Result of expression: {response}")
    print(f"Time of execution: {end - start:.2f}s")

