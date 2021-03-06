from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt_extended import JWTManager


app = Flask(__name__)


"""Initializations by passing classinstaces to app"""

db=SQLAlchemy(app)
api = Api(app)
jwt=JWTManager(app)


"""sqlalchemy configs"""
app.config['JWT_SECRET_KEY'] = 'Jwt-secret-string'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SECRET_KEY']='some-secret-string'


"""enabling blacklisting in configuration"""
app.config['JWT_BLACKLIST_ENABLED']=True
app.config['JWT_BLACKLIST_TOKEN_CHECKS']=['access','refresh']



@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti=decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)


@app.before_first_request
def create_tables():
    db.create_all()


import views,models, resources

api.add_resource(resources.UserRegistration,'/registration')
api.add_resource(resources.UserLogin,'/login')
api.add_resource(resources.UserLogoutAccess,'/logout/access')
api.add_resource(resources.UserLogoutRefresh,'/logout/refresh')
api.add_resource(resources.TokenRefresh,'/token/refresh')
api.add_resource(resources.AllUsers,'/users')
api.add_resource(resources.SecretResource,'/secret')


