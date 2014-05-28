import networkx
import unittest

from nose.plugins import Plugin

from inspect import isfunction, ismethod
from nose.case import FunctionTestCase, MethodTestCase
from nose.failure import Failure
from nose.util import (
    isclass,
    isgenerator,
    transplant_func,
    transplant_class
)

import logging
import os
log = logging.getLogger('nose.plugins.step')

# heavily borrowed from https://gist.github.com/Redsz/5736166
#  and https://gist.github.com/andresriancho/3844715
#  and https://github.com/erikrose/nose-progressive/blob/master/noseprogressive/plugin.py

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
        parser.add_option('--with-dependency', action='store_true', dest='dependency',
                          help="Order tests according to @requires decorators")

    def configure(self, options, conf):
        Plugin.configure(self, options, conf)
        if options.dependency:
            self.enabled = True

    def Dependency_loadTestsFromTestCase(self, cls):
        """Get tests from nose test runner, then sort the tests topologically"""
        l = self._loader
        tmp = l.loadTestsFromTestCase(cls)

        # test name to test
        test_map = {}
        
        # create a list of dependencies for each test method
        dependency_map = {}
        for test in tmp._tests:
            test_name = test.test._testMethodName

            test_map[test_name] = test
            func = getattr(cls, test_name)

            dependency_list = getattr(func, "_dependency_list", [])
            dependency_map[test_name] = dependency_list

        # sort dependency list topologically
        graph = networkx.DiGraph()
        for key, vals in dependency_map.items():
            for val in vals:
                graph.add_edge(val, key)
            graph.add_edge(key, "root")

        dependency_order = networkx.topological_sort(graph)

        tests_in_order = [test_map[test_name] for test_name in dependency_order
                          if test_name in test_map]

        tmp._tests = tests_in_order
        return tmp

    def prepareTestLoader(self, loader):
        self._loader = loader

    def makeTest(self, obj, parent=None):

        """Given a test object and its parent, return a test case
        or test suite.
        """
        ldr = self._loader
        if isinstance(obj, unittest.TestCase):
            return obj
        elif isclass(obj):
            if parent and obj.__module__ != parent.__name__:
                obj = transplant_class(obj, parent.__name__)
            if issubclass(obj, unittest.TestCase):
                # Sort the tests according to their dependencies
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
