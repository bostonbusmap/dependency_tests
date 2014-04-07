This code was developed at the Gygi proteomics lab at Harvard Medical by George Schneeloch.

This is a Python nose plugin which reorders tests in some order based on @requires annotations.

## Why

We run a series of jobs which can take a long time. I recently learned about Docker and wanted to write functional tests which would each run in a Docker container. A Docker container is a lightweight process whose results are version-controlled, allowing you to easily go back and see the results of previous tests. Since the tests are time consuming I wanted to have them run incrementally, depending on the results of a previous test which ran in its own Docker container. In our case we can run a job which takes 30 minutes and then run other tests which depend on the results of that job, without executing that job again.


## Usage

The basic steps are:
 - `python setup.py install`
 - Add `from dependency_tests.plugin import requires` at the top of your test case.
 - Add the @requires attribute on test methods to specify which tests should run before other tests.
 - Run nose with '--with-dependency' to enable this plugin.

See `examples/test_basic.py` for a working example, and `run_on_examples.sh` for a script to run it.

## Caveat

This is not well tested at all. It will probably fall apart for non-trivial cases, but I accept pull requests!

## License

GPL, since this is adapted from GPL'ed code.
