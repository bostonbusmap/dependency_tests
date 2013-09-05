#!/bin/bash

venv/bin/nosetests --nologcapture --with-xunit --xunit-file=./examples_out.xml --dependency examples
