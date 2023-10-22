from models import storage
from flask import Flask
from flask import render_template
from os import getenv
from models import storage

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/states')
def states_list():
    current_id = "0"
    all_states = storage.all(State)
    states = sorted(all_states.values(), key=lambda state: state.name)
    return render_template("9-states.html",
                           states=states, current_id=current_id)


@app.route('/states/<id>')
def state_cities(id):
    current_id = "1"
    all_state = storage.all(State)
    key = "State" + "." + str(id)
    try:
        state = all_state[key]
    except KeyError:
        curr_id = "2"
        return render_template("9-states.html", curr_id=curr_id)
    storage_type = getenv("HBNB_TYPE_STORAGE")
    return render_template("9-states.html", state=state,
                           storage_type=storage_type, current_id=current_id)


@app.teardown_appcontext
def close_db_session(exception):
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
