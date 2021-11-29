import simplejson as json
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

favouritespeople = db.Table('favouritespeople',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('people_id', db.Integer, db.ForeignKey('people.id'), primary_key=True)
)

starshipfavourites = db.Table('starshipfavourites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('starship_id', db.Integer, db.ForeignKey('starship.id'), primary_key=True)
)

class Favplanet(db.Model):
    __tablename__="favplanet"
    id= db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"), nullable=False)
    favplanethave=db.relationship("Planet", back_populates="planet_havefav")
    

    def __repr__(self):
        return f'The planet is {self.planet_id}'
    
    def to_dict(self):
        return {
            "id-user": self.user_id,
            "id-planet": self.planet_id
            # do not serialize the password, its a security breach
        }
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class User(db.Model):
    __tablename__: "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=False, nullable=False)
    _password = db.Column(db.String(120), unique=False, nullable=False)
    _is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    have_a_user_favourite_people = db.relationship('People', secondary=favouritespeople, back_populates='have_a_favourite_people')
    have_user_starship = db.relationship('Starship', secondary=starshipfavourites, back_populates="have_user_starshipfav")
    favorites = db.relationship("Favplanet")

    def __repr__(self):
        return f'User {self.email}, id: {self.id}' 

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "people": [people.to_dict() for people in self.have_a_user_favourite_people]
            "starships": [starship.to_dict() for starship in self.have_user_starship]
        }

    @classmethod
    def get_by_email(cls,email):
        user = cls.query.filter_by(email=email).one_or_none()
        return user
    
    @classmethod
    def get_user_by_id(cls,id):
        user = cls.query.get(id)
        return user

    def add_fav_starship (self,starship):
        self.have_user_starship.append(starship)
        db.session.commit()
        return self.have_user_starship

    @classmethod 
    def get_user_by_id(cls,id): 
        user = cls.query.get(id)
        return user

    def add_fav_people(self,people):
        self.have_a_user_favourite_people.append(people)
        return self.have_a_user_favourite_people

        

class StarshipsDetails(db.Model):
    __tablename__: "starships_details"

    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(250), nullable=False)
    starship_class = db.Column(db.String(250), nullable=False)
    length = db.Column(db.String(250), nullable=False)
    passengers = db.Column(db.String(250), nullable=False)

    starship_have_details = db.relationship("Starship", back_populates="starship_have")
   

    def __repr__(self):
        return f'StarshipsDetails is {self.model}, starship_class: {self.starship_class}, length: {self.length}, passengers: {self.passengers}' 


    def to_dict(self):
        return {
            "id": self.id,
            "model": self.model, 
            "starship_class": self.starship_class, 
            "length": self.length, 
            "passengers": self.passengers,
        }

    @classmethod
    def get_all_starshipdetails(cls):
        starshipsdetails = cls.query.all()
        return starshipsdetails

    @classmethod
    def get_by_id_starshipdetails(cls,id):
        starshipdetails = cls.query.get(id)
        return starshipdetails


class Starship(db.Model):
    __tablename__: "starship"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    starships_id = db.Column(db.Integer, db.ForeignKey("starships_details.id"), nullable=False)    
    
    starship_have = db.relationship("StarshipsDetails", back_populates="starship_have_details")
    have_user_starshipfav = db.relationship('User', secondary=starshipfavourites, back_populates="have_user_starship")

    def __repr__(self):
        return f'Starships is {self.name}, id: {self.id}' 


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }


    @classmethod
    def get_all_starships(cls):
        starships = cls.query.all()
        return starships
    

    @classmethod
    def get_by_id_starship(cls,id_starship):
        starship = cls.query.get(id_starship)
        return starship
    
    


class PlanetDetails(db.Model):
    __tablename__: "planet_details"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    climate = db.Column(db.String(120), unique=False, nullable=False)
    gravity = db.Column(db.Float, unique=False, nullable=False)
    diameter = db.Column(db.Float, unique=False, nullable=False)
    terrain = db.Column(db.String(80), unique=False, nullable=False)
    orbitalperiod = db.Column(db.Integer, unique=False, nullable=False)
    

    def __repr__(self):
        return f'The diameter is {self.diameter}'


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "gravity": self.gravity,
            "diameter": self.diameter,
            "terrain": self.terrain,
            "orbitalperiod": self.orbitalperiod
        }
    
    @classmethod
    def getby_id(cls,id):
        planetdetail=cls.query.get(id)
        return planetdetail
    

class Planet(db.Model):
    __tablename__: "planet"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    planet_id= db.Column(db.Integer, db.ForeignKey("planet_details.id"), nullable=False)
    planet_havefav = db.relationship("Favplanet", back_populates="favplanethave")


    def __repr__(self):
        return f'The planet is {self.name}'
    

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

    
    @classmethod
    def get_all(cls):
        planets= cls.query.all()
        return planets
        

    @classmethod
    def get_byid(cls,id_planet):
        planet=cls.query.filter_by(id=id_planet).one_or_none()
        return planet


class PeopleDetails(db.Model):
    __tablename__: "people_details"

    id  = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    heigth = db.Column(db.DECIMAL, unique=False, nullable=False)
    mass = db.Column(db.DECIMAL, unique=False, nullable=False)
    hairColor = db.Column(db.String(250), unique=False, nullable=False)
    eyeColor = db.Column(db.String(250), unique=False, nullable=False)
    homeworld = db.Column(db.String(250), unique=False, nullable=False)

    detail_has_character = db.relationship("People", back_populates="people_has_details")
    

    def __repr__(self):
        return f'PeopleDetails is {self.name}, heigth: {self.heigth}, mass: {self.mass}, hairColor: {self.hairColor}, eyeColor: {self.eyeColor}, homeworld: {self.homeworld}'


    def to_dict_details(self):
        return  {
            "id": self.id,
            "name": self.name,
            "heigth": json.dumps(self.heigth , use_decimal=True),
            "mass": json.dumps(self.mass , use_decimal=True),
            "hairColor": self.hairColor,
            "eyeColor": self.eyeColor,
            "homeworld": self.homeworld
        }


    @classmethod 
    def get_all_details(cls):
        all_details = cls.query.all()
        return  all_details
    

    @classmethod 
    def get_by_id_cceate_all_details(cls, id_create_all_details): 
        create_details = cls.query.get(id)
        return create_details


class People(db.Model):
    __tablename__: "people"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    detail_id = db.Column(db.Integer, db.ForeignKey("people_details.id"), nullable=False) 

    people_has_details = db.relationship("PeopleDetails", back_populates="detail_has_character")
    have_a_favourite_people = db.relationship("User", secondary=favouritespeople, back_populates="have_a_user_favourite_people")


    def __repr__(self):
        return f'People is {self.name}, id : {self.id}'


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }


    @classmethod 
    def get_all_people(cls):
        all_people = cls.query.all()
        return all_people
    

    @classmethod 
    def get_by_id_people(cls, id): 
        character = cls.query.get(id)
        return character

   