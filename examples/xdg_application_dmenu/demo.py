#!/usr/bin/python

from pymenu import Menu
from pymenu.ext.xdmenu import DmenuPrompt
from pymenu.ext.xdg import make_xdg_menu_entry, launch_xdg_menu_entry

menu_entry = make_xdg_menu_entry()
prompt = DmenuPrompt()

my_menu = Menu(menu_entry, prompt)

choice = my_menu.choose_value()
launch_xdg_menu_entry(choice)
