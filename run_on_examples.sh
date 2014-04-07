#!/bin/bash
set -e

rm -rf venv-run-examples
virtualenv venv-run-examples
. venv-run-examples/bin/activate

python setup.py install

venv-run-examples/bin/nosetests --nologcapture --with-dependency --with-xunit --xunit-file=./examples_out.xml --verbose examples
