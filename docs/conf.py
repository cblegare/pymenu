#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# pymenu documentation build configuration file
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys
import os

# If extensions (or modules to document with autodoc) are in another
# directory, add these directories to sys.path here. If the directory is
# relative to the documentation root, use os.path.abspath to make it
# absolute, like shown here.
#sys.path.insert(0, os.path.abspath('.'))

# Get the project root dir, which is the parent dir of this
cwd = os.getcwd()
project_root = os.path.dirname(cwd)

# Insert the project root dir as the first element in the PYTHONPATH.
# This lets us ensure that the source package is imported, and that its
# version is used.
sys.path.insert(0, project_root)

import setup as setup_script

project_metadata = setup_script.ProjectMetadata()

# -- General configuration ---------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = '1.4'


def require_sphinx(required_version):
    global needs_sphinx
    def string_to_version(vstring):
        return tuple(vstring.split("."))
    if string_to_version(needs_sphinx) < string_to_version(required_version):
        needs_sphinx = required_version

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['sphinx.ext.intersphinx',
              'sphinx.ext.autodoc',
              'sphinx.ext.viewcode',
              'sphinx.ext.napoleon',
              'sphinx.ext.todo']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['templates']

# The suffix of source filenames.
source_suffix = '.rst'


# The encoding of source files.
source_encoding = 'utf-8'


# Some warning to ignore.  This can help using the -W (warning to errors)
# option
require_sphinx('1.4')
suppress_warnings = [
    "image.nonlocal_uri"
]


# Mappings to external docs
intersphinx_mapping = {'python': ('https://docs.python.org/3.4',
                                  None),
                       'anytree': ('http://anytree.readthedocs.io/en/latest/',
                                   None),
                       'xdg': ('http://pyxdg.readthedocs.io/en/latest',
                               None)}

# We enable the nitpicky mode that will warn about all references where the
# target cannot be found.
# Some python built-ins can not be found (including 'type' and 'object').
# This is simply a bug in the Python docs themselves (see, for example,
# https://bugs.python.org/issue11975).
# Sphinx issues warning like
#   WARNING: py:class reference target not found: object
# To make the warning go away, we use nitpick_ignore option.
require_sphinx('1.1')
nitpicky = True
nitpick_ignore = [
    ('py:class', 'str'),
    ('py:class', 'type'),
    ('py:class', 'object'),
    ('py:class', 'list'),
    ('py:obj', 'list.append'),
    ('py:obj', 'list.count'),
    ('py:obj', 'list.extend'),
    ('py:obj', 'list.index'),
    ('py:obj', 'list.insert'),
    ('py:meth', 'list.pop'),
    ('py:obj', 'list.remove'),
    # Warning from type hinting (pep 484)
    ('py:obj', 'Callable'),
    ('py:obj', 'Iterable'),
    ('py:obj', 'Optional'),
    ('py:obj', 'list'),
    ('py:obj', 'dict'),
    ('py:obj', 'Any'),
    ('py:obj', 'str'),
    ('py:obj', 'int'),
    ('py:obj', 'bool'),
    ('py:obj', ''),
    # Specific warnings
    ('py:class', 'classmethod'),
    ('py:obj', 'distutils.version.LooseVersion'),
    ('py:obj', 'pkg_resources.parse_version'),
    ('py:class', 'setuptools.Command'),
    ('py:func', 'setuptools.setup'),
    ('py:class', 'subprocess.Popen'),
    ('py:class', 'exceptions.Exception'),

]


# The master toctree document.
master_doc = 'index'

# General information about the project.
project = project_metadata.name
copyright = u'2017, {!s}'.format(project_metadata.author)

# The version info for the project you're documenting, acts as replacement
# for |version| and |release|, also used in various other places throughout
# the built documents.
#
# The short X.Y version.
version = str(project_metadata.version)
# The full version, including alpha/beta/rc tags.
#release = version

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to
# some non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['*.py', 'Makefile']

# The reST default role (used for this markup: `text`) to use for all
# documents.
#default_role = None

# This value selects what content will be inserted into the main body of an
# autoclass directive. The possible values are:
#   "class"
#       Only the class’ docstring is inserted. This is the default. You can
#       still document __init__ as a separate method using automethod or the
#       members option to autoclass.
#   "both"
#       Both the class’ and the __init__ method’s docstring are concatenated
#       and inserted.
#   "init"
#       Only the __init__ method’s docstring is inserted.
# If the class has no __init__ method or if the __init__ method’s docstring is
# empty, but the class has a __new__ method’s docstring, it is used instead.
autoclass_content = 'both'

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built
# documents.
#keep_warnings = False


# -- Options for HTML output -------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
import sphinx_rtd_theme
html_theme = 'sphinx_rtd_theme'


# Theme options are theme-specific and customize the look and feel of a
# theme further.  For a list of options available for each theme, see the
# documentation.
#html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as
# html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the
# top of the sidebar.
#html_logo = None

# The name of an image file (within the static path) to use as favicon
# of the docs.  This file should be a Windows icon file (.ico) being
# 16x16 or 32x32 pixels large.
#html_favicon = None

# Add any paths that contain custom static files (such as style sheets)
# here, relative to this directory. They are copied after the builtin
# static files, so a file named "default.css" will overwrite the builtin
# "default.css".
html_static_path = ['_static']

# If not '', a 'Last updated on:' timestamp is inserted at every page
# bottom, using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names
# to template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer.
# Default is True.
#html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer.
# Default is True.
#html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages
# will contain a <link> tag referring to it.  The value of this option
# must be the base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = 'pymenudoc'


# -- Options for LaTeX output ------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #'preamble': '',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass
# [howto/manual]).
latex_documents = [
    ('index', 'pymenu.tex',
     u'pymenu Documentation',
     u'Charles Bouchard-Légaré', 'manual'),
]

# The name of an image file (relative to this directory) to place at
# the top of the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings
# are parts, not chapters.
#latex_use_parts = False

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_domain_indices = True


# -- Options for manual page output ------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'pymenu',
     u'pymenu Documentation',
     [u'Charles Bouchard-Légaré'], 1)
]

# If true, show URL addresses after external links.
#man_show_urls = False


# -- Options for Texinfo output ----------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    ('index', 'pymenu',
     u'pymenu Documentation',
     u'Charles Bouchard-Légaré',
     'pymenu',
     'One line description of project.',
     'Miscellaneous'),
]

# Documents to append as an appendix to all manuals.
#texinfo_appendices = []

# If false, no module index is generated.
#texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
#texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
#texinfo_no_detailmenu = False
