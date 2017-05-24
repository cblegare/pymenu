#!/usr/bin/python
# coding: utf8


from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import readline  # Used by 'input'

from six.moves import input


class Prompt(object):
    """
    Abstract class for defining menu user interfaces.
    """

    def prompt_for_one(self, menu):
        """

        Args:
            menu (list): List from which to choose from.

        Returns:
            str
        """
        raise NotImplementedError


class SimpleCommandLineMenu(Prompt):
    def __init__(self, question=None, prompt=None):
        """
        Simply prompt a user for choices in command line.

        Args:
            question (str): Header question displayed before the choices.
            prompt (str): Actual prompt message for the user.
        """
        self._question = question or 'Please select one of the following'
        self._prompt = prompt or 'Your choice: '

    def prompt_for_one(self, menu):
        """
        Args:
            menu (list): List from which to choose from.

        Returns:
            str: Chosen key

        Raises:
            KeyError: when the select item in not a valid choice.
        """
        choices = menu
        if menu.entry.parent:
            choices.append('..')
        for entry in menu.entry.children:
            choices.append(entry.name)

        while True:
            print(self._question)
            for key in choices:
                print(key)
            choice = input(self._prompt)
            if choice in choices:
                return choice
