# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
from datetime import datetime

project = 'DBtective'
copyright = f'{datetime.now().year}, CrEagleOne'
author = 'CrEagleOne'
release = '1.0.0'

sys.path.insert(0, os.path.abspath("../src"))
sys.path.insert(1, os.path.abspath('..'))
sys.path.insert(2, os.path.abspath('../..'))

locale_dirs = ['_build/locale/']
gettext_compact = False
language = 'en'
supported_languages = ['en', 'fr']
html_output_encoding = 'utf-8'

autodoc_default_options = {
    "special-members": "__init__",
    "members": True,
    "undoc-members": False,  # Document functions without docstrings
    "imported-members": False,  # Document imported functions
}

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",  # Support Google & NumPy docstrings
    "sphinx.ext.viewcode",  # Adds a link to the source code
    'myst_parser'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']


def setup(app):
    app.add_css_file('style.css')
