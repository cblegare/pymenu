#!/usr/bin/python
# coding: utf8


from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import subprocess

import xdg.Menu
import tatsu

from pymenu import Launcher
from pymenu.menu.entry import MenuEntry


class XdgLauncher(Launcher):
    def __init__(self, menu_def, ui_chooser):
        """
        An application launcher matching a XDG menu specification.

        Args:
            menu_def (str): Path to a `.menu` file as defined in the `Desktop
                Menu Specification`_

                .. _`Desktop Menu Specification`: https://specifications.freedesktop.org/menu-spec/menu-spec-1.0.html
            ui_chooser (Callable): See :class:`pymenu.MenuEntry`.

        See Also:
            :class:`pymenu.menu.MenuEntry`
        """
        xdg_base_menu = xdg.Menu.parse(str(menu_def))
        xdg_menu = XdgMenuEntry(xdg_base_menu, ui_chooser)
        super(XdgLauncher, self).__init__(xdg_menu, launch_xdg_menu_entry)


class XdgMenuEntry(MenuEntry):
    def __init__(self, wrapped_entry, ui_chooser, parent=None):
        """
        Wrap an XDG menu entry.

        Args:
            wrapped_entry (xdg.Menu.Menu):
            ui_chooser (Callable[[dict], Any]): See
                :class:`pymenu.MenuEntry`
            parent:

        See Also:
            :class:`xdg.Menu.Menu`
        """
        if isinstance(wrapped_entry, xdg.Menu.Menu):
            key = wrapped_entry.getName()
        else:
            key = wrapped_entry.DesktopEntry.getName()

        super(XdgMenuEntry, self).__init__(key,
                                           ui_chooser,
                                           value=wrapped_entry,
                                           parent=parent)

        if isinstance(wrapped_entry, xdg.Menu.Menu):
            for child in wrapped_entry.getEntries():
                XdgMenuEntry(child, ui_chooser, self)


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
    desktop_app.launch(targets)


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

                .. _`Debian Alternatives System`: https://wiki.debian.org/DebianAlternatives
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
            if arg in ['%f', '%u'] and target:
                cmd.append(target)
            elif arg in ['%F', '%U'] and target:
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

        if 1 < sum(arg
                   for arg in unmapped_args
                   if arg in ['%f', '%F', '%u', '%U']):
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
