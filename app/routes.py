from flask.helpers import make_response
from app import db 
from flask import Blueprint, request, jsonify
from app.models.planet import Planet

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

@planets_bp.route("", methods=["POST"], strict_slashes=False)
# Creates a planet object using provided request body information
def planets():
    request_body = request.get_json()
    new_planet = Planet(name=request_body["name"],
                        description=request_body["description"],
                        size=request_body["size"])
    db.session.add(new_planet)
    db.session.commit()

    return {
        "success": True,
        "message": f"Planet {new_planet.name} successfully created"
        }, 201

@planets_bp.route("", methods=["GET"], strict_slashes=False)
# Returns a list of all of the planets in the database
def planets_index():
    name_from_url = request.args.get("name")
    # search for planet by name
    if name_from_url:
        planets = Planet.query.filter_by(name=name_from_url)
    # search for all planets
    else:
        planets = Planet.query.all()

    planets_response = []
        
    for planet in planets:
        planets_response.append(planet.to_json())

    return jsonify(planets_response), 200

# Checks if the provided value is an integer; if not, returns false
def is_int(value):
    try:
        return int(value)
    except ValueError:
        return False

@planets_bp.route("/<planet_id>", methods=["GET","PUT","DELETE"], strict_slashes=False)
# Applies different request methods to specific planet objects
def handle_planet(planet_id):
    if not is_int(planet_id):
        return{
            "message": f"ID {planet_id} must be an integer",
            "success": False
        }, 400

    planet = Planet.query.get(planet_id)
    
    if planet is None:
        return make_response({
        "message": f"Planet with ID {planet_id} was not found",
        "success": False
    }, 404)

    # Searches for the planet with the provided id
    if request.method == "GET":
        return planet.to_json(), 200
    # Updates a planet object using provided request body information
    elif request.method == "PUT":
        form_data = request.get_json()

        planet.name = form_data["name"]
        planet.description = form_data["description"]
        planet.size = form_data["size"]

        db.session.commit()

        return {
            "success": True,
            "message": f"Planet {planet_id} successfully updated"
        }, 200

    # Deletes a planet object from database
    else:
        db.session.delete(planet)
        db.session.commit()

        return {
            "success": True,
            "message": f"Planet {planet_id} successfully deleted"
        }, 200
