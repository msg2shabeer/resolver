from resolver import db
from datetime import datetime
from resolver.json_serializer import JsonSerializer


class User(db.Model):
	'''User table to store the user information, includes admin and staffs'''
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

class UserJsonSerializer(JsonSerializer):
	__attributes__ = ['id', 'name', 'user_name', 'password','user_type_id']
	__required__ = ['name', 'user_name', 'password', 'user_type_id']
	__attribute_serializer__ = dict()
	__object_class__ = User

class UserType(db.Model):
	'''Table storing category details of users'''
	id=db.Column(db.Integer, primary_key=True)
	name=db.Column(db.String(25))

	def __init__(self, name):
		self.name=name

	def __repr__(self):
		return '<User Type %r>' % self.name

class UserTypeJsonSerializer(JsonSerializer):
	__attributes__ = ['id', 'name']
	__required__ = ['name']
	__attribute_serializer__ = dict()
	__object_class__ = UserType
		

class Complaint(db.Model):
	'''Complaints table'''
	id=db.Column(db.Integer, primary_key=True)
	cust_id=db.Column(db.String(25))
	cust_name=db.Column(db.String(30))
	cust_address=db.Column(db.String(100))
	cust_phone=db.Column(db.String(15))
	complaint_phone=db.Column(db.String(15))
	no_calls=db.Column(db.Integer, default=1)
	date_time=db.Column(db.DateTime)
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

class ComplaintJsonSerializer(JsonSerializer):
	__attributes__ = ['id', 'cust_id', 'cust_name', 'cust_address', 'cust_phone',\
	 'complaint_phone', 'no_calls', 'priority', 'date_time', 'service_id', 'complaint_type_id', 'status_id']
	__required__ = ['cust_id', 'cust_name', 'cust_address', 'cust_phone',\
	 'complaint_phone', 'service_id', 'complaint_type_id', 'status_id']
	__attribute_serializer__ = dict(date_time='date')
	__object_class__ = Complaint

	def __init__(self, utc_offset=None):
		if utc_offset:
			self.__utc_offset__=utc_offset


class Service(db.Model):
	'''Service'''

	id=db.Column(db.Integer, primary_key=True)
	name=db.Column(db.String(20), unique=True)

	def __init__(self, name):
		self.name=name

class ServiceJsonSerializer(JsonSerializer):
	__attributes__=['id', 'name']
	__required__=['name']
	__attribute_serializer__=dict()
	__object_class__=Service
		
class ComplaintType(db.Model):
	'''ComplaintType'''
	
	id=db.Column(db.Integer, primary_key=True)
	name=db.Column(db.String(20), unique=True)
	service_id=db.Column(db.Integer, db.ForeignKey('service.id'))
	service=db.relationship('Service', backref=db.backref('complaint_types', lazy='dynamic'))
	
	def __init__(self, name, service_id):
		self.name=name
		self.service_id=service_id

class ComplaintTypeJsonSerializer(JsonSerializer):
	__attributes__=['id', 'name', 'service_id']
	__required__=['name', 'service_id']
	__attribute_serializer__=dict()
	__object_class__=ComplaintType
		
		
class ComplaintStatus(db.Model):
	'''ComplaintStatus'''
	
	id=db.Column(db.Integer, primary_key=True)
	name=db.Column(db.String(20), unique=True)

	def __init__(self, name):
		self.name=name

class ComplaintStatusJsonSerializer(JsonSerializer):
	__attributes__=['id', 'name']
	__required__=['name']
	__attribute_serializer__=dict()
	__object_class__=ComplaintStatus