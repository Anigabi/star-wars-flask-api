"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from sqlalchemy import exc
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Planet , PlanetDetails, User
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


@app.route('/planet', methods=['GET'])
def get_planet():

    planets= Planet.get_all()

    if planets:
        all_planets= [planet.to_dict() for planet in planets]
        return jsonify(all_planets), 200

    return jsonify({'error':'No planets found'}), 200


@app.route('/planets/<int:id>/detail', methods=['GET'])
def get_planet_details(id):
   
    planet= Planet.get_byid(id)

    if not planet:
        return jsonify({'error':'Missing planet'}), 400
      
    return jsonify(planet.to_dict()),201



def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if not (username and password):
        return ({'error':'Missing data'}), 400
    # Query your database for username and password
    user = User.get_userbyemail(email)
    if not user :
        # the user was not found on the database
        return jsonify({"msg": "Bad username or password"}), 401
    
    # create a new token with the user id inside
    access_token = create_access_token(identity=user.id)
    return jsonify({ "token": access_token, "user_id": user.id })

 #this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
