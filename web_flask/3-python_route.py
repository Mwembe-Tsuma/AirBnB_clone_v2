#!/usr/bin/python3
"""This module starts a flask application with 4 routes."""

from flask import Flask
# from web_flask import app

app = Flask(__name__,)


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


@app.route('/python/<text>', strict_slashes=False)
@app.route('/python', strict_slashes=False)
def python_route(text='is cool'):
    """Display 'Python and value of text."""
    return f"Python {text.replace('_', ' ')}"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
