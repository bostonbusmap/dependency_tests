from setuptools import setup, find_packages

setup(name='dependency_tests',
      version="0.1",
      packages=find_packages(),
      entry_points = {
        'nose.plugins.0.10': [
            'dependency_tests = dependency_tests:DependencyTests'
            ]
        },
      # ...
      )
