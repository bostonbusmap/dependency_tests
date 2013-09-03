import networkx

from nose import loader

from nose.plugins import Plugin

import os

# heavily borrowed from https://gist.github.com/Redsz/5736166

state = {}

def requires(dependencies):
    if type(dependencies) == str:
        dependency_list = [dependencies]
    else:
        dependency_list = dependencies

    def fn(func):
        def wrapped(*args, **kwargs):
            return func(*args, **kwargs)
        wrapped._dependency_list = dependency_list
        return wrapped
    return fn
    

class DependencyTests(Plugin):
    def options(self, parser, env=os.environ):
        Plugin.options(self, parser, env)
        parser.add_option('--dependency', action='store_true', dest='dependency',
                          help="Order tests according to @requires decorators")

    def configure(self, options, conf):
        Plugin.configure(self, options, conf)
        if options.steps:
            self.enabled = True

    def loadTestsFromTestCase(self, cls):
        l = loader.TestLoader()
        tmp = l.loadTestsFromTestCase(cls)

        # test name to test
        test_map = {}
        
        dependency_map = {}
        for test in tmp._tests:
            test_name = test.test._testMethodName

            test_map[test_name] = test
            func = getattr(cls, test_name)

            dependency_list = getattr(func, "_dependency_list", [])
            dependency_map[test_name] = dependency_list

        graph = networkx.DiGraph()
        for key, vals in dependency_map.iteritems():
            for val in vals:
                graph.add_edge(key, val)

        dependency_order = networkx.topological_sort(graph)

        tests_in_order = [test_map[test_name] for test_name in dependency_order]
        tmp._tests = tests_in_order
        return tmp
        

