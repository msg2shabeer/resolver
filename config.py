# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# Define the database - we are working with
# SQLite for this example
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'resolver.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///resolver.db'
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = '\xdc\xd7\xab\xe8\xeb\x06\xb8\x7f5\xc7\xf4\xe3\xfa\xa6\xe4.\x1f\xcfTR.\xd8.K'

# Setting the modification tracking flag to true, mainly to disable the warning
SQLALCHEMY_TRACK_MODIFICATIONS=True

# Setting the timezone UTC Offset for serializing the date and time
UTC_OFFSET=dict(hours=5, minutes=30)


