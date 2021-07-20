#For routes we import jsonify, JWT, my models, schemas, db and bcrypt 

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from models.models import User, Address
from schema.schemas import address_schema, addresses_schema, user_schema, users_schema
from database import db
import bcrypt

blue_print = Blueprint('app', __name__)

#Initial route 
@blue_print.route('/', methods=['GET'])
def inicio():
    return jsonify(respuesta='This is an API REST with Python, Flask, and MySQL')

#Create User
@blue_print.route('/create/users', methods=['POST'])
def create_user():
    try:
        #Get new user name
        name = request.json.get('name')
        #Get password
        password = request.json.get('password')
        #Get email
        email = request.json.get('email')

        if not name or not password or not email: 
            return jsonify (respuesta='Invalid fields, name, password and email are mandatory'),400

        #Check DB by existing email
        email_exist = User.query.filter_by(email=email).first()

        if email_exist:
            return jsonify(respuesta='Email already in use, please use another'), 400

        #Password Encrypt
        encrypted_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

        #Create model and insert in database
        new_user = User(name,encrypted_password,email)

        db.session.add(new_user)
        db.session.commit()

        return jsonify(respuesta='Success User Created'), 201

    except Exception:
        return jsonify(respuesta='Error 500'),500

#Login Route
@blue_print.route('/login/users',methods=['POST'])
def new_session():
    try:
         #Obtain email
        email = request.json.get('email')
        #Obtain password
        password = request.json.get('password')
        
        if not password or not email: 
            return jsonify (respuesta='Invalid fields, password and email are mandatory'), 400

        #Check DB
        email_exist = User.query.filter_by(email=email).first()    

        if not email_exist:
            return jsonify(respuesta='Email not found'), 404

        valid_password = bcrypt.checkpw(password.encode('utf-8'), email_exist.password.encode('utf-8'))

        # if valid password is ok, then it creates valid token you must add this TOKEN to authorization "bearer token"
        if valid_password:
            access_token = create_access_token(identity=email)
            return jsonify(access_token=access_token), 200
        return jsonify(respuesta='Incorrect email or password'), 404

    except Exception:
        return jsonify(respuesta='Error 500'), 500

#Ruta - Get User by ID
@blue_print.route('/get/users/<int:id>', methods=['GET'])
@jwt_required()
def get_users_by_id(id):
    try:
        user = User.query.get(id)
        #If user exists
        if user:
            addresses = Address.query.filter_by(user_id=id).all()

            #json is a combine user and address json "a json with an array"
            json = '{ ' + '"name": ' + '"' + str(user.name).strip() + '", ' + ' "email":  ' + '"' + str(user.email).strip() + '", ' + '"addresses":  '
            json = json + '[ '

            #obtain all the values for addresses in a for
            for u in addresses:
                 json = json + '{ "id" : "' + str(u.id) + '", "postalcode": "' + str(u.postalcode) + '", "municipality": "' + str(u.municipality) + '", "state": "' + str(u.state) + '", "neighborhood": "' + str(u.neighborhood) + '", "primary": "' + str(u.primary) + '" }, '  
            json = json[:-2] +  "]  }"         
            return jsonify(json), 200
        else:
            return jsonify(respuesta='User not found'), 404
    except Exception:
        return jsonify(respuesta='Error 500'), 500        

#JWT Protected routes

#Ruta - Get Users
@blue_print.route('/get/users', methods=['GET'])
@jwt_required()
def get_users():
    try:
        users = User.query.all()
        answer = users_schema.dump(users)

        return users_schema.jsonify(answer), 200
    except Exception:
        return jsonify(answer='Error 500'), 500


