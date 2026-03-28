from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(min_lenght=1, description='First name of the owner'),
    'last_name': fields.String(min_lenght=1, description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'id': fields.String(readOnly=True, description='The unique identifier of the place'),
    'title': fields.String(required=True, min_length=1, description='Title of the place'),
    'description': fields.String(min_length=1, description='Description of the place'),
    'price': fields.Float(required=True, min_length=1, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(attribute='owner.id', description='ID of the owner'),
    'amenities': fields.List(
        fields.String(attribute='id'), 
        required=True, 
        min_length=1,
        description="List of amenities IDs"
    ),
    'reviews': fields.List(fields.String(attribute='id'), attribute='_reviews')})

#Define the review model for input validation and documentation 
review_model = api.model('Review', {
    'id': fields.String(readOnly=True, description='Review ID'),
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'user_id': fields.String(attribute='user.id', description='User ID'),
    'place_id': fields.String(attribute='place.id', description='Place ID')
})

@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User not found')
    @api.response(500, "An unexpected error occurred")
    def post(self):
        """Register a new place"""
        current_user_id = get_jwt_identity()
        data = api.payload
        user = facade.get_user(current_user_id)
        if not user:
            api.abort(404, 'User not found')
        data['owner_id'] = current_user_id
        try:
            new_place = facade.create_place(data)
            return new_place, 201
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, "An unexpected error occurred")

    @api.marshal_list_with(place_model)
    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        return facade.get_all_places(), 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @jwt_required()
    @api.marshal_with(place_model)
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        try:
            place = facade.get_place(place_id)
            return place, 200
        except ValueError as e:
            api.abort(404, str(e))

    @api.marshal_with(place_model)
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        current_user_id = get_jwt_identity()
        update_data = api.payload
        if not update_data:
            api.abort(400, 'No data provided')
        place = facade.update_place(place_id)
        if not place:
            api.abort(404, "Place not found")
        if str(place.owner_id) != str(current_user_id):
            api.abort(403, "Not authorized to modify this place")
        ALLOWED_FIELDS = ('title', 'description', 'price')
        invalid_fields = [f for f in update_data if f not in ALLOWED_FIELDS]
        if invalid_fields:
            api.abort(400, f"Fields not allowed: {', '.join(invalid_fields)}")
        try:
            updated_place = facade.update_place(place_id, update_data)
            return updated_place, 200
        except ValueError as e:
            api.abort(400, str(e))



@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.marshal_list_with(review_model)
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try: 
            reviews = facade.get_reviews_by_place(place_id)
            return reviews, 200
        except ValueError as e: 
            api.abort(404, str(e))


@api.response(204, 'Place successfully deleted')
@api.response(404, 'Place not found')
@api.response(403, 'Unauthorized action')
@jwt_required()
def delete(self, place_id):
    current_user = get_jwt_identity()
    place = facade.get_place(place_id)
    is_admin = current_user.get('is_admin', False)
    user_id = current_user.get('id')
    if not is_admin and place.owner_id != user_id:
        return {'error': 'Unauthorized action'}, 403
    try:
        facade.delete_place(place_id)
    except ValueError as e:
        return api.abort(404, str(e))
    return '', 204
    
#------------------------ Admin --------------------------
@api.route('/places/<place_id>')
class AdminPlaceModify(Resource):
    @jwt_required()
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    def put(self, place_id):
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')
        place = facade.get_place(place_id)
        update_data = api.payload
        if not is_admin and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403
        try:
            updated_place = facade.update_place(place_id, update_data)
            return updated_place, 200
        except ValueError as e:
            api.abort(400, str(e))
