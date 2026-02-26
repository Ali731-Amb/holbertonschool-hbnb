from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns

def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')
    # Register the amenities namespace
    api.add_namespace('amenities', description='Amenity operations')
    # Register the place namespace
    api.add_namespace('places', description='Place operations')
    # Register the review namespace
    api.add_namespace('reviews', description='Review operations')
    return app