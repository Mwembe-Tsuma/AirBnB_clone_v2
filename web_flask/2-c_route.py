#!/usr/bin/python3
"""This module starts a flask application with 3 routes."""

from web_flask import app


@app.route('/', strict_slashes=False)
def index():
    """Display 'Hello HBNB!'"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Display 'HBNB'."""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_route(text):
    """Display 'C' and value of 'text' underscore replaced with space"""
    return f"C {text.replace('_', ' ')}"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
