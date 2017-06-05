
|build_badge| |pypi_badge| |rtfd_badge| |cov_badge| |lic_badge|

.. |rtfd_badge| image:: https://readthedocs.org/projects/pymenu/badge/?version=latest
    :target: https://pymenu.readthedocs.io/en/latest/?badge=latest
    :alt: Latest Documentation

.. |lic_badge| image:: https://img.shields.io/badge/License-LGPL%20v3-blue.svg
    :target: http://www.gnu.org/licenses/lgpl-3.0
    :alt: GNU Lesser General Public License v3

.. |build_badge| image:: https://img.shields.io/travis/cblegare/pymenu.svg
    :target: https://travis-ci.org/cblegare/pymenu
    :alt: Build Status

.. |pypi_badge| image:: https://img.shields.io/pypi/v/pymenu.svg
    :target: https://pypi.python.org/pypi/pymenu`
    :alt: Released on PyPI

.. |py3_badge| image:: https://pyup.io/repos/github/cblegare/pymenu/python-3-shield.svg
    :target: https://pyup.io/repos/github/cblegare/pymenu/
    :alt: Python 3 ready

.. |cov_badge| image:: https://codecov.io/gh/cblegare/pymenu/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/cblegare/pymenu
    :alt: Coverage Report


An API for menu definitions.

.. warning:: Before 1.0 release, this project will not follow any reliable
    versioning scheme.  Do not expect backward-compatibility between versions!

.. warning:: This project is not stable at all!  Parts of it might be moved to
    external packages without notice.

This project was intented to be used with the `extensible dmenu wrapper`_ as a
menu API for Qtile_.

`pymenu` is free software and licensed under the GNU Lesser General Public
License v3.


Features
--------

* Simple python interfaces for menus
* Easy to configure using simple dictionaries and the filesystem
* Extension available for XDG-based menus (including launching applications
  defined in `desktop` files).


Credits
---------

This package was created with Cookiecutter_ and the `cblegare/pythontemplate`_
project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cblegare/pythontemplate`: https://github.com/cblegare/pythontemplate
.. _`extensible dmenu wrapper`: https://github.com/cblegare/xdmenu
.. _Qtile: http://www.qtile.org
