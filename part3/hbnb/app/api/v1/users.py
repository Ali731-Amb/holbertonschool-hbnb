from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'id': fields.String(readOnly=True, description='The unique identifier of the user'),
    'first_name': fields.String(required=True, min_lenght=1, description='First name of the user'),
    'last_name': fields.String(required=True, min_lenght=1, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'pets': fields.String(description='Pet of the user', enum=['DOG', 'CAT', 'OTHERS'])
    })

@api.route('/')
class UserList(Resource): 
    @api.response(200, 'Success')
    def get(self):
        """List all users"""
        users = facade.get_all_users()
        return [{
        'id': u.id,
        'first_name': u.first_name,
        'last_name': u.last_name,
        'email': u.email,
        'pets': u.pets.name if u.pets else None
                } for u in users], 200
    
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        new_user = facade.create_user(user_data)
        return {
        'id': new_user.id, 
        'message': 'User successfully registered'
        }, 201

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200
    
    @api.expect(user_model, validate = True)
    @api.response(200, 'User successfully upadated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        user_data = api.payload
        if 'email' in user_data:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user and existing_user.id != user_id:
                return {'error' : 'Email is already registered'}, 400
        updated_user = facade.update_user(user_id, user_data)
        if updated_user is None: 
            return {'error' : 'User not found'}, 404
        return{
            'id': updated_user.id, 
            'first_name': updated_user.first_name, 
            'last_name': updated_user.last_name, 
            'email': updated_user.email,
            'pets': updated_user.pets.name if updated_user.pets else None
                } , 200 

    @api.response(200, 'User successfully deleted')
    @api.response(400, 'Invalid input data')
    def delete(self, user_id):
        delete_user = facade.delete_user(user_id)
        if delete_user is False: 
            return {'error' : 'User not found'}, 404
        return {'message' : 'User deleted successfully'}, 200
    
    @jwt_required()
    def put(self, user_id):
        """Update user information"""
        current_user_id = get_jwt_identity()
        if current_user_id != user_id:
            return {'error': 'Unauthorized action. You can only update your own profile.'}, 403
        user_data = api.payload
        if 'email' in user_data:
            return {'error': 'Email cannot be modified'}, 400
        try:
            updated_user = facade.update_user(user_id, user_data)
            if not updated_user:
                return {'error': 'User not found'}, 404
            return updated_user.to_dict(), 200
        except Exception as e:
            return {"error": str(e)}, 400
