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

sys.path.insert(0, os.path.abspath('..'))

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
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']
