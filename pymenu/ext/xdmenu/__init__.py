#!/usr/bin/python
# coding: utf8


from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import xdmenu

from pymenu import Prompt


class DmenuPrompt(Prompt):
    def __init__(self, dmenu=None):
        """

        Args:
            dmenu (xdmenu.BaseMenu):
        """
        self._dmenu = dmenu or xdmenu.Dmenu()

    def prompt_for_one(self, menu):
        """

        Args:
            menu (list): List from which to choose from.

        Returns:
            str
        """
        results = self._dmenu.run(menu)

        try:
            choice = results[0]
        except IndexError:
            choice = None

        return choice

