#!/bin/bash
set -e

rm -rf venv-run-examples
virtualenv venv-run-examples
. venv-run-examples/bin/activate

pip install -r requirements.txt
python setup.py install

venv-run-examples/bin/nosetests --nologcapture --with-dependency --with-xunit --xunit-file=./examples_out.xml --verbose examples
