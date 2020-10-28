from flask import Flask, render_template, request, redirect, send_from_directory
from replit import db
import random, string, json, os, validators

# Debugging Flags
print_db_on_start = False


# Shortener Setup
url = "https://replit.sh/"

if print_db_on_start:
	print(list(db.keys()))

with open('ids.json') as f:
	users = json.load(f)

app = Flask('app')

def newString():
	letters = string.ascii_lowercase
	result_str = ''.join(random.choice(letters) for i in range(8))
	return result_str

def getStrings(id):
	urls = db["user_id_" + id]
	return urls

def compileLine(id): # When passed the id for a short URL, returns a preformatted html table line
	url = db[id]
	return '<tr><td>' + id[10:] + '</td><td>' + url + '</td><td>' + '<a href ="https://replit.sh/delete/' + id[10:] + '">Delete Entry</a></td></tr>'

@app.route('/')
def index():
	global users
	if len(request.headers['X-Replit-User-Id']) != 0 and int(request.headers['X-Replit-User-Id']) in users:
		return render_template(
		'submit.html',
		user_id=request.headers['X-Replit-User-Id'],
		user_name=request.headers['X-Replit-User-Name'],
		error=""
	)
	elif len(request.headers['X-Replit-User-Id']) != 0 and int(request.headers['X-Replit-User-Id']) not in users:
		return render_template('error.html', code = "401", message = "You aren't an allowed user, sorry!")
	else:
		return render_template(
		'index.html',
		user_id=request.headers['X-Replit-User-Id'],
		user_name=request.headers['X-Replit-User-Name'],
		user_roles=request.headers['X-Replit-User-Roles']
	)

@app.route('/dash')
def dashboard():
	try:
		ids = getStrings(request.headers['X-Replit-User-Id'])
		idTable = ""
		for id in ids:
			idTable = idTable + compileLine(id)
		return render_template(
			'dashboard.html',
			user_id=request.headers['X-Replit-User-Id'],
			user_name=request.headers['X-Replit-User-Name'],
			user_roles=request.headers['X-Replit-User-Roles'],
			idTable = idTable,
			error = ""
		)
	except:
		return render_template(
			'dashboard.html',
			user_id=request.headers['X-Replit-User-Id'],
			user_name=request.headers['X-Replit-User-Name'],
			user_roles=request.headers['X-Replit-User-Roles'],
			idTable = idTable,
			error = "<p>No Entries Yet</p>"
		)

@app.route('/delete/<string:id>')
def delete(id):
	if not id:
		id = "Please stop trying to break the site lol"
	return render_template(
		'delete.html',
		user_id=request.headers['X-Replit-User-Id'],
		user_name=request.headers['X-Replit-User-Name'],
		user_roles=request.headers['X-Replit-User-Roles'],
		id = id
	)

@app.route('/del', methods=['POST'])
def deleteEntry():
	if len(request.headers['X-Replit-User-Id']) != 0 and int(request.headers['X-Replit-User-Id']) in users:
		user_id = request.headers['X-Replit-User-Id']
		id = request.form['id']
		users_ids = db["user_id_" + user_id]
		try:
			users_ids.remove("short_url_" + id)
			del db["short_url_" + id]
			db["user_id_" + user_id] = users_ids
			return redirect(url + "dash", 302)
		except:
			return render_template('error.html', code = "401", message = "You aren't allowed to do that!")
	else:
		return render_template('error.html', code = "401", message = "You aren't allowed to do that!")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'sitemap.xml')

@app.route('/robots.txt')
def robots():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'robots.txt')

@app.route('/humans.txt')
def humans():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'humans.txt')

@app.route('/getid')
def getId():
    return render_template(
		'getid.html',
		user_id=request.headers['X-Replit-User-Id'],
		user_name=request.headers['X-Replit-User-Name'],
		user_roles=request.headers['X-Replit-User-Roles']
	)

@app.route('/<string:key>', methods=['GET'])
def sendUrl(key):
	key = "short_url_" + key
	if not db[key]:
		return render_template('error.html', code = "404", message = "That URL could not be found!")
	else:
		return redirect(db[key], 302)

@app.route('/new', methods=['POST'])
def newEntry():
	if len(request.headers['X-Replit-User-Id']) != 0 and int(request.headers['X-Replit-User-Id']) in users:
		key = "short_url_" + newString()
		keys = list(db.keys())
		while key in keys:
			key = "short_url_" + newString()
			keys = list(db.keys())
		if not validators.url(str(request.form['url'])):
			return render_template(
				'submit.html',
				user_id=user,
				user_name=request.headers['X-Replit-User-Name'],
				error="That was not a valid URL. Please enter a valid URL and try again."
			)
		db[key] = request.form['url']
		try:
			strings = list(getStrings(request.headers['X-Replit-User-Id']))
		except:
			strings = []
		strings.append(key)
		db["user_id_" + request.headers['X-Replit-User-Id']] = strings
		return render_template('done.html', newUrl = url + key[10:])
	else:
		return render_template('error.html', code = "401", message = "You aren't allowed to do that!")

@app.errorhandler(400)
def error_bad_request(e):
	return render_template('error.html', code = "400", message = "Bad Request")

@app.errorhandler(401)
def error_unauthorized(e):
	return render_template('error.html', code = "401", message = "Unauthorized")

@app.errorhandler(403)
def error_forbidden(e):
	return render_template('error.html', code = "403", message = "Forbidden")

@app.errorhandler(404)
def error_page_not_found(e):
	return render_template('error.html', code = "404", message = "Page not Found")

@app.errorhandler(409)
def error_conflict(e):
	return render_template('error.html', code = "409", message = "Conflict")

@app.errorhandler(500)
def error_internal_server_error(e):
	return render_template('error.html', code = "500", message = "Internal Server Error")

@app.errorhandler(501)
def error_not_implemented(e):
	return render_template('error.html', code = "501", message = "Not Implemented")

@app.errorhandler(502)
def error_bad_gateway(e):
	return render_template('error.html', code = "502", message = "Bad Gateway")

app.run(host='0.0.0.0', port=8080)