#Ruta - Create Address
@blue_print.route('/create/users/<int:id>/addresses', methods=['POST']) 
@jwt_required()
def create_address(id):
    try:

        user_id = User.query.get(id)

        if not user_id:
            return jsonify(respuesta='User not found'), 404
        
        #Checks if there is more than 3 addresses
        count_address = Address.query.filter_by(user_id=id).count()


        if count_address < 3:
            primary = False
            #If we are creating the first address then it will be the default/primary address
            if count_address == 0:
                primary = True


            postalcode = request.json['postalcode']
            municipality = request.json['municipality']
            state = request.json['state']
            neighborhood = request.json['neighborhood']
            new_address = Address(postalcode,municipality,state,neighborhood,primary,id)    
            user_id.addresses.append(new_address)

            #Add new address to the data base
            db.session.add(new_address) 
            db.session.commit()
            return jsonify(respuesta='Success. Address created'), 201

        else:
            return jsonify(respuesta='Sorry, you cant have more than 3 addresses'), 201

                
    except Exception:
        return jsonify(respuesta='Error 500'), 500


#Ruta - User Update Password
@blue_print.route('/update/user/<int:id>/update-password', methods=['PUT'])
@jwt_required()
def update_user(id):
    try:
        user = User.query.get(id)
        #Obtain email
        email = request.json.get('email')
        if not user or not user.email == email:
            return jsonify(respuesta='Sorry, User or email are wrong'), 404

       
        #Obtain old password
        old_password = request.json.get('oldpassword')
         #Obtain new password
        new_password = request.json.get('newpassword')

        #Check if it is a valid password
        valid_password = bcrypt.checkpw(old_password.encode('utf-8'), user.password.encode('utf-8'))
        if valid_password:
            #Password Encrypt
            encrypted_password = bcrypt.hashpw(new_password.encode('utf-8'),bcrypt.gensalt())
            user.password = encrypted_password
            db.session.commit()
            return jsonify(respuesta='Update Password Successful'), 200
        else:
            return jsonify(respuesta='Error, Wrong Password'), 404
        
    except Exception:
        return jsonify(respuesta='Error 500'), 500        



#Ruta - Get Addresses
@blue_print.route('/get/addresses', methods=['GET'])
@jwt_required()
def get_addresses():
    try:
        addresses = Address.query.all()
        answer = addresses_schema.dump(addresses)

        return addresses_schema.jsonify(answer), 200
    except Exception:
        return jsonify(answer='Error 500'), 500

#Ruta - Get address by ID
@blue_print.route('/get/addresses/<int:id>', methods=['GET'])
@jwt_required()
def get_addresses_by_id(id):
    try:
        address = Address.query.get(id)
        if address:
            return address_schema.jsonify(address), 200
        else:
            return jsonify(respuesta='Error Address not found'), 404  
    except Exception:
        return jsonify(respuesta='Error 500'), 500        

#Ruta - Update Address
@blue_print.route('/update/user/<int:id>/addresses/<int:ad_id>', methods=['PUT'])
@jwt_required()
def update_address(id,ad_id):
    try:
        #Get user and address
        user = User.query.get(id)
        address = Address.query.get(ad_id)

        #If there is no address or user it returns a user-not-found message
        if not address or not user or address.user_id != id:
            return jsonify(respuesta='User or Address not found'), 404

        primary = request.json.get('primary')
        if primary == "True":
            bol_primary = True
        else:    
            bol_primary = False
        
        #You cant change default/primary address to False, first select which will be your primary address
        if primary == "False" and address.primary:
            return jsonify(respuesta='Error, you must have one primary address'), 404

        #If you edit a non primary address to primary, then it search for the old_primary and change it to false
        if primary == "True" and address.primary == False:
            primary_address = Address.query.filter(Address.primary==True,Address.user_id==id).first()
            primary_address.primary = False

        #Update all the address values    
        address.postalcode = request.json['postalcode']
        address.municipality = request.json['municipality']
        address.state = request.json['state']
        address.neighborhood = request.json['neighborhood']
        address.primary = bol_primary
        db.session.commit()

        return jsonify(respuesta='Udate Address Successful'), 200
    except Exception:
        return jsonify(respuesta='Error 500'), 500        


#Ruta - Delete Address
@blue_print.route('/delete/addresses/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_address_by_id(id):
    try:
        address = Address.query.get(id)
        
        if not address:
            return jsonify(respuesta='Address not found'), 404

        db.session.delete(address)    
        db.session.commit()
        return jsonify(respuesta='Success. Address deleted.'), 200
    except Exception:
        return jsonify(respuesta='Error 500'), 500            