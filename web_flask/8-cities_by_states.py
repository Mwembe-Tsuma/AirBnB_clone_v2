#!/usr/bin/python3
"""This module starts a flask web app, """

from web_flask import app
from flask import render_template
from models import storage
from models.state import State
from models.city import City


@app.teardown_appcontext
def teardown(exception):
    """Remove current SQLAlchemy Session."""
    storage.close()
    if exception:
        print(exception)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """Diplay a list of states."""
    all_states = storage.all(State)
    return render_template(
            '7-states_list.html',
            all_states=all_states,
            )


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """Display states and their cities."""
    all_states = storage.all(State)
    all_cities = storage.all(City)
    return render_template(
            '8-cities_by_states.html',
            all_states=all_states,
            all_cities=all_cities,
            )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
