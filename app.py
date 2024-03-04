"""Flask app for Cupcakes"""

import os

from flask import Flask, jsonify, request
# from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///cupcakes')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# debug = DebugToolbarExtension(app)

@app.get('/api/cupcakes')
def get_all_cupcakes():
    """Returns JSON with list of all cupcakes and their corresponding data
    {cupcakes: [
        so on
    ]}
    """
    # TODO: add "shape" of the data

    cupcakes = Cupcake.query.all()
    serialized_cupcakes = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes = serialized_cupcakes)


@app.get('/api/cupcakes/<int:cupcake_id>')
def get_single_cupcake(cupcake_id):
    """Returns JSON data about single cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake = cupcake.serialize())

@app.post('/api/cupcakes')
def add_cupcake():
    """Adds cupcake to database and returns JSON with new cupcake data"""

    new_cupcake = Cupcake(
        flavor = request.json['flavor'],
        size = request.json['size'],
        rating = request.json['rating'],
        image_url = request.json['image_url'] or None
    )

    db.session.add(new_cupcake)
    db.session.commit()

    return (jsonify(cupcake = new_cupcake.serialize()), 201)


# @app.patch('/api/cupcakes/<int:cupcake_id>')
# def update_cupcake(cupcake_id):
#     """Updates cupcake and returns JSON with updated cupcake information"""

#     cupcake = Cupcake.query.get_or_404(cupcake_id)
#     ...

# @app.delete('/api/cupcakes/<int:cupcake_id>')
# def delete_cupcake(cupcake_id):
#     """Delete cupcake and returns JSON with id of deleted cupcake"""

#     cupcake = Cupcake.query.get_or_404(cupcake_id)
