from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import relationship

db = SQLAlchemy()

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
    def get_by_id_starshipdetails(cls,id_starshipdetails):
        starshipdetails = cls.query.filter(id=id_starshipdetails).one_or_none()
        return starshipdetails

class Starship(db.Model):
    __tablename__: "starship"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    starships_id = db.Column(db.Integer, db.ForeignKey("starships_details.id"), nullable=False)    
    
    starship_have = db.relationship("StarshipsDetails", back_populates="starship_have_details")

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
        starship = cls.query.filter(id=id_starship).one_or_none()
        return starship
    


    


  