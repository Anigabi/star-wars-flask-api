import simplejson as json

from flask_sqlalchemy import SQLAlchemy


# from sqlalchemy.orm import relationship

db = SQLAlchemy()


class PlanetDetails(db.Model):
    __tablename__:"planet_details"
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
            "climate":self.climate,
            "gravity":self.gravity,
            "diameter":self.diameter,
            "terrain":self.terrain,
            "orbitalperiod":self.orbitalperiod
        }
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self




class Planet(db.Model):
    __tablename__:"planet"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    planet_id= db.Column(db.Integer, db.ForeignKey("planet_details.id"), nullable=False)

    def __repr__(self):
        return f'The planet is {self.name}'
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
            # do not serialize the password, its a security breach
        }
    
    def create(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def get_all(cls):
        planets= cls.query.all()
        return planets
        
    @classmethod
    def get_byid(cls,id_planet):
        planet=cls.query.filter_by(id=id_planet).one_or_none()
        return planet

    
class User (db.Model):
    __tablename__:"user"
    id_user = db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(120),unique=True, nullable=False)
    password= db.Column(db.String(120),unique=True, nullable=False)

    def __repr__(self):
        return f'The email is {self.email}'
    
    def to_dict(self):
        return {
            "id": self.email
            # do not serialize the password, its a security breach
        }
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def get_userbyemail(cls,email_user):
        user= cls.query.filter_by(email=email_user).one_or_none()
        return user
    
    def create(self):
        db.session.add(self)
        db.session.commit()

   

#class Favouritesplanet:
 #   __tablename__:"planetfavs"
  #  id_user= db.Column(db.Integer,db.ForeignKey