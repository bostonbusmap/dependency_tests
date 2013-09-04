from setuptools import setup, find_packages

setup(name='dependency_tests',
      version="0.1",
      install_requires=["networkx", "nose"],
      packages=find_packages(),
      entry_points = {
        'nose.plugins.0.10': [
            'dependency_tests = dependency_tests.dependency_test_base:DependencyTests'
            ]
        },
      # ...
      )
