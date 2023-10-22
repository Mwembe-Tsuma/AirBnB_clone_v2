from models import storage
from flask import Flask
from flask import render_template

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/states')
def states_list():
    states = storage.all("State")
    return render_template("9-states.html", state=states)


@app.route('/states/<id>')
def state_cities(id):
    for state in storage.all("State").values():
        if state.id == id:
            return render_template("9-states.html", state=state)
    return render_template("9-states.html")


@app.teardown_appcontext
def close_db_session(exception):
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
