from resolver import app
from resolver.models import User
from flask import jsonify
# Home
@app.route('/')
def hello_world():
	return 'Welcome to resolver'

# Get all users
@app.route('/users/', methods = ['GET'])
def get_users():
	return jsonify({'users': User.query.all()})

# Get a single user

# Add a new user

# Get all complaints

# Get a single complaint by its ID

# Get complaints by customer ID

# Add a complaint