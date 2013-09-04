import networkx
import unittest

from nose import loader
from nose.suite import ContextSuite

from nose.plugins import Plugin

from inspect import isfunction, ismethod
from nose.util import (getpackage, isclass, isgenerator, ispackage,
                       resolve_name, transplant_func, transplant_class)
from nose.case import FunctionTestCase, MethodTestCase
from nose.failure import Failure

import logging
import os
log = logging.getLogger('nose.plugins.step')

# heavily borrowed from https://gist.github.com/Redsz/5736166
# makeTest from https://gist.github.com/andresriancho/3844715

def requires(*args):
    if len(args) == 0:
        dependency_list = []
    elif len(args) == 1:
        if type(args[0]) == str:
            dependency_list = [args[0]]
        else:
            dependency_list = args[0]
    else:
        dependency_list = args

    def fn(func):
        func._dependency_list = dependency_list
        return func
    return fn
    
class DependencyTests(Plugin):
    def options(self, parser, env=os.environ):
        Plugin.options(self, parser, env)
        parser.add_option('--dependency', action='store_true', dest='dependency',
                          help="Order tests according to @requires decorators")

    def configure(self, options, conf):
        Plugin.configure(self, options, conf)
        if options.dependency:
            self.enabled = True

    def Dependency_loadTestsFromTestCase(self, cls):
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
                graph.add_edge(val, key)
            graph.add_edge(key, "root")

        dependency_order = networkx.topological_sort(graph)

        tests_in_order = [test_map[test_name] for test_name in dependency_order
                          if test_name in test_map]

        yield ContextSuite(tests_in_order)

    def makeTest(self, obj, parent=None):
        """Given a test object and its parent, return a test case
        or test suite.
        """
        ldr = loader.TestLoader()
        if isinstance(obj, unittest.TestCase):
            return obj
        elif isclass(obj):
            if parent and obj.__module__ != parent.__name__:
                obj = transplant_class(obj, parent.__name__)
            if issubclass(obj, unittest.TestCase):
                # Randomize the order of the tests in the TestCase
                return self.Dependency_loadTestsFromTestCase(obj)
            else:
                return ldr.loadTestsFromTestClass(obj)
        elif ismethod(obj):
            if parent is None:
                parent = obj.__class__
            if issubclass(parent, unittest.TestCase):
                return parent(obj.__name__)
            else:
                if isgenerator(obj):
                    return ldr.loadTestsFromGeneratorMethod(obj, parent)
                else:
                    return MethodTestCase(obj)
        elif isfunction(obj):
            if parent and obj.__module__ != parent.__name__:
                obj = transplant_func(obj, parent.__name__)
            if isgenerator(obj):
                return ldr.loadTestsFromGenerator(obj, parent)
            else:
                return FunctionTestCase(obj)
        else:
            return Failure(TypeError,
                           "Can't make a test from %s" % obj)
