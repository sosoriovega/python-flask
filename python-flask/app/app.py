# Sergio Osorio Vega API REST using
# python, flask, db, blue print, JWT, bcrypt, Marshmallow, and SQL Alchemy
# docker and for testing porpuses I use Postman, MYSQL Workbench (and windows Mysql), 

#My imports:
from flask import Flask
from database import db
from sqlalchemy_utils import create_database, database_exists
from routes.routes import blue_print
from flask_jwt_extended import JWTManager
import datetime
import os

app = Flask(__name__)

#Data Base. I cfreate a root user with my password, we can create a specific user with any pass

#db_usuario = 'root'
#db_clave = 'sergio77'
#db_host = 'localhost'
#db_nombre = 'db_api_python'
#DB_URL = f'mysql+pymysql://{db_usuario}:{db_clave}@{db_host}/{db_nombre}'

db_usuario = os.environ.get('DB_USUARIO')
db_clave = os.environ.get('DB_CLAVE')
db_host = os.environ.get('DB_HOST')
db_nombre = os.environ.get('DB_NOMBRE')

DB_URL = f'mysql+pymysql://{db_usuario}:{db_clave}@{db_host}/{db_nombre}'


app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_SECRET_KEY'] =  os.environ.get('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=12)

#JWT
jwt = JWTManager(app)

# SQLAlchemy inicialization 
db.init_app(app)

#start routes
app.register_blueprint(blue_print)

#Data Base creation 
with app.app_context():
    if not database_exists(DB_URL):
        create_database(DB_URL)
    db.create_all()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)