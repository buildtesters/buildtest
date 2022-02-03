# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import shutil
import sys

here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, here)
from buildtest import BUILDTEST_COPYRIGHT, BUILDTEST_VERSION
from buildtest.cli.buildspec import BuildspecCache
from buildtest.config import SiteConfiguration
from buildtest.defaults import BUILDTEST_ROOT, VAR_DIR
from buildtest.utils.file import is_dir

# set BUILDTEST_ROOT environment that is generally set by 'source setup.sh'
os.environ["BUILDTEST_ROOT"] = here
# add $BUILDTEST_ROOT/bin to $PATH to reference 'buildtest' command in docs
os.environ["PATH"] += "%s%s" % (os.pathsep, os.path.join(here, "bin"))

# remove $BUILDTEST_ROOT/var which writes variable data
if is_dir(VAR_DIR):
    shutil.rmtree(VAR_DIR)


configuration = SiteConfiguration()
configuration.detect_system()
configuration.validate()
# need to create buildspec cache

cache = BuildspecCache(
    rebuild=True,
    configuration=configuration,
)

# -- Project information -----------------------------------------------------
project = "buildtest"
copyright = BUILDTEST_COPYRIGHT

author = "Shahzeb Siddiqui, Vanessa Sochat"

# The short X.Y version
version = BUILDTEST_VERSION
# The full version, including alpha/beta/rc tags
release = BUILDTEST_VERSION


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Sphinx extensions
extensions = [
    "autoapi.extension",
    "sphinxarg.ext",
    "sphinxcontrib.programoutput",
    "sphinxext.remoteliteralinclude",
    "sphinx_rtd_theme",
    "sphinx_tabs.tabs",
    # "sphinx.ext.autosectionlabel",
    "sphinx.ext.coverage",
    "sphinx.ext.imgmath",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
]

# Sphinx AutoApi configuration see https://sphinx-autoapi.readthedocs.io/en/latest/
autoapi_type = "python"
autoapi_dirs = [os.path.join(BUILDTEST_ROOT, "buildtest")]
autoapi_add_toctree_entry = True
autoapi_member_order = "bysource"
autoapi_root = "api"
autoapi_python_class_content = "both"
autoapi_template_dir = "_templates/autoapi"

# sphinx napoleon setting see https://sphinxcontrib-napoleon.readthedocs.io/en/latest/sphinxcontrib.napoleon.html#module-sphinxcontrib.napoleon
napoleon_include_init_with_doc = False

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

suppress_warnings = ["autoapi"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# configuration for sphinx-copybutton see https://sphinx-copybutton.readthedocs.io/en/latest/
copybutton_prompt_text = r">>> |\.\.\. |\$ "
copybutton_prompt_is_regexp = True

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = None


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

html_logo = f"{BUILDTEST_ROOT}/logos/BuildTest_Primary_Center_4x3.png"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    "prev_next_buttons_location": "both",
    "sticky_navigation": True,
    "style_external_links": True,
    "logo_only": True,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_context = {
    # "display_github": True,  # Integrate GitHub
    # "github_user": "shahzebmsiddiqui",  # Username
    # "github_repo": "buildtest",  # Repo name
    # "github_version": "master",  # Version
    # "css_files": ["_static/theme_overrides.css"]  # override wide tables in RTD theme
}

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "buildtestdoc"


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (
        master_doc,
        "buildtest.tex",
        "buildtest Documentation",
        "Shahzeb Siddiqui",
        "manual",
    )
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, "buildtest", "buildtest Documentation", [author], 1)]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "buildtest",
        "buildtest Documentation",
        author,
        "buildtest",
        "One line description of project.",
        "Miscellaneous",
    )
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ["search.html"]
