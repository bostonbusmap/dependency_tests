import unittest
from dependency_tests.dependency_test_base import requires

class TestBasic(unittest.TestCase):
    @requires("test_b")
    def test_a(self):
        print "a"

    def test_b(self):
        print "b"

    @requires("test_d", "test_h")
    def test_e(self):
        print "e"

    @requires("test_e")
    def test_f(self):
        print "f"

    @requires("test_h")
    def test_g(self):
        print "g"

    def test_h(self):
        print "h"

    @requires(["test_d", "test_b"])
    def test_c(self):
        print "c"

    def test_d(self):
        print "d"


class TestBasicWithCycle(unittest.TestCase):
    @requires("test_b")
    def test_a(self):
        print "a"

    def test_b(self):
        print "b"

    @requires("test_d", "test_f")
    def test_e(self):
        print "e"

    @requires("test_e")
    def test_f(self):
        print "f"

    @requires("test_h")
    def test_g(self):
        print "g"

    def test_h(self):
        print "h"

    @requires(["test_d", "test_b"])
    def test_c(self):
        print "c"

    def test_d(self):
        print "d"


