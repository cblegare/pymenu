#!/usr/bin/python
# coding: utf8


from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from collections import OrderedDict


class Menu(object):
    def __init__(self, root_entry, prompt):
        """

        Args:
            root_entry (pymenu.MenuEntry):
            prompt (pymenu.Prompt):
        """
        self._root = root_entry
        self._prompt = prompt

    @property
    def entry(self):
        """
        Returns:
            pymenu.MenuEntry
        """
        return self._root

    def choose_value(self):
        """
        Prompt until a leaf menu item is choosen.

        Returns:
            Any: The associated value for the chosen item.
        """
        current_menu = self
        while not current_menu.entry.is_leaf:
            current_menu = current_menu.choose_menu()
        return current_menu.entry.value

    def choose_menu(self):
        """
        Prompt for a choice of menu items.

        Returns:
            pymenu.Menu: The chosen menu object
        """
        choices = OrderedDict()
        if self.entry.parent:
            choices['..'] = self.entry.parent
        for entry in self.entry.children:
            choices[entry.name] = entry

        chosen_ley = self._prompt.prompt_for_one(choices.keys())
        return self.__class__(choices[chosen_ley], self._prompt)
