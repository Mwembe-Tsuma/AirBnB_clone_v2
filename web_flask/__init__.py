#!/usr/bin/python3
"""This module creates a flask app."""

from flask import Flask

app = Flask(
        __name__,
        template_folder='./templates',
        )
