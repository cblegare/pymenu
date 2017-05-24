.. _setup:


setup module
============


The *setup.py* file is a swiss knife for various tasks.

Start by creating a virtual python environment::

    $ python -m venv .

You now can use this isolated clean python environment::

    $ bin/python --version
    Python 3.5.2

You may also activate it for the current shell.  POSIX shells would use::

    $ . bin/activate

running tests
-------------

We use `py.test`_ for running tests because it is amazing.  Run it by invoking
the simple *test* alias of *setup.py*::

    $ bin/python setup.py test

This will also check codestyle and test coverage.

.. _py.test: http://doc.pytest.org/en/latest/

checking code style
-------------------

We use `flake8`_ for enforcing coding standards.  Run it by invoking
the simple *lint* alias of *setup.py*::

    $ bin/python setup.py lint


.. _flake8: https://flake8.readthedocs.io/en/latest/

building source distirbutions
-----------------------------

Standard *sdist* is supported::

    $ bin/python setup.py sdist


building binary distributions
-----------------------------

Use the `wheel distribution standard`_::

    $ bin/python setup.py bdist_wheel

.. _wheel distribution standard: http://pythonwheels.com/


building html documentation
---------------------------

Use *setup.py* to build the documentation::

    $ bin/python setup.py docs

A `make`_ implementation is not required on any platform, thanks to the
:class:`setup.Documentation` class.

.. autoclass:: setup.Documentation

.. _make: https://www.gnu.org/software/make/
.. _Sphinx: http://www.sphinx-doc.org/

cleaning your workspace
-----------------------

We also included a custom command which you can invoke through *setup.py*::

    $ bin/python setup.py clean

The :class:`setup.Clean` command is set to clean the following file patterns:

.. autoclass:: setup.Clean

   .. autoattribute:: setup.Clean.default_patterns
