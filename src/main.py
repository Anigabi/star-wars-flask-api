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
from models import db, User,Planet, PlanetDetails, PeopleDetails, People, StarshipsDetails, Starship
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

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

@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if email and password:
        user = User.get_by_email(email)

        if user:
            '''check password'''
            access_token = create_access_token(identity=user.user_to_dict(), time=timedelta(hours=12))
            print(access_token)
            return jsonify({'token':access_token}), 200

        return jsonify({"msg": "Bad username or password"}), 401


@app.route('/user/<int:id>/favourite', methods=['GET'])
@jwt_required()
def get_fav(id):
    token_id = get_jwt_identity()

    if token_id == id:
        '''return favs'''
    return jsonify(user.to_dict()), 200


@app.route('/starships', methods=['GET'])
def get_starships():
    starships = Starship.get_all_starships()
    all_starships = [starship.to_dict() for starship in starships]
    return jsonify(all_starships), 200

@app.route('/starships/<int:id>', methods=['GET'])
def get_starship_by_id(id):
    starship = Starship.get_by_id_starship(id)
    
    if starship:
        return jsonify(starship.to_dict()), 200
    
    return jsonify({'error': 'Starship not found'}), 404

@app.route('/starshipsdetails', methods=['GET'])
def get_starshipsdetails():
    starshipsdetails = StarshipsDetails.get_all_starshipdetails()
    all_starshipsdetails = [starshipdetails.to_dict() for starshipdetails in starshipsdetails]
    return jsonify(all_starshipsdetails), 200

@app.route('/starshipsdetails/<int:id>', methods=['GET'])
def get_starshipdetails_by_id(id):
    starshipdetails = StarshipsDetails.get_by_id_starshipdetails(id)
    
    if starshipdetails:
        return jsonify(starshipdetails.to_dict()), 200
    
    return jsonify({'error': 'Starship not found'}), 404


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


@app.route('/starships/<int:id>', methods=['GET'])
def get_starship_by_id(id):
    starship = Starship.get_by_id_starship(id)
    
    if starship:
        return jsonify(starship.to_dict()), 200
    
    return jsonify({'error': 'Starship not found'}), 404

@app.route('/starshipsdetails', methods=['GET'])
def get_starshipsdetails():
    starshipsdetails = StarshipsDetails.get_all_starshipdetails()
    all_starshipsdetails = [starshipdetails.to_dict() for starshipdetails in starshipsdetails]
    return jsonify(all_starshipsdetails), 200

@app.route('/starshipsdetails/<int:id>', methods=['GET'])
def get_starshipdetails_by_id(id):
    starshipdetails = StarshipsDetails.get_by_id_starshipdetails(id)
    
    if starshipdetails:
        return jsonify(starshipdetails.to_dict()), 200
    
    return jsonify({'error': 'Starship not found'}), 404


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


@app.route('/People', methods=['GET'])
def get_all_people():
    peoples = People.get_all_people()

    if peoples: 
        all_People = [people.to_dict() for people in peoples]
        return jsonify(all_People), 200

    return jsonify({'error':'People not found'}), 200
    

@app.route('/People/<int:id>', methods=['GET'])
def get_people_by_id(id): 
    people = People.get_by_id_people(id)
    
    if people: 
        return jsonify(people.to_dict()), 200

    return jsonify({'error':'Character not found'})

@app.route('/PeopleDetails', methods=['GET'])
def get_all_details():
    details = PeopleDetails.get_all_details()

    if details: 
        all_details = [details.to_dict_details() for details in details]
        return jsonify(all_details), 200 

    return jsonify({'error': 'Details not found'}), 200

@app.route('/PeopleDtails/<int:id>', methods=['GET'])
def create_all_details_by_id():
    create_details = PeopleDetails.get_by_id_cceate_all_details(id)

    if create_details: 
        return jsonify(create_details.to_dict_details()), 200
    
    return jsonify({'error': 'Details not found'})

 #this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)



