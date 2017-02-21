from resolver import app
from resolver.models import *
from flask import jsonify,request
from resolver import db
# Home
@app.route('/')
def hello_world():
	return 'Welcome to resolver'

# Get all users
@app.route('/users/', methods = ['GET'])
def get_users():
	users=jsonify({'users':[UserJsonSerializer().serialize(x) for x in User.query.all()]})
	# to debug , we could use app.logger.debug(users.get_data())
	return users

# Get a single user
@app.route('/user/<int:id>', methods = ['GET'])
def get_user(id):
	user = jsonify({'user':[UserJsonSerializer().serialize(x) for x in User.query.filter_by(id=id)]})
	return user

# Add a new user
@app.route('/user/add', methods = ['POST'])
def put_user():
	db.session.add(UserJsonSerializer().deserialize(orequest.json))
	db.session.commit()
	return jsonify({'message' :'User Created successfully'}), 200

# Get all complaints

# Get a single complaint by its ID

# Get complaints by customer ID

# Add a complaint
@app.route('/complaint/add',methods = ['POST'])
def put_complaint():
	db.session.add(Complaint(**request.json))
	db.session.commit()
	return jsonify({'message' : 'Complaint Created Successfully'}), 200

# Change complaint status

# Get complaint by it's id