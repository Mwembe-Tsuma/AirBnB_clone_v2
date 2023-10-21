#!/usr/bin/python3
"""This module starts a flask application."""

from flask import Flask
# from web_flask import app

app = Flask(__name__,)


@app.route('/', strict_slashes=False)
def index():
    """Display 'Hello HBNB!'"""
    return 'Hello HBNB!'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
