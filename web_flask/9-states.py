from models import storage
from flask import Flask
from flask import render_template
from os import getenv
from models.state import State

app = Flask(__name__)


@app.route("/states", strict_slashes=False)
def states():
    """
    The function retrieves a list of all states from storage.
    """
    with_id = "0"
    all_states = storage.all(State)
    states = sorted(all_states.values(), key=lambda state: state.name)
    return render_template("9-states.html", states=states, with_id=with_id)


@app.route("/states/<id>", strict_slashes=False)
def states_id(id):
    """
    The function `states_id` retrieves a state object.
    """
    with_id = "1"
    all_state = storage.all(State)
    key = "State" + "." + str(id)
    try:
        state = all_state[key]
    except KeyError:
        width_id = "2"
        return render_template("9-states.html", width_id=width_id)
    storage_type = getenv("HBNB_TYPE_STORAGE")
    return render_template("9-states.html", state=state,
                           storage_type=storage_type, with_id=with_id)


@app.teardown_appcontext
def close(exception):
    """
    close a storage object.
    """
    storage.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
