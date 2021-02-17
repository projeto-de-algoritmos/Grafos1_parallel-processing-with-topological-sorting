import logging

logger = logging.getLogger(__name__)

count_graph = {}
relational_graph = {}
cache = {}

class Evaluate:

    def __init__(self, function, *args, **kwargs):

        self.function = function
        self.args = args
        self.kwargs = kwargs

    def __call__(self):

        def try_evaluate(obj):


            if isinstance(obj, Evaluate):

                return obj()

            return obj

        if cache.get(id(self), False):
            logger.debug(f"Return cache response for {id(self)}")
            return cache.get(id(self))

        method = self.function

        self.args = tuple(map(try_evaluate, self.args))

        #TODO(felipe) create kwargs evaluation

        response = method(*self.args, **self.kwargs)
        response =  try_evaluate(response)

        logger.debug(f"Inserting a response into cache for {id(self)}")
        cache[id(self)] = response

        return response

def lazy(function):

    def decorated(*args, **kwargs):

        value = Evaluate(function, *args, **kwargs)

        count_graph[id(value)] = 0
        relational_graph[id(value)] = []

        for arg in args:
            if isinstance(arg, Evaluate):
                count_graph[id(value)] += 1
                relational_graph[id(arg)].append(id(value))

        return value

    return decorated

        
