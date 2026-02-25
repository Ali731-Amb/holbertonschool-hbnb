from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'id': fields.String(readOnly=True, description='The unique identifier of the amenity'),
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate= True)
    @api.marshal_with(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload
        return facade.create_amenity(amenity_data), 201

@api.marshal_list_with(amenity_model)
@api.response(200, 'List of amenities retrieved successfully')
def get(self):
	"""Retrieve a list of all amenities"""
	return facade.get_all_amenities(), 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.marshal_with(amenity_model)
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
            """Get amenity details by ID"""
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                    return {'error' : 'Amenity not found'}, 404
            return amenity


    @api.marshal_with(amenity_model)
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity_data = api.payload
        updated_amenity = facade.update_amenity(amenity_id, amenity_data)
        if updated_amenity is None:
            return {'error' : 'Amenity not found'}, 404
        return updated_amenity
