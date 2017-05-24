#!/usr/bin/python3.5
# coding: utf8


"""Package main definition."""


from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from pkg_resources import get_distribution, DistributionNotFound
import sys

__project__ = 'xdmenu'
__version__ = None  # required for initial installation

try:
    distribution = get_distribution(__project__)
    __version__ = distribution.version

except DistributionNotFound:
    # This will happen if the package is not installed.
    # For more informations about development installation, read about
    # the 'develop' setup.py command or the '--editable' pip option.
    # Note that development installations may break other packages from
    # the same implicit namespace
    # (see https://github.com/pypa/packaging-problems/issues/12)
    __version__ = '(local)'
else:
    pass


from pymenu.menu import Menu
from pymenu.menu.entry import MenuEntry, DictMenuEntry, FileSystemMenuEntry
from pymenu.menu.prompt import Prompt, SimpleCommandLineMenu
from pymenu.launcher import Launcher

__all__ = ['Menu',
           'MenuEntry',
           'DictMenuEntry',
           'FileSystemMenuEntry',
           'Prompt',
           'SimpleCommandLineMenu',
           'Launcher']

try:
    from pymenu.ext.xdg import XdgMenuEntry, XdgLauncher, Application
    __all__.extend(['XdgMenuEntry',
                    'XdgLauncher',
                    'Application'])
except ImportError:
    # pyxdg is not installed
    pass
