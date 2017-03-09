from resolver import app
from resolver.models import *
from flask import jsonify,request
from flask_security import Security, SQLAlchemyUserDatastore, login_required

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Home
@app.route('/')
def hello_world():
	return 'Welcome to resolver'

# Get all users
@app.route('/users/', methods = ['GET'])
def get_users():
	users=User.query.all()
	return jsonify({'users' : UserSchema().dump(users, many=True).data}), 200

# Get a single user
@app.route('/users/<int:id>', methods = ['GET'])
def get_user(id):
	user = User.query.filter_by(id=id).first()
	if user:
		return jsonify({'user': UserSchema().dump(user).data}), 200
	else:
		return jsonify({'message' : 'User Do not Exist with id:'+str(id)}), 500

# Add a new user
@app.route('/users/', methods = ['POST'])
def put_user():
	try:
		db.session.add(UserSchema().load(request.json).data)
		db.session.commit()
	except Exception as e:
		return jsonify({'message' : 'User Creation Failed'}), 500
	else:
		return jsonify({'message' :'User Created successfully'}), 201

# Activate/Deactivate a user
# Eg: /users/1/activate/1 --> activates a user
# Eg: /users/1/activate/0 --> deactivates a user
@app.route('/users/<int:id>/activate/', methods = ['PUT'])
def activate_user(id):
	act=request.json['activate_flag']
	msg='User Deativated'
	user=User.query.filter_by(id=id).first()
	if not user:
		return jsonify({'message': 'No Such User'}), 500
	try:
		user.active=False
		if act:
			user.active=True
			msg='User Activated'
		db.session.add(user)
		db.session.commit()
	except Exception as e:
		return jsonify({'message': 'User Activation Failed'}), 500
	return jsonify({'message': msg}), 201


# Get Roles
@app.route('/roles/', methods=['GET'])
def get_roles():
	roles=Role.query.all()
	return jsonify({'roles' : RoleSchema().dump(roles, many=True).data}), 200

# Get a single Role
@app.route('/roles/<int:id>/', methods=['GET'])
def get_roles_by_id(id):
	role=Role.query.filter_by(id=id).first()
	if role:
		return jsonify({'role': RoleSchema().dump(role).data}), 200
	else:
		return jsonify({'message' : 'Role Do not Exist with id:'+str(id)}), 500


# Add a new role
@app.route('/roles/', methods = ['POST'])
def add_role():
	try:
		db.session.add(RoleSchema().load(request.json).data)
		db.session.commit()
	except Exception as e:
		return jsonify({'message' : 'Role Creation Failed'}), 500
	else:
		return jsonify({'message' :'Role Created successfully'}), 201

# Add a new role to an user
@app.route('/users/<int:id>/roles/', methods=['PUT'])
def add_user_role(id):
	user=User.query.filter_by(id=id).first()
	if not user:
		return jsonify({'message' : 'User Role Adding failed, there is no such user'}), 500
	for r in request.json['roles']:
		role=Role.query.filter_by(id=r).first()
		if role:
			user.roles.append(role)
	db.session.add(user)
	db.session.commit()
	return jsonify({'message' : 'User Role Added Successfully'}), 200


# Get all complaints
@app.route('/complaints/', methods=['GET'])
def get_complaints():
	complaints=Complaint.query.all()
	return jsonify({'complaints' : ComplaintSchema().dump(complaints, many=True).data}), 200

# Get a single complaint by its ID
@app.route('/complaints/<int:id>', methods = ['GET'])
def get_complaint(id):
	complaint = Complaint.query.filter_by(id=id).first()
	if complaint:
		return jsonify({'complaint' : ComplaintSchema().dump(complaint).data}), 200
	else:
		return jsonify({'message' : 'Complaints Do not Exist with id:'+str(id)}), 500

# Get complaints by customer ID
@app.route('/complaints/cust/<string:cust_id>', methods = ['GET'])
def get_complaint_cust(id):
	complaints = Complaint.query.filter_by(cust_id=str(cust_id))
	if complaints:
		return jsonify({'complaints' : ComplaintSchema().dump(complaints, many=True).data}), 200
	else:
		return jsonify({'message' : 'Complaints Do not Exist for customer id:'+str(id)}), 500

# Add a complaint --- Check for existing complaint
@app.route('/complaints/', methods = ['POST'])
def put_complaint():
	try:
		db.session.add(ComplaintSchema().load(request.json).data)
		db.session.commit()
	except Exception as e:
		return jsonify({'message' : 'Complaint Creation Failed'}), 500
	else:
		return jsonify({'message' : 'Complaint Created Successfully'}), 201

# Change complaint status
@app.route('/complaints/<int:id>/status/',methods = ['PUT'])
def change_complaint_status(id):
	complaint=Complaint.query.filter_by(id=id).first()
	if not complaint:
		return jsonify({'message' : 'Complaint Status Changing failed, there is no such complaint'}), 500
	complaint.status_id = request.json['status_id']
	db.session.add(complaint)
	db.session.commit()
	return jsonify({'message' : 'Complaint Status Changed Successfully'}), 200
