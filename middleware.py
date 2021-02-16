from werkzeug.wrappers import Request, Response, ResponseStream

class middleware():

	def __init__(self, app):
		self.app = app

	def __call__(self, environ, start_response):
		request = Request(environ)

		if request.headers['X-Replit-User-Id']:
			return self.app(environ, start_response)

		print("Authorization Failed")
		res = Response(u'Authorization failed', mimetype= 'text/plain', status=401)
		return res(environ, start_response)