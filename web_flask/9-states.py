#!/usr/bin/python3
"""This module starts a flask web app, """

from web_flask import app
from flask import render_template, request
from models import storage
from models.state import State
from models.city import City


@app.teardown_appcontext
def teardown(exception):
    """Remove current SQLAlchemy Session."""
    storage.close()
    if exception:
        print(exception)


@app.route('/states', strict_slashes=False)
@app.route('/states_list', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states_list(id=None):
    """Diplay a list of states."""
    all_states = storage.all(State)
    all_cities = None
    if id:
        all_states = {
                i: all_states[i] for i in all_states
                if all_states[i].id == id}
        all_cities = storage.all(City)
        all_cities = {
                i: all_cities[i] for i in all_cities
                if all_cities[i].state_id == id
                and list(all_states.values())[0].id == id
        }
    template = '9-states.html'
    if request.path == '/states_list':
        template = '7-states_list.html'
    return render_template(
            template,
            all_states=all_states,
            all_cities=all_cities,
            )


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """Display all states with their corresponding cities."""
    all_states = storage.all(State)
    all_cities = storage.all(City)
    return render_template(
            '8-cities_by_states.html',
            all_states=all_states,
            all_cities=all_cities,
            )


@app.route('/states/<id>', strict_slashes=False)
def states_by_id(id):
    """Display all states with their corresponding cities."""
    all_states = storage.all(State)
    all_cities = None
    if id:
        all_cities = storage.all(City)
        all_cities = {k: v for k, v in all_cities if v.state_id == id}
    return render_template(
            '8-cities_by_states.html',
            all_states=all_states,
            all_cities=all_cities,
            )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
