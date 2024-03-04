"""Flask app for Cupcakes"""

import os

from flask import Flask, jsonify, request
# from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Cupcake, DEFAULT_IMG_URL

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
    {
        "cupcakes": [
                {
                        "flavor": "choco",
                        "id": 6,
                        "image_url": "http://test.com/cupcake.jpg",
                        "rating": 5,
                        "size": "huge"
                }
        ]
    }
    """

    cupcakes = Cupcake.query.all()
    serialized_cupcakes = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized_cupcakes)


@app.get('/api/cupcakes/<int:cupcake_id>')
def get_single_cupcake(cupcake_id):
    """Returns JSON data about single cupcake
    {
        "cupcake": {
                "flavor": "choco",
                "id": 6,
                "image_url": "http://test.com/cupcake.jpg",
                "rating": 5,
                "size": "huge"
        }
    }
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.serialize())


@app.post('/api/cupcakes')
def add_cupcake():
    """Adds cupcake to database and returns JSON with new cupcake data
    Send data like this:
    {
        "flavor": "BAnana Choc",
        "size": "MEGA BIG",
        "rating": 10,
        "image_url": ""
    }
    Recieve data like this:
    {
        "cupcake": {
            "flavor": "BAnana Choc",
            "id": 7,
            "image_url": "http://test.com/cupcake.jpg",
            "rating": 10,
            "size": "MEGA BIG"
        }
    }

    """

    new_cupcake = Cupcake(
        flavor=request.json['flavor'],
        size=request.json['size'],
        rating=request.json['rating'],
        image_url=request.json['image_url'] or None
    )

    db.session.add(new_cupcake)
    db.session.commit()

    return (jsonify(cupcake=new_cupcake.serialize()), 201)


@app.patch('/api/cupcakes/<int:cupcake_id>')
def update_cupcake(cupcake_id):
    """Updates cupcake and returns JSON with updated cupcake information
    Send data like this:
    {
        "flavor": "vanilla"
    }
    (note that you can pass any of flavor, rating, size, image_url)

    Receive data like this
    {
        "cupcake": {
            "flavor": "vanilla",
            "id": 6,
            "image_url": "https://tinyurl.com/demo-cupcake",
            "rating": 5,
            "size": "huge"
        }
    }
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image_url = request.json.get('image_url', cupcake.image_url) or DEFAULT_IMG_URL

    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())


@app.delete('/api/cupcakes/<int:cupcake_id>')
def delete_cupcake(cupcake_id):
    """Delete cupcake and returns JSON with id of deleted cupcake
    Receive data like this:
    {
        "deleted": [
            6
        ]
    }
    """


    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(deleted=[cupcake_id])
