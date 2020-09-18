"""This file provides method to access buildtest and schema docs when
requested from command line.
"""

import webbrowser


def buildtestdocs(args=None):
    print(args)
    """Open buildtest docs in web browser. This implements ``buildtest docs``"""
    webbrowser.open("https://buildtest.readthedocs.io/")


def schemadocs(args=None):
    """Open buildtest schema docs in web browser. This implements ``buildtest schemadocs``"""
    webbrowser.open("https://buildtesters.github.io/schemas/")
