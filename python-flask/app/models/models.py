from database import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False,unique=True)
    addresses = db.relationship('Address', backref="User", lazy='dynamic')


    def __init__(self,name,password,email):
        self.name = name
        self.password = password
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.id
        

class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    postalcode = db.Column(db.Integer)
    municipality = db.Column(db.String(100))
    state = db.Column(db.String(100))
    neighborhood = db.Column(db.String(200))
    primary = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#    user = db.relationship('User')
 
 

    def __init__(self,postalcode,municipality,state,neighborhood, primary, user):
        self.postalcode = postalcode
        self.municipality = municipality
        self.state = state
        self.neighborhood = neighborhood
        self.primary = primary
        self.user = user

    def __repr__(self):
         return '<Address %r>' % self.id
       

