#!/usr/bin/python3
""""script that starts a Flask web application"""

from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity
from os import getenv
app = Flask(__name__)


@app.route("/hbnb_filters", strict_slashes=False)
def hbnb_filter():
    """ The function `hbnb_filter` retrieves data from storage."""
    storage_type = getenv("HBNB_TYPE_STORAGE")
    all_state = storage.all(State)
    all_amenity = storage.all(Amenity)
    amenities = sorted(all_amenity.values(),
                       key=lambda amenities: amenities.name)
    states = sorted(all_state.values(), key=lambda states: states.name)
    return render_template("10-hbnb_filters.html", states=states,
                           amenities=amenities, storage_type=storage_type)


@app.teardown_appcontext
def close(exception):
    """
    Close.
    """
    storage.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
