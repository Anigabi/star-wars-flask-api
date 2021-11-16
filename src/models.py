from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class PlanetDetails(db.Model):
    __tablename__:"planet_details"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    climate = db.Column(db.String(120), unique=False, nullable=False)
    gravity = db.Column(db.Float(80), unique=False, nullable=False)
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
        return self
    
    @classmethod
    def get_all(cls):
        planets= cls.query.all()
        return planets
        
    @classmethod
    def get_byid(cls,id_planet):
        planet=cls.query.filter_by(id=id_planet).one_or_none()
        return planet



    
class PeopleDetails(db.Model):
    __tablename__:"people_details"
    id  = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    heigth = db.Column(db.DECIMAL, unique=False, nullable=False)
    mass = db.Column(db.DECIMAL, unique=False, nullable=False)
    hairColor = db.Column(db.String(250), unique=False, nullable=False)
    eyeColor = db.Column(db.String(250), unique=False, nullable=False)
    homeworld = db.Column(db.String(250), unique=False, nullable=False)

    detail_has_character = db.relationship('People', back_populates='people_has_details')

    def __repr__(self):
        return f'PeopleDetails is {self.name}, heigth: {self.heigth}, mass: {self.mass}, hairColor: {self.hariColor}, eyeColor: {self.eyeColor}, homeworld: {self.homeworld}'

    def to_dict(self):
        return  {
            "id": self.id,
            "name": self.name,
            "heigth": self.heigth,
            "mass": self.mass,
            "hairColor": self.hairColor,
            "eyeColor": self.eyeColor,
            "homeworld": self.homeworld
        }

    @classmethod 
    def get_all(cls):
        all_details = cls.query.all()
        return  all_details
    
    @classmethod 
    def get_by_id(cls, id): 
        create_details = cls.query.get(id)
        return create_details


class People(db.Model):
    __tablename__: "people"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    detail_id = db.Column(db.Integer, db.ForeignKey("people_details.id"), nullable=False)

    people_has_details = db.relationship("PeopleDetails", back_populates="detail_has_character")
    

    def __repr__(self):
        return f'People is {self.name}, id : {self.id}'

    def to_dict(self):        
        
        return {          
              "id": self.id,          
              "name": self.name,  
            }

    @classmethod 
    def get_all(cls):
        all_people = cls.query.all()
        return all_people
    
    #def get_by_id(cls):
    @classmethod 
    def get_by_id(cls, id): 
        character = cls.query.get(id)
        return character

    
            

   

