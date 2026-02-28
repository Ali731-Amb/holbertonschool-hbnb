from flask_restx import Namespace, Resource, fields
from app.services import facade

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
    'title': fields.String(required=True, min_length=1, description='Title of the place'),
    'description': fields.String(min_length=1, description='Description of the place'),
    'price': fields.Float(required=True, min_length=1, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, min_length=1, required=True, description="List of amenities ID's")
})

#Define the review model for input validation and documentation 
review_model = api.model('Review',{
    'text' : fields.String(required=True, min_length=1, description='Title of the review'),
    'rating' : fields.Integer(required=True, min_length=1, description='Rating of the place from 1 to 5'),
    'place' : fields.String(required=True, min_length=1, description='Place of the review'),
    'user' : fields.String(required=True, min_length=1, description='User of the place')
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        place_data = api.payload #on utilise pas ça !! 
        try: 
            new_place = facade.create_place(api.payload)
            return new_place, 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.marshal_list_with(place_model)
    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        # Placeholder for logic to return a list of all places
        return facade.get_all_places(), 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.marshal_with(place_model)
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        # Placeholder for the logic to retrieve a place by ID, including associated owner and amenities
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
        # Placeholder for the logic to update a place by ID
        try:
            place_data = api.payload
            place = facade.update_place(place_id, place_data)
            return place, 200
        except ValueError as e:
            message = str(e)
            if "not found" in message:
                api.abort(404, message)
            else:
                api.abort(400, message)



@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.marshal_list_with(review_model)
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        # Placeholder for logic to return a list of reviews for a place
        try: 
            reviews = facade.get_reviews_by_place(place_id)
            return reviews, 200
        except ValueError as e: 
            api.abort(404, str(e))


    @api.response(204, 'Place successfully deleted')
    @api.response(404, 'Place not found')
    def delete(self, place_id):
        try:
            facade.delete_place(place_id)
        except ValueError as e:
            return api.abort(404, str(e))
        return '', 204