"""
This module create 2 graphs. 

The count_graph variable have a dict that represents
for each key the number of other nodes that this node
have depencies

The relational_graph is another dict that represents the
actual graph, each node is a python object id (see id 
built-in function) and have edges to others objects.

Finally, the module have a cache system. For every node the response
if filled into the cache to don't waste time processing this again.
This feature implies that all functions need to be stateless/thread-safe.

The idea of the module is construct a DAG graph that will be used into the topological
sorting algorithm to process some tasks in a processing pool.
"""

import logging

logger = logging.getLogger(__name__)

# Count graph, each value is the number of nodes with reference to
# a object
count_graph = {}

# Relantional graph: just a normal graph that uses python object id
relational_graph = {}

# Save the response of some nodes and is used in consective calls
cache = {}

class Evaluate:
    """
    This class makes the function add lazyness to the functions
    Every evaluated response is saved into cache to be used again
    """

    def __init__(self, function, *args, **kwargs):

        self.function = function
        self.args = args
        self.kwargs = kwargs

    @staticmethod
    def try_evaluate(obj):
        """
        Try to evaluate the object if is a Evaluate object.
        In case of instance(obj, Evaluate) the response is 
        cached
        """
        response = obj
    
        if isinstance(obj, Evaluate):
            response = obj()

            logger.debug(
                f"Inserting a response into cache for {id(obj)}"
            )

            cache[id(obj)] = response
            
        return response

    def __call__(self):

        response = None

        # return the cached response if already have one
        if cache.get(id(self), False):
            logger.debug(f"Return cache response for {id(self)}")
            response = cache.get(id(self))

        else:
            # evaluate the object and use try_evaluate to cache the response
            method = self.function

            self.args = tuple(map(self.try_evaluate, self.args))

            #TODO(felipe) create kwargs evaluation

            response = method(*self.args, **self.kwargs)

            # If somehow the response is a Evalute object
            response = self.try_evaluate(response)

        return response

def lazy(function):
    """
    This function is a decorator that will 
    makes a function be able to receive
    promise and return then.

    This function create the count_graph and relational_graph
    """

    def decorated(*args, **kwargs):

        # create a node
        value = Evaluate(function, *args, **kwargs)

        # Add references in each graph
        count_graph[id(value)] = 0
        relational_graph[id(value)] = []

        # Adding information about edges
        for arg in args:
            if isinstance(arg, Evaluate):
                count_graph[id(value)] += 1
                relational_graph[id(arg)].append(id(value))

        return value

    return decorated

