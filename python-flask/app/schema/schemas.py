from flask_marshmallow import Marshmallow

ma = Marshmallow()

# User Schema

class UserSchema(ma.Schema):
    class Meta:
            fields = ('id', 'name', 'password', 'email')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


#Address Schema
class AddressSchema(ma.Schema):
    class Meta:
        fields = ('id', 'postalcode', 'municipality', 'state', 'neighborhood', 'primary', 'user_id')

address_schema = AddressSchema()
addresses_schema = AddressSchema(many=True)