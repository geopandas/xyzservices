# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import shutil
import sys
from pathlib import Path
sys.path.insert(0, os.path.abspath("../.."))
import xyzservices  # noqa

# -- Project information -----------------------------------------------------

project = "xyzservices"
copyright = "2021, Martin Fleischmann, Dani Arribas-Bel"
author = "Martin Fleischmann, Dani Arribas-Bel"

version = xyzservices.__version__
# The full version, including alpha/beta/rc tags
release = version

html_title = f'xyzservices <span id="release">{release}</span>'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "numpydoc",
    "sphinx.ext.autosummary",
    "myst_nb",
    "sphinx_copybutton",
]

jupyter_execute_notebooks = "force"
autosummary_generate = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "furo"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_css_files = [
    "custom.css",
]
# html_sidebars = {
#     "**": ["docs-sidebar.html"],
# }
# html_logo = "_static/logo.svg"

p = Path().absolute()
shutil.copy(p.parents[1] / "xyzservices" / "data" / "providers.json", p / "_static")
