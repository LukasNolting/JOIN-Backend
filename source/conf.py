# Configuration file for the Sphinx documentation builder.
import os
import sys
import django

# Pfad überprüfen und setzen
django_project_path = os.path.abspath('../../Join_Backend')
print(f"Django Project Path: {django_project_path}")  # Debugging-Ausgabe
sys.path.insert(0, django_project_path)

# Setzen Sie das Django-Settings-Modul
os.environ['DJANGO_SETTINGS_MODULE'] = 'joinbackend.settings'

# Django-Konfiguration laden
django.setup()

project = 'join'
copyright = '2024, Lukas'
author = 'Lukas'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon',]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
