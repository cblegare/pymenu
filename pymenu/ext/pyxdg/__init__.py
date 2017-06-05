#!/usr/bin/python
# coding: utf8


from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import subprocess

import xdg.Menu
import tatsu

from pymenu import MenuEntry


class XdgMenuEntry(MenuEntry):
    def __init__(self, wrapped_entry, parent=None):
        """
        Wrap an XDG menu entry.

        Args:
            wrapped_entry (xdg.Menu.Menu):
            parent:

        See Also:
            :class:`xdg.Menu.Menu`
        """
        if isinstance(wrapped_entry, xdg.Menu.Menu):
            key = wrapped_entry.getName()
        elif isinstance(wrapped_entry, xdg.Menu.MenuEntry):
            key = wrapped_entry.DesktopEntry.getName()
        super(XdgMenuEntry, self).__init__(key,
                                           value=wrapped_entry,
                                           parent=parent)

        if isinstance(wrapped_entry, xdg.Menu.Menu):
            for child in _menulike_children(wrapped_entry):
                XdgMenuEntry(child, self)

    @classmethod
    def from_xdg_menu_file(cls, menu_def_file):
        """
        Constructor for a `.menu` file.

        See Also:
            :func:`pymenu.ext.xdg.make_xdg_menu_entry`
        """
        return make_xdg_menu_entry(menu_def_file, cls=cls)


def _menulike_children(menu):
    children = menu.getEntries()
    for child in children:
        if isinstance(child, (xdg.Menu.Menu, xdg.Menu.MenuEntry)):
            yield child


def make_xdg_menu_entry(menu_def_file=None, cls=None):
    """
    Make a :class:`pymenu.MenuEntry` based on a XDG .menu file.

    This is usually located in ``/etc/xdg/menus/applications.menu``.

    Args:
        menu_def_file (str): Path to a `.menu` file as defined in the `Desktop
            Menu Specification`_. Defaults to
            ``/etc/xdg/menus/applications.menu``

            This file can usually be found in the ``/etc/xdg/menus`` folder.
            The following command is a good start to list these .menu files:

            .. code-block: text

                find /etc/xdg/menus -name *applications.menu

            These `.menu` file may not include applications that installed
            their desktop entries in a user folder such as
            ``~/.local/share/applications``.  In order to add additional
            directories to the desktop entries search path, you need to add
            a ``<AppDir>`` tag to the `.menu` file for the relevant directory.

            .. _`Desktop Menu Specification`: https://specifications.freedesktop.org/menu-spec/menu-spec-1.0.html  # noqa: E501
        cls (type): The subclass of :class:`pymenu.MenuEntry` to create.  The
            default is :class:`pymenu.ext.xdg.XdgMenuEntry`.

    See Also:
        :class:`pymenu.menu.MenuEntry`
    """
    menu_def_file = menu_def_file or '/etc/xdg/menus/applications.menu'
    cls = cls or XdgMenuEntry
    xdg_base_menu = xdg.Menu.parse(str(menu_def_file))
    menu_entry = cls(xdg_base_menu)
    return menu_entry


def launch_xdg_menu_entry(entry, *targets):
    """
    A convenient launcher for desktop entries.

    This uses the :class:`~Application` with default values.

    Args:
        entry (xdg.Menu.MenuEntry):

    Returns:
        None
    """
    desktop_app = Application(entry)
    desktop_app.launch(*targets)


