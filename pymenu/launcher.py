#!/usr/bin/python
# coding: utf8


from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


class Launcher(object):
    def __init__(self, menu, action):
        """

        Args:
            menu (pymenu.MenuEntry):
            action:
        """
        self._menu = menu
        self._action = action

    def launch(self):
        chosen = self._menu.choose()
        return self._action(chosen)
