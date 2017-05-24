#!/usr/bin/python
# coding: utf8


from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os

import anytree
import six


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
        except NotADirectoryError:
            pass


def _is_dict(data):
    try:
        for _, _ in six.iteritems(data):
            return True
    except AttributeError:
        return False

