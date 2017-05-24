.. _testing:

Automated tests
===============


The :mod:`tests` package provides automated testing for
*`pymenu`*.

Tests are known to assess software behavior and find bugs. They are also
used as part of the code's documentation, as a design tool or for preventing
regressions.

See also:

* http://stackoverflow.com/questions/4904096/whats-the-difference-between-unit-functional-acceptance-and-integration-test
* http://stackoverflow.com/questions/520064/what-is-unit-test-integration-test-smoke-test-regression-test


Unit tests
----------

Exercise the smallest pieces of testable software in the application to
determine whether they behave as expected.

Unit tests should not

* call out into (non-trivial) collaborators,
* access the network,
* hit a database,
* use the file system or
* spin up a thread.

Most of the unit tests can be found directory in the code documentation
and are run using `doctest`_. When they cannot be simple or extensible
enough with impeding readability, they should be written in the
:mod:`tests.unit` package.

.. _`doctest`: https://docs.python.org/3/library/doctest.html


Integration tests
-----------------

Verify the communication paths and interactions between components to detect
interface defects.

The line between unit and integration tests may become blurry. When in doubt,
you are most certainly thinking integration tests.  Write those in the
:mod:`tests.integration` package.


Functional tests
----------------

Functional tests check a particular feature for correctness by comparing
the results for a given input against the specification. They are often used
as an executable definition of a user story. Write those in the
:mod:`tests.functional` package.


Regression tests
----------------

A test that was written when a bug was found (and then fixed). It ensures
that this specific bug will not occur again. The full name is *non-regression
test*. It can also be a test made prior to changing an application to make
sure the application provides the same outcome. Put these in the
:mod:`tests.regression` package.
