from flask import Blueprint, request
from flask_restx import Resource, Api, fields
from src import db
from src.api.models import User

# call blueprint

users_blueprint = Blueprint('users', __name__)
api = Api(users_blueprint)
user = api.model('User', {
    'id': fields.Integer(readOnly=True),
    'username': fields.String(required=True),
    'email': fields.String(required=True),
    'fullname': fields.String(required=True),
    'created_date': fields.DateTime,
})

# user api

class UsersList(Resource):
    @api.expect(user, validate=True)
    def post(self):
        post_data = request.get_json()
        username = post_data.get('username')
        email = post_data.get('email')
        fullname = post_data.get('fullname')
        response_object = {}

        # check duplicate email 

        user = User.query.filter_by(email=email).first()
        if user:
            response_object['message'] = 'Sorry, that email already exists.'
            return response_object, 400
        
        # check duplicate username

        user = User.query.filter_by(username=username).first()
        if user:
            response_object['message'] = 'Sorry, that username already exists.'
            return response_object, 400

        # add user

        db.session.add(User(username=username, email=email, fullname=fullname))
        db.session.commit()

        response_object = {
            'message': f'{username} was added!'
        }
        return response_object, 201

    # list all users

    @api.marshal_with(user, as_list=True)
    def get(self):
        return User.query.all(), 200

# return user by id

class Users(Resource):
    @api.marshal_with(user)
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            api.abort(404, f"User {user_id} does not exist")
        return user, 200

# add api endpoints

api.add_resource(UsersList, '/users')
api.add_resource(Users, '/users/<int:user_id>')
