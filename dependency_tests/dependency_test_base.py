import inspect
import networkx

state = {}

def requires(dependencies):
    if type(dependencies) == str:
        dependency_list = [dependencies]
    else:
        dependency_list = dependencies

    def fn(func):
        def wrapped(self, *args, **kwargs):
            func(self, *args, **kwargs)
        wrapped._dependency_list = dependency_list
        return wrapped
    return fn
    

class DependencyTestBase(unittest.TestCase):
    def execution_order(self):
        """Iterate over methods in this class and return an ordered list
        based on dependencies"""
        # map of method name to a list of required methods
        root = "setUp"
        dependency_map = {root : []}

        methods = inspect.getmembers(self)
        for method_name, method in methods:
            if method_name.startswith("test_"):
                dependency_list = getattr(method, "_dependency_list", [])
                dependency_map[method_name] = [root] + dependency_list

        graph = networkx.DiGraph()
        for key, vals in dependency_map.iteritems():
            for val in vals:
                graph.add_edge(key, val)

        dependency_order = networkx.topological_sort(graph)

        return dependency_order

    @requires
    def test_bulk_queue(self):
        print "running test_bulk_queue..."

    def test_other(self):
        print "running test_other..."

    @requires("test_bulk_queue")
    def test_basic(self):
        print "running test_basic"

    def setUp(self):
        pass

    def execute(self):
        pass


def main():
    print DependencyTestBase().execution_order()

if __name__ == "__main__":
    main()
