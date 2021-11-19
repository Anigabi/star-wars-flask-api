import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, PeopleDetails, People

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = os.environ.get('JWI_KEY')


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

@app.route('/people/', methods=['GET'])
def get_all_people():
    peoples = People.get_all_people()

    if peoples: 
        all_People = [people.to_dict() for people in peoples]
        return jsonify(all_People), 200

    return jsonify({'error':'Not character yet'}), 200
    

@app.route('/people/<int:id>', methods=['GET'])
def get_people_by_id(id): 
    people = people.get_by_id_people(id)
    
    if people: 
        return jsonify(people.to_dict()), 200

    return jsonify({'error':'Character not found'})

@app.route('/people/<int:id>/people-details', methods=['GET'])
def get_all_details():
    details = PeopleDetails.get_all_details()

    if details: 
        all_details = details.to_dict_details()
        return jsonify(all_details), 200 

    return jsonify({'error': 'Details not found'}), 200

#this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)



