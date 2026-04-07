from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('auth', description='Authentication operations')

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login', methods=['POST'])
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload
        print("=== DEBUG LOGIN ===")
        print("Email reçu:", credentials['email'])
        user = facade.get_user_by_email(credentials['email'])
        print("User trouvé:", user)
        if user:
            print("Hash:", user.password_hash)
            print("Verify:", user.verify_password(credentials['password']))
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"is_admin": user.is_admin}
        )
        return {'access_token': access_token}, 200

@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        print("jwt------")
        print(get_jwt_identity())
        current_user = get_jwt_identity()
        return {'message': f'Hello, user {current_user}'}, 200
