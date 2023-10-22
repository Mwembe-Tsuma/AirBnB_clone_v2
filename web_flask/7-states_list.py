#!/usr/bin/python3
""""script that starts a Flask web application"""

from flask import render_template
from models import storage
from models.state import State


@app.teardown_appcontext
def teardown(exception):
    storage.close()
    if exception:
        print(exception)


@app.route('/states_list', strict_slashes=False)
def states_list():
    all_states = storage.all(State)
    return render_template('7-states_list.html', states=states)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
