from . import db

class Property(db.Model):

    __tablename__ = 'properties'

    propertyId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128))
    numBed = db.Column(db.Integer)
    numBath = db.Column(db.Integer)
    location = db.Column(db.String(128))
    price = db.Column(db.Integer)
    prop_type = db.Column(db.String(20))
    description = db.Column(db.String(1000))
    photo = db.Column(db.Text)
    

    def __init__(self,title, numBed, numBath, location, price, prop_type, description, photo):
        self.title = title 
        self.numBed = numBed
        self.numBath = numBath
        self.location = location
        self.price = price  
        self.prop_type = prop_type
        self.description = description
        self.photo= photo
