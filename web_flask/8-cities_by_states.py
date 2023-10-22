#!/usr/bin/python3
""" flask module for states"""
from models import storage
from os import getenv
from flask import Flask, render_template
from models.state import State


app = Flask(__name__)


@app.route("/cities_by_states", strict_slashes=False)
def cities_by_states():
    all_state = storage.all(State)
    states = sorted(all_state.values(), key=lambda state: state.name)
    storage_type = getenv("HBNB_TYPE_STORAGE")
    return render_template("8-cities_by_states.html", states=states,
                           storage_type=storage_type)


@app.teardown_appcontext
def close(exception):
    storage.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
