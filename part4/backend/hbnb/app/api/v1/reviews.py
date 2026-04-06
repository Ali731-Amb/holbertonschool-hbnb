from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'id': fields.String(readOnly=True, description='Review ID'),
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(description='User ID'),
    'place_id': fields.String(description='Place ID')
})

@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.marshal_with(review_model)
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self): 
        """Register a new review"""
        current_user_id = get_jwt_identity()
        review_data = api.payload
        place_id = review_data.get('place_id')
        place = facade.get_place(place_id)
        if not place : 
            api.abort(404, "Place not found")
        if place.owner_id == current_user_id:
            api.abort(400, "You cannot review your own place")
        existing_review = facade.get_user_review_for_place(current_user_id, place_id)
        if existing_review:
            api.abort(400, "You have already reviewed this place")
        review_data['user_id'] = current_user_id
        try:
            new_review = facade.create_review(review_data)
            return new_review, 201
        except ValueError as e : 
            api.abort(400, str(e))            

    @api.marshal_list_with(review_model)
    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        return facade.get_all_reviews(), 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.marshal_with(review_model)
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error' : 'Review not found'}, 404
        return review

    @jwt_required()
    @api.marshal_with(review_model)
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unautorized action')
    def put(self, review_id):
        """Update a review's information"""
        current_user_id = get_jwt_identity()
        update_data = api.payload
        if not update_data:
            api.abort(404, 'Review not found')
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, 'Review not found')
        if str(review.user_id) != str(current_user_id):
            api.abort(403, 'You can update only your own review')
        ALLOWED_FIELDS = ('text', 'rating')
        invalid_fields = [f for f in update_data if f not in ALLOWED_FIELDS]
        if invalid_fields:
            api.abort(400, f"Fields not allowed: {', '.join(invalid_fields)}")
        try: 
            updated_review = facade.update_review(review_id, update_data)
            if not updated_review: 
                api.abort(400, 'Review update failed')
            return updated_review.to_dict(), 200
        except ValueError as e: 
            api.abort(400, str(e))

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unautorized action')
    @api.response(500, 'An error occured during deltion')
    def delete(self, review_id):
        current_user_id = get_jwt_identity()
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, 'Review not found')
        if str(review.user_id) != str(current_user_id):
            api.abort(403, 'You can only delete your own review')
        try:
            facade.delete_review(review_id)
            return {'message': 'Review deleted successfully'}, 200
        except Exception as e:
            api.abort(500, f'An error occured during deletion: {str(e)}')
