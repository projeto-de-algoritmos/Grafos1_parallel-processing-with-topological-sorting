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
def sub(x: int, y: int):
    return x - y

@lazy
@delay
def div(x: int, y: int):
    return x // y

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

    expression = mult(add(sub(attr_val(3),add(attr_val(12),attr_val(14))),attr_val(5)),div(add(attr_val(1),attr_val(1)),attr_val(3)))

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
    print("Simulating expressions execution")
    print("1 second = 1 cpu cycle\n")
    print("Executing the expression sequentially")
    start = time.time()

    expression = create_expression()
    response = expression()

    end = time.time()

    clear_graphs()

    print(f"Result of expression: {response}")
    print(f"Time of execution: {end - start:.2f}s")

    expression = create_expression()

    # PARALLEL EXECUTION
    print("\nExecuting the expression in parallel (unlimited CPUS)")

    start = time.time()

    # running topological sorting
    t_sort = topological_sorting(relational_graph.copy(), count_graph.copy(), graph.copy())

    response = process(t_sort, count_graph.copy(), relational_graph.copy())

    end = time.time()

    # Number of CPUs to be used in cicles measurement
    CPUS = 4
    cicles = count_cycles(t_sort.copy(), relational_graph.copy(), CPUS)

    print(f"Result of expression: {response}")
    print(f"Time of execution: {end - start:.2f}s")

    print("\nCycles counting for fixed number of cores:")
    print(f"It takes {count_cycles(t_sort.copy(), relational_graph.copy(), 2)} cycles to execute the expression using 2 CPUS")
    print(f"It takes {count_cycles(t_sort.copy(), relational_graph.copy(), 3)} cycles to execute the expression using 3 CPUS")
    print(f"It takes {count_cycles(t_sort.copy(), relational_graph.copy(), 4)} cycles to execute the expression using 4 CPUS")
    print(f"It takes {count_cycles(t_sort.copy(), relational_graph.copy(), 5)} cycles to execute the expression using 5 CPUS")
    print(f"It takes {count_cycles(t_sort.copy(), relational_graph.copy(), 10)} cycles to execute the expression using 10 CPUS")
    print(f"It takes {count_cycles(t_sort.copy(), relational_graph.copy(), 50)} cycles to execute the expression using 50 CPUS")