class Application(object):
    def __init__(self, entry, parser=None, term_args=None):
        """
        A launchable application defined by a XDG desktop entry.

        Args:
            entry (xdg.Menu.MenuEntry): The desktop entry for this application.
            parser (Callable): A function that parses an Exec string of a
                desktop entry and returns an abstract syntax tree (AST) of it.
                The AST is expected to be made of lists and have the following
                structure (given the input ``app arg1 arg2``)::

                    [
                        ['a', 'p', 'p'],
                        [
                            ['a', 'r', 'g', '1'],
                            ['a', 'r', 'g', '2']
                        ]
                    ]

                The default parser should work in most cases.

            term_args (list): Command line argument prefixes for terminal
                applications.  In XDG compliant desktop environments, the
                default (``['x-terminal-emulator', '-e']``) should be enough
                since it work on any setup that implements the `Debian
                Alternatives System`_ which is common in many UNIX
                distributions and most popular desktop environments.

                If you do not use this from of a XDG compliant environment (in
                Qtile_, for instance) you will need to set this manually.

                .. _`Debian Alternatives System`: https://wiki.debian.org/DebianAlternatives  # noqa: E501
                .. _Qtile: http://www.qtile.org
        """
        self._entry = entry.DesktopEntry  # type: xdg.DesktopEntry.DesktopEntry
        self._parse = parser or exec_parser
        self._executable_cache = None
        self._arguments_cache = None
        self._terminal = term_args or ['x-terminal-emulator', '-e']

    def launch(self, *target_uris, **popen_kwargs):
        """
        Launch this application with provided targets.

        Args:
            *target_uris: Positional arguments are used as URI targets for this
                application.  If this application can handle multiple URIs at
                once, they are all parametrized in one subprocess.  If this
                application can only handle one URI at a time, multiple
                processes are launched.  If this application cannot handle
                target URIs, this argument is ignored.
            **popen_kwargs: This application is launched as subprocesses using
                :class:`subprocess.Popen`.  These keyword arguments are simply
                passed along to this subprocess constructor.

        Returns:
            list: All subprocesses launched.
        """
        cmds = []

        if '%F' in self.arguments or '%U' in self.arguments:
            cmds.append(self._make_cmd(target_uris))
        else:
            for target in target_uris:
                cmds.append(self._make_cmd(target))

        processes = []
        for cmd in cmds:
            processes.append(subprocess.Popen(cmd, **popen_kwargs))
        return processes

    @property
    def executable(self):
        """
        Provide the command line executables part for this application.

        This may include terminal-specific executables and arguments, such as
        ``['x-terminal-emulator', '-e']`` in addition to the actual executable
        if this is a terminal application.

        Returns:
            list
        """
        if self._executable_cache is None:
            self._parse_exec()
        return self._executable_cache

    @property
    def arguments(self):
        """
        Provide the command line arguments for this application.

        Some (``%i``, ``%c``, ``%k``) fieldcode placeholders are replaced.
        Target-like fieldcodes placeholders like ``%f``, ``%F``, ``%u`` and
        ``%U`` are not replaced.

        Returns:
            list
        """
        if self._arguments_cache is None:
            self._parse_exec()
        return self._arguments_cache

    @property
    def _icon_args(self):
        icon_key = self._entry.getIcon()
        if icon_key:
            return ['--icon', icon_key]
        return []

    @property
    def _name_args(self):
        name_key = self._entry.getName()
        if name_key:
            return [name_key]
        return []

    @property
    def _desktopfile_args(self):
        return [self._entry.filename]

    def _make_cmd(self, target=None):
        """
        Args:
            target: One or many URI targets

        Returns:
            list
        """
        cmd = self.executable[:]
        for arg in self.arguments:
            if arg in ['%f', '%u']:
                if target:
                    cmd.append(target)
            elif arg in ['%F', '%U']:
                if target:
                    cmd.extend(target)
            else:
                cmd.append(arg)
        return cmd

    def _parse_exec(self):
        exec_string = self._entry.getExec()
        exec_ast = self._parse(exec_string)
        executable_ast, arguments_ast = exec_ast
        executable_path = ''.join(executable_ast)
        self._executable_cache = []
        if self._entry.getTerminal():
            self._executable_cache.extend(self._terminal)
        self._executable_cache.append(executable_path)

        self._arguments_cache = []
        unmapped_args = [''.join(argument_ast)
                         for argument_ast in arguments_ast]

        if 1 < len([arg
                   for arg in unmapped_args
                   if arg in ['%f', '%F', '%u', '%U']]):
            raise Exception('Malformed Exec entry.')

        for arg in unmapped_args:
            if arg == '%i':
                self._arguments_cache.extend(self._icon_args)
            elif arg == '%c':
                self._arguments_cache.extend(self._name_args)
            elif arg == '%k':
                self._arguments_cache.extend(self._desktopfile_args)
            else:
                self._arguments_cache.append(arg)


EXEC_GRAMMAR = r"""
@@grammar::Exec

command = executable arguments;

executable
    =
    wordexpression
    ;

arguments
    =
    {argument}*
    ;

argument
    =
    | wordexpression
    | @+:fieldcode
    ;

wordexpression
    =
    | @:chars
    | quote @:reservedchars quote
    ;

fieldcode
    =
    | /%[fFuUdDnNickvm]/
    | quote @:/%[fFuUdDnNickvm]/ quote
    ;

quote
    =
    /(?<!\\)"/
    ;

chars
    =
    {CHAR}+
    ;

reservedchars
    =
    {CHAR|RESERVERDCHAR|QUOTEDCHAR}+
    ;

CHAR
    =
    /[a-zA-Z_0-9\-]/
    ;

QUOTEDCHAR
    =
    '\'@:/[\\\$\`\"]/
    ;

RESERVERDCHAR
    =
    /[\ \t\n\'\>\<\~\|\&\;\*\?\#\(\)]/
    ;
"""


_exec_parser = tatsu.compile(EXEC_GRAMMAR)


def exec_parser(exec_string):
    """
    Examples:
        >>> exec_parser(r'vim')
        [['v', 'i', 'm'], []]
        >>> exec_parser(r'"vim"')
        [['v', 'i', 'm'], []]
        >>> exec_parser(r'vim arg1 arg2')
        [['v', 'i', 'm'], [['a', 'r', 'g', '1'], ['a', 'r', 'g', '2']]]
        >>> exec_parser(r'vim "arg"')
        [['v', 'i', 'm'], [['a', 'r', 'g']]]
        >>> exec_parser(r'"vim arg"')
        [['v', 'i', 'm', ' ', 'a', 'r', 'g'], []]
        >>> exec_parser(r'"vim arg" "x y"')
        [['v', 'i', 'm', ' ', 'a', 'r', 'g'], [['x', ' ', 'y']]]
        >>> exec_parser(r'vim %u')
        [['v', 'i', 'm'], [['%u']]]
        >>> exec_parser(r'vim "%u"')
        [['v', 'i', 'm'], [['%u']]]
        >>> exec_parser(r'vim "%u" foo %F')
        [['v', 'i', 'm'], [['%u'], ['f', 'o', 'o'], ['%F']]]
        >>> exec_parser(r'vim "\$foo"')
        [['v', 'i', 'm'], [['$', 'f', 'o', 'o']]]
    """

    # other test should include
    # but doctests breaks with such mad escape sequences mangling
    # >>> make_cmd_from_exec(r'"a a" b "c \" 3"')
    # [['a', ' ', 'a'], [['b'], ['c', ' ', '"', ' ', '3']]]
    # >>> make_cmd_from_exec(r'"a \\\\ \$f\`"')
    # [['a', ' ', '\\', '\\', ' ', '$', 'f', '`'], []]
    return _exec_parser.parse(exec_string)


if __name__ == '__main__':
    import doctest
    flags = doctest.IGNORE_EXCEPTION_DETAIL | doctest.ELLIPSIS
    doctest.testmod(optionflags=flags)
