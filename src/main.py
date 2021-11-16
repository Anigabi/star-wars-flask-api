"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Planet , PlanetDetails
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/planets', methods=['GET'])
def get_planet():

    planets= Planet.get_all()

    if planets:
        all_planets= [planet.to_dict() for planet in planets]
        return jsonify(all_planets), 200

    return jsonify({'error':'No planets found'})


@app.route('/planets/<int:id>', methods=['POST'])
def create_planet(id):
    new_planet= request.json.get('planet', None)

    if not new_planet:
        return jsonify({'error':'Missing data'}), 400
    
    planet=Planet(name=new_planet, planet_id=id)

    planet_created= planet.create()
    return jsonify(planet_created.to_dict()),201

@app.route('/planets/details', methods=['POST'])
def create_detailsplanet():
    
    

    name=request.json.get('name',None)
    climate=request.json.get('climate',None)
    gravity=request.json.get('gravity',None)
    diameter=request.json.get('diameter',None)
    terrain=request.json.get('terrain',None)
    orbitalperiod=request.json.get('orbitalperiod',None)

    if name:
        details= PlanetDetails(name=name, climate= climate, gravity=gravity, diameter=diameter, terrain=terrain,orbitalperiod=orbitalperiod)
        details.create()
        return jsonify(details.to_dict()),201
    
    return jsonify({'error':'Missing info'}), 404


   
        
        
        

    
    

    

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
