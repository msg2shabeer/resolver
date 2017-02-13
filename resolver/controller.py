import resolver
@resolver.app.route('/')
def hello_world():
	return 'Welcome to resolver'