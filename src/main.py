"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from datetime import timedelta

from flask import Flask, request, jsonify, url_for
from sqlalchemy import exc
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

from utils import generate_sitemap
from models import db, User, Planet, PlanetDetails
from admin import setup_admin

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = os.environ.get('JWI_KEY')
jwt = JWTManager(app)

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


@app.route('/planet', methods=['GET'])
def get_planet():

    planets= Planet.get_all()

    if planets:
        all_planets= [planet.to_dict() for planet in planets]
        return jsonify(all_planets), 200

    return jsonify({'error':'No planets found'}), 200

@app.route('/planets/<int:id>/detail', methods=['GET'])
def get_planetdetail(id):

    planetdet= PlanetDetails.getby_id(id)

    if planetdet:
    
        return jsonify(planetdet.to_dict()), 200

    return jsonify({'error':'No details found'})


@app.route('/people', methods=['GET'])
def get_all_people():
    peoples = People.get_all_people()

    if peoples: 
        all_People = [people.to_dict() for people in peoples]
        return jsonify(all_People), 200

    return jsonify({'error':'People not found'}), 200


 #this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)



