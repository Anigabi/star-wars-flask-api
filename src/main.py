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
from models import db, StarshipsDetails, Starship
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

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
