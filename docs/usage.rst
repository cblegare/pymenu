=====
Usage
=====

The simplest possible usage of this wrapper is through the :func:`xdmenu.dmenu`
function.

.. autofunction:: xdmenu.dmenu
    :noindex:

The :mod:`xdmenu` package also provides the :class:`xdmenu.Dmenu` class.  This
class can be provided with default configuration values to customize the
behavior of `dmenu`.

.. autoclass:: xdmenu.Dmenu
    :noindex:

Run `dmenu` using :meth:`xdmenu.Dmenu.run`.

.. automethod:: xdmenu.Dmenu.run
    :noindex:

If you only want to get the command line arguments, simply use
:meth:`xdmenu.Dmenu.make_cmd`

.. automethod:: xdmenu.Dmenu.make_cmd
    :noindex:

Since `xdmenu` is intended to be extensible, you can add supported options
using :meth:`xdmenu.Dmenu.add_arg`

.. automethod:: xdmenu.Dmenu.add_arg
    :noindex:


