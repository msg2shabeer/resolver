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
	return users, 200

# Get a single user
@app.route('/users/<int:id>', methods = ['GET'])
def get_user(id):
	user = jsonify({'user':[UserJsonSerializer().serialize(x) for x in User.query.filter_by(id=id)]})
	return user, 200

# Add a new user
@app.route('/users/', methods = ['POST'])
def put_user():
	try:
		db.session.add(UserJsonSerializer().deserialize(request.json))
		db.session.commit()
	except Exception as e:
		return jsonify({'message' : 'User Creation Failed'}), 500
	else:
		return jsonify({'message' :'User Created successfully'}), 201

# Get all complaints
@app.route('/complaints/', methods=['GET'])
def get_complaints():
	complaints=jsonify({'complaints':[ComplaintJsonSerializer(utc_offset=app.config['UTC_OFFSET']).serialize(x) for x in Complaint.query.all()]})
	return complaints, 200

# Get a single complaint by its ID
@app.route('/complaints/<int:id>', methods = ['GET'])
def get_complaint(id):
	complaint = jsonify({'complaint':[ComplaintJsonSerializer(utc_offset=app.config['UTC_OFFSET']).serialize(x) for x in Complaint.query.filter_by(id=id)]})
	return complaint, 200

# Get complaints by customer ID
@app.route('/complaints/cust/<int:id>', methods = ['GET'])
def get_complaint_cust(id):
	complaint = jsonify({'complaint':[ComplaintJsonSerializer(utc_offset=app.config['UTC_OFFSET']).serialize(x) for x in Complaint.query.filter_by(id=id)]})
	return complaint, 200

# Add a complaint --- Check for existing complaint
@app.route('/complaints/', methods = ['POST'])
def put_complaint():
	try:
		db.session.add(ComplaintJsonSerializer().deserialize(request.json))
		db.session.commit()
	except Exception as e:
		return jsonify({'message' : 'Complaint Creation Failed'}), 500
	else:
		return jsonify({'message' : 'Complaint Created Successfully'}), 201

# Change complaint status
@app.route('/complaints/<int:id>/status/',methods = ['PUT'])
def change_complaint_status(id):
	complaint=Complaint.query.filter_by(id=id).first() #return first result
	if not complaint:
		return jsonify({'message' : 'Complaint Status Changing failed, there is no such complaint'}), 500
	complaint.status_id = request.json['status_id']
	db.session.add(complaint)
	db.session.commit()
	return jsonify({'message' : 'Complaint Status Changed Successfully'}), 200
