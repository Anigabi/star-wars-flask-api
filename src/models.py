from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
            # do not serialize the password, its a security breach
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

