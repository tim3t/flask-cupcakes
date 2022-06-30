"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify
import flask_sqlalchemy
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

def serialize_cupcakes(cupcake):
    """Serialize a cupcake object to dictionary for JSON"""

    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    }

@app.route('/api/cupcakes')
def list_all_cupcakes():
    """Return JSON of all cupcakes"""

    cupcakes = Cupcake.query.all()
    serialized = [serialize_cupcakes(c) for c in cupcakes]

    return jsonify(cupcakes=serialized)

@app.route('/api/cupcakes/<cupcake_id>')
def list_single_cupcake(cupcake_id):
    """Return JSON of a single cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = serialize_cupcakes(cupcake)

    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """Post route to create/add a cupcake"""

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"] or None

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    db.session.add(new_cupcake)
    db.session.commit()

    serialized = serialize_cupcakes(new_cupcake)
    return (jsonify(cupcake=serialized), 201)

@app.route('/api/cupcakes/<cupcake_id>', methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Patch route to update an individual cupcake"""

    data = request.json
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = data["flavor"]
    cupcake.size = data["size"]
    cupcake.rating = data["rating"]
    cupcake.image = data["image"]
    db.session.commit()
    
    return jsonify(cupcake=cupcake.serialize_cupcakes())

@app.route('/api/cupcakes/<cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Delete an individual cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake_id)
    db.session.commit()
    return jsonify(message="Deleted")

