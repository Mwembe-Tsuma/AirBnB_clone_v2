#!/usr/bin/python3
"""This module starts a flask web app, """

from web_flask import app
from flask import render_template
from models import storage
from models.state import State


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
    return render_template('7-states_list.html', all_states=all_states)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
