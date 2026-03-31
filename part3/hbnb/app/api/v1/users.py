from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'id': fields.String(readOnly=True, description='The unique identifier of the user'),
    'first_name': fields.String(required=True, min_lenght=1, description='First name of the user'),
    'last_name': fields.String(required=True, min_lenght=1, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'pets': fields.String(description='Pet of the user', enum=['DOG', 'CAT', 'OTHERS'])
    })

user_update_model = api.model('User', {
    'id': fields.String(readOnly=True, description='The unique identifier of the user'),
    'first_name': fields.String(required=True, min_lenght=1, description='First name of the user'),
    'last_name': fields.String(required=True, min_lenght=1, description='Last name of the user'),
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
    
    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload
        if "password" not in user_data or not user_data["password"]:
            return {'erreur' : 'A password is required'}, 400
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
    
    @jwt_required()
    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @api.response(500, 'Internal server error')
    def put(self, user_id):
        current_user_id = get_jwt_identity()
        update_data = api.payload
        if not update_data:
            api.abort(400, 'Invalid input data')
        if str(user_id) != str(current_user_id):
            api.abort(403, 'You can only update your own informations')
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, 'User not found')
        ALLOWED_FIELDS = ['first_name', 'last_name']
        if not all(field in ALLOWED_FIELDS for field in update_data):
            api.abort(403, f"Only {', '.join(ALLOWED_FIELDS)} can be updated")
        try:
            updated_data = facade.update_user(user_id, update_data)
            return {
                'message': 'User update successfully',
                'user': updated_data
            }, 200
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, "An unexpected error occurred during update")

    @api.response(200, 'User successfully deleted')
    @api.response(400, 'Invalid input data')
    def delete(self, user_id):
        delete_user = facade.delete_user(user_id)
        if delete_user is False: 
            return {'error' : 'User not found'}, 404
        return {'message' : 'User deleted successfully'}, 200

#-------------------- Admin -----------------

@api.route('/users/')
class AdminUserCreate(Resource):

    @jwt_required()
    def post(self):
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        user_data = api.payload
        email = user_data.get('email')
        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400
        new_user = facade.create_user(user_data)
        return {
        'id': new_user.id, 
        'message': 'User successfully registered'
        }, 201
    
@api.route('/users/<user_id>')
class AdminUserModify(Resource):
    @jwt_required()
    @api.response(200, 'User update successfully')
    @api.response(400, 'Email already registered')
    @api.response(403, 'Unauthorized action')
    @api.response(500, "An unexpected error occurred during update")
    def put(self, user_id):
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        data = api.payload
        email = data.get('email')
        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400
        try:
            updated_data = facade.update_user(user_id, data)
            return {
                'message': 'User update successfully',
                'user': updated_data
            }, 200
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, "An unexpected error occurred during update")