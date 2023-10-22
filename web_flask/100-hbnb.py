#!/usr/bin/python3
"""#!/usr/bin/python3
""""script that starts a Flask web application"""

from flask import Flask
from flask import render_template
from models import storage

app = Flask(__name__)


@app.route("/hbnb_filters", strict_slashes=False)
def hbnb_filters():
    states = storage.all("State")
    amenities = storage.all("Amenity")
    return render_template("10-hbnb_filters.html",
                           states=states, amenities=amenities)


@app.teardown_appcontext
def teardown(excpt=None):
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
