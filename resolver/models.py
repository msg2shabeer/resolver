from resolver import db
from datetime import datetime
from marshmallow import Schema, fields, post_load

class User(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	name=db.Column(db.String(25))
	user_name=db.Column(db.String(20), unique=True)
	password=db.Column(db.String(40))
	user_type_id=db.Column(db.Integer,db.ForeignKey('user_type.id'))
	user_type = db.relationship('UserType',backref=db.backref('users', lazy='dynamic'))
	
	def __init__(self, name, user_name, password, user_type_id):
		self.name=name
		self.user_name=user_name
		self.password=password
		self.user_type_id=user_type_id

	def __repr__(self):
		return '<User %r>' % self.user_name

class UserSchema(Schema):
	id=fields.Integer()
	name=fields.Str()
	user_name=fields.Str()
	password=fields.Str()
	user_type_id=fields.Integer()

	@post_load
	def make_user(self, data):
		return User(**data)

class UserType(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	name=db.Column(db.String(25))
	description=db.Column(db.String(100))

	def __init__(self, name):
		self.name=name

	def __repr__(self):
		return '<User Type %r>' % self.name

class UserTypeSchema(Schema):
	id=fields.Integer()
	name=fields.Str()
	description=fields.Str()

	@post_load
	def make_user_type(self, data):
		return UserType(**data)

class Complaint(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	cust_id=db.Column(db.String(25))
	cust_name=db.Column(db.String(30))
	cust_address=db.Column(db.String(100))
	cust_phone=db.Column(db.String(15))
	complaint_phone=db.Column(db.String(15))
	no_calls=db.Column(db.Integer, default=1)
	date_time=db.Column(db.DateTime, default=datetime.utcnow())
	priority=db.Column(db.Float, default=0.00)
	
	service_id=db.Column(db.Integer, db.ForeignKey('service.id'))
	service=db.relationship('Service', backref=db.backref('complaints', lazy='dynamic'))
	
	complaint_type_id=db.Column(db.Integer, db.ForeignKey('complaint_type.id'))
	compaint_type=db.relationship('ComplaintType', backref=db.backref('complaints', lazy='dynamic'))
	
	status_id=db.Column(db.Integer, db.ForeignKey('complaint_status.id'))
	status=db.relationship('ComplaintStatus', backref=db.backref('complaints', lazy='dynamic'))

	def __init__(self, cust_id, cust_name, cust_address, cust_phone, complaint_phone, service_id, complaint_type_id, status_id, date_time=None):
		self.cust_id=cust_id
		self.cust_name=cust_name
		self.cust_address=cust_address
		self.cust_phone=cust_phone
		self.complaint_phone=complaint_phone
		self.service_id=service_id
		self.complaint_type_id=complaint_type_id
		self.status_id=status_id
		if date_time is None:
			date_time=datetime.utcnow()
		self.date_time=date_time


	def __repr__(self):
		return '<Complaint id:%r p:%r d:%r c_id:%r>' %(self.id,self.priority,self.date_time,self.cust_id)

class ComplaintSchema(Schema):
	id=fields.Integer()
	cust_id=fields.Str()
	cust_name=fields.Str()
	cust_address=fields.Str()
	cust_phone=fields.Str()
	complaint_phone=fields.Str()
	no_calls=fields.Integer()
	date_time=fields.DateTime()
	priority=fields.Float()
	service_id=fields.Integer()
	complaint_type_id=fields.Integer()
	status_id=fields.Integer()

	@post_load
	def make_complaint(self, data):
		return Complaint(**data)

class Service(db.Model):

	id=db.Column(db.Integer, primary_key=True)
	name=db.Column(db.String(20), unique=True)
	description=db.Column(db.String(100))


	def __init__(self, name):
		self.name=name

class ServiceSchema(Schema):
	id=fields.Integer()
	name=fields.Str()
	description=fields.Str()

	@post_load
	def make_service(self, data):
		return Service(**data)

class ComplaintType(db.Model):
	
	id=db.Column(db.Integer, primary_key=True)
	name=db.Column(db.String(20), unique=True)
	description=db.Column(db.String(100))

	service_id=db.Column(db.Integer, db.ForeignKey('service.id'))
	service=db.relationship('Service', backref=db.backref('complaint_types', lazy='dynamic'))
	
	def __init__(self, name, service_id):
		self.name=name
		self.service_id=service_id

class ComplaintTypeSchema(Schema):
	id=fields.Integer()
	name=fields.Str()
	service_id=fields.Integer()
	description=fields.Str()


	@post_load
	def make_complaint_type(self, data):
		return ComplaintType(**data)
		
class ComplaintStatus(db.Model):
	
	id=db.Column(db.Integer, primary_key=True)
	name=db.Column(db.String(20), unique=True)
	description=db.Column(db.String(100))


	def __init__(self, name):
		self.name=name

class ComplaintStatusSchema(Schema):
	id=fields.Integer()
	name=fields.Str()
	description=fields.Str()

	@post_load
	def make_complaint_status(self, data):
		return ComplaintStatus(**data)
