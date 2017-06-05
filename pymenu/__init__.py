#!/usr/bin/python3.5
# coding: utf8


"""Package main definition."""


from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
from collections import OrderedDict
import errno

import anytree
import six

from pkg_resources import get_distribution, DistributionNotFound

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


class MenuEntry(anytree.Node):
    def __init__(self, name, value=None, parent=None):
        """
        A menu tree node.

        This is essentially a tree node, as inherited by
        :class:`anytree.node.Node`. Sub classes may require to implement the
        creation of child entries.

        Args:
            name (str): A name for this node.
            value (Any): Associated value.
            parent (pymenu.MenuEntry): Parent entry node.
        """
        super(MenuEntry, self).__init__(name,
                                        parent=parent)
        self._value = value

    @property
    def value(self):
        return self._value


class Prompt(object):
    """
    Abstract class for defining menu user interfaces.
    """

    def prompt_for_one(self, choices):
        """

        Args:
            choices (list): List from which to choose from.

        Returns:
            str
        """
        raise NotImplementedError


class DictMenuEntry(MenuEntry):
    def __init__(self, name, data, parent=None):
        """
        A menu tree node made of a dictionary structure.

        Args:
            name (str): The name of this node.
            data (dict): The value of this node.  If this is a dictionary,
                child nodes will be created from it.
            parent (pymenu.MenuEntry): Parent entry node.
        """
        menuvalue = data if not _is_dict(data) else None

        super(DictMenuEntry, self).__init__(name,
                                            value=menuvalue,
                                            parent=parent)

        try:
            for key, value in six.iteritems(data):
                DictMenuEntry(key, value, self)
        except AttributeError:
            # data is not a dictionnary
            pass


class FileSystemMenuEntry(MenuEntry):
    def __init__(self, path, parent=None):
        """
        A menu tree node made from a filesystem path.

        Args:
            path (str): Filesystem path from which to build the menu tree.
            parent (pymenu.MenuEntry): Paren entry node.

        Note:
            The creation of child nodes if **not lazy**. This means that
            creating an instance of this class from a top level folder of a
            large file sets will consumes a lot of RAM.
        """
        path = str(path)
        super(FileSystemMenuEntry, self).__init__(path,
                                                  value=path,
                                                  parent=parent)
        try:
            for sub in os.listdir(path):
                self.__class__(os.path.join(path, sub), self)
        except OSError as e:
            if e.errno != errno.ENOTDIR:
                raise e


class SimpleCommandPrompt(Prompt):
    def __init__(self, question=None, prompt=None):
        """
        Simply prompt a user for choices in command line.

        Args:
            question (str): Header question displayed before the choices.
            prompt (str): Actual prompt message for the user.
        """
        self._question = question or 'Please select one of the following'
        self._prompt = prompt or 'Your choice: '

    def prompt_for_one(self, choices):
        """
        Args:
            choices (list): List from which to choose from.

        Returns:
            str: Chosen key

        Raises:
            KeyError: when the select item in not a valid choice.
        """
        enumeration = OrderedDict()
        for k, v in enumerate(choices):
            enumeration[str(k)] = v

        print(self._question)
        for num, path in six.iteritems(enumeration):
            print('{:>4} {!s}'.format(num, path))
        choice = input(self._prompt)
        return enumeration[choice]


def _is_dict(data):
    try:
        for _, _ in six.iteritems(data):
            return True
    except AttributeError:
        return False
