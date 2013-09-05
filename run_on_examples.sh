#!/bin/bash

rm -rf venv-run-examples
virtualenv venv-run-examples
. venv-run-examples/bin/activate

pip install git+ssh://grizzly/var/git/dependency_tests
pip install nose

venv-run-examples/bin/nosetests --nologcapture --with-dependency --with-xunit --xunit-file=./examples_out.xml --with-id --verbose examples
