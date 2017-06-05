#!/usr/bin/python

from pymenu import Menu, FileSystemMenuEntry
from pymenu.ext.xdmenu import DmenuPrompt

menu_entry = FileSystemMenuEntry('.')
prompt = DmenuPrompt()

my_menu = Menu(menu_entry, prompt)

choice = my_menu.choose_value()
print(choice)
