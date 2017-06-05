#!/usr/bin/python

from pymenu import Menu, FileSystemMenuEntry, SimpleCommandPrompt

menu_entry = FileSystemMenuEntry('.')
prompt = SimpleCommandPrompt()

my_menu = Menu(menu_entry, prompt)

choice = my_menu.choose_value()
print(choice)
