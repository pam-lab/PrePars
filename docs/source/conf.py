# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
_PATH_HERE = os.path.abspath(os.path.dirname(__file__))
_PATH_ROOT = os.path.realpath(os.path.join(_PATH_HERE, "..", ".."))
sys.path.insert(0, os.path.abspath(_PATH_ROOT))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Prepars'
copyright = '2022, Mahdi Akhi, Pouya Khani, Amir Pourmand'
author = 'Mahdi Akhi, Pouya Khani, Amir Pourmand'
release = '0.0.4'



# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
]

napoleon_google_docstring = False
napoleon_numpy_docstring = True

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']


