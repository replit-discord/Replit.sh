from flask import Flask, render_template, request, redirect, send_from_directory
from replit import db
import random, string, json, os, validators, logging

print_db_on_start = False
export_db_on_start = False
import_db_on_start = False

# Shortener Setup
url = "https://replit.sh/" # URL of Your Site
siteName = "Replit.sh" # Name of your Site

logging.basicConfig(filename='replitsh.log',level=logging.INFO) #if you replate INFO with DEBUGGING have fun saying goodbye to your db lol

if print_db_on_start:
	print(list(db.keys()))

if export_db_on_start:
	outdb = {}
	print("Starting DB Export...")
	for x in list(db.keys()):
		print("Set key " + str(x) + " to " + str(db[x]))
		outdb[x] = db[x]
	f = open('out.json', 'w')
	with open('out.json', 'w') as outfile:
		print("File opened...")
		json.dump(outdb, outfile)
		print("File written...")
		print("File closed...")

if import_db_on_start:
	print("Clearning old db")
	for x in list(db.keys()):
		print("Cleared key " + str(x))
		del db[x]
	print("Opening JSON File")
	with open("in.json", "r") as read_file:
		print("Converting JSON encoded data into Python dictionary")
		indb = json.load(read_file)
	print("Starting DB Import...")
	for key, value in indb.items():
		print ("Set key " + str(key) + " to " + str(value))
		db[key] = value
	print("Database imported")

users = json.loads(os.getenv("IDS"))

app = Flask('app')

##def statsCreate(id):

def fancyLog(path, type, returned, htmlCode):
	path = checkLogLength("| Path: {}".format(path))
	type = checkLogLength("| Type: {}".format(type))
	returned = checkLogLength("| Returned: {}".format(returned))
	print("+-------------------------------------------------------------------------------------------+")
	print("| API Request                                                                               |")
	print(path + "|")
	print(type + "|")
	print(returned + "|")
	print("| HTML Code: {}                                                                            |".format(str(htmlCode)))
	print("+-------------------------------------------------------------------------------------------+")

def checkLogLength(x):
	while len(x) < 92:
		x = x + " "
	return x

def newString():
	letters = string.ascii_lowercase
	result_str = ''.join(random.choice(letters) for i in range(8))
	return result_str

def getStrings(id):
	urls = db["user_id_" + id]
	return urls

def compileLine(id): # When passed the id for a short URL, returns a preformatted html table line
	return '<tr><td>' + id[10:] + '</td><td>' + db[id] + '</td><td>' + '<a href ="https://replit.sh/delete/' + id[10:] + '">Delete Entry</a></td><td><a href ="https://replit.sh/edit/' + id[10:] + '">Edit Entry</a></td></tr>'

@app.route('/')
def index():
	global siteName
	global users
	if not request.headers['X-Replit-User-Id']:
		fancyLog("/", "File", "templates/index.html", 200)
		return render_template(
		'index.html',
		siteName=siteName,
		user_id=request.headers['X-Replit-User-Id'],
		user_name=request.headers['X-Replit-User-Name'],
		user_roles=request.headers['X-Replit-User-Roles']
	)
	if len(request.headers['X-Replit-User-Id']) != 0 and int(request.headers['X-Replit-User-Id']) in users:
		fancyLog("/", "File", "templates/submit.html", 200)
		return render_template(
		'submit.html',
		siteName=siteName,
		user_id=request.headers['X-Replit-User-Id'],
		user_name=request.headers['X-Replit-User-Name'],
		error=""
	)
	elif len(request.headers['X-Replit-User-Id']) != 0 and int(request.headers['X-Replit-User-Id']) not in users:
		fancyLog("/", "File", "templates/error.html", 401)
		return render_template('error.html', code = "401", message = "You aren't an allowed user, sorry!", siteName=siteName)
	else:
		fancyLog("/", "File", "templates/index.html", 200)
		return render_template(
		'index.html',
		siteName=siteName,
		user_id=request.headers['X-Replit-User-Id'],
		user_name=request.headers['X-Replit-User-Name'],
		user_roles=request.headers['X-Replit-User-Roles']
	)

@app.route('/custom')
def custom():
	global siteName
	global users
	if not request.headers['X-Replit-User-Id']:
		fancyLog("/custom", "File", "templates/index.html", 200)
		return render_template(
		'index.html',
		siteName=siteName,
		user_id=request.headers['X-Replit-User-Id'],
		user_name=request.headers['X-Replit-User-Name'],
		user_roles=request.headers['X-Replit-User-Roles']
	)
	if len(request.headers['X-Replit-User-Id']) != 0 and int(request.headers['X-Replit-User-Id']) in users:
		fancyLog("/custom", "File", "templates/custom.html", 200)
		return render_template(
		'custom.html',
		siteName=siteName,
		user_id=request.headers['X-Replit-User-Id'],
		user_name=request.headers['X-Replit-User-Name'],
		error=""
	)
	elif len(request.headers['X-Replit-User-Id']) != 0 and int(request.headers['X-Replit-User-Id']) not in users:
		fancyLog("/custom", "File", "templates/error.html", 401)
		return render_template('error.html', code = "401", siteName=siteName, message = "You aren't an allowed user, sorry!")
	else:
		fancyLog("/custom", "File", "templates/index.html", 200)
		return render_template(
		'index.html',
		siteName=siteName,
		user_id=request.headers['X-Replit-User-Id'],
		user_name=request.headers['X-Replit-User-Name'],
		user_roles=request.headers['X-Replit-User-Roles']
	)

@app.route('/wp-login.php')
def wploginphp():
	global siteName
	fancyLog("/wp-login.php", "Redirect", "/dash", 302)
	return redirect(url + 'dash')

@app.route('/dash')
def dashboard():
	global siteName
	try:
		ids = getStrings(request.headers['X-Replit-User-Id'])
		idTable = ""
		for id in ids:
			idTable = idTable + compileLine(id)
		fancyLog("/dash", "File", "templates/dashboard.html", 200)
		return render_template(
			'dashboard.html',
			siteName=siteName,
			user_id=request.headers['X-Replit-User-Id'],
			user_name=request.headers['X-Replit-User-Name'],
			user_roles=request.headers['X-Replit-User-Roles'],
			idTable = idTable,
			error = ""
		)
	except:
		fancyLog("/dash", "File", "templates/dashboard.html", 200)
		return render_template(
			'dashboard.html',
			siteName=siteName,
			user_id=request.headers['X-Replit-User-Id'],
			user_name=request.headers['X-Replit-User-Name'],
			user_roles=request.headers['X-Replit-User-Roles'],
			idTable = idTable,
			error = "<p>No Entries Yet</p>"
		)

@app.route('/delete/<string:id>')
def delete(id):
	global siteName
	if not id:
		id = "Please stop trying to break the site lol"
	fancyLog("/delete/" + str(id), "File", "templates/delete.html", 200)
	return render_template(
		'delete.html',
		siteName=siteName,
		user_id=request.headers['X-Replit-User-Id'],
		user_name=request.headers['X-Replit-User-Name'],
		user_roles=request.headers['X-Replit-User-Roles'],
		id = id
	)

@app.route('/edit/<string:id>')
def edit(id):
	global siteName
	if not id:
		id = "Please stop trying to break the site lol"
	fancyLog("/edit/" + str(id), "File", "templates/edit.html", 200)
	return render_template(
		'edit.html',
		siteName=siteName,
		user_id=request.headers['X-Replit-User-Id'],
		user_name=request.headers['X-Replit-User-Name'],
		user_roles=request.headers['X-Replit-User-Roles'],
		oldurl = db["short_url_" + id],
		id = id
	)

@app.route('/del', methods=['POST'])
def deleteEntry():
	global siteName
	if len(request.headers['X-Replit-User-Id']) != 0 and int(request.headers['X-Replit-User-Id']) in users:
		user_id = request.headers['X-Replit-User-Id']
		id = request.form['id']
		users_ids = db["user_id_" + user_id]
		try:
			users_ids.remove("short_url_" + id)
			del db["short_url_" + id]
			db["user_id_" + user_id] = users_ids
			fancyLog("/del", "Redirect", "/dash", 302)
			return redirect(url + "dash", 302)
		except:
			fancyLog("/del", "File", "templates/error.html", 401)
			return render_template('error.html', code = "401", siteName=siteName, message = "You aren't allowed to do that!")
	else:
		fancyLog("/del", "File", "templates/error.html", 401)
		return render_template('error.html', code = "401", siteName=siteName, message = "You aren't allowed to do that!")

@app.route('/edt', methods=['POST'])
def editEntry():
	global siteName
	global url
	if len(request.headers['X-Replit-User-Id']) != 0 and int(request.headers['X-Replit-User-Id']) in users:
		user_id = request.headers['X-Replit-User-Id']
		id = request.form['id']
		newurl = request.form['newurl']
		try:
			db["short_url_" + id] = newurl
			fancyLog("/del", "Redirect", "/dash", 302)
			return redirect(url + "dash", 302)
		except:
			fancyLog("/edt", "File", "templates/error.html", 401)
			return render_template('error.html', code = "401", siteName=siteName, message = "You aren't allowed to do that!")
	else:
		fancyLog("/edt", "File", "templates/error.html", 401)
		return render_template('error.html', code = "401", siteName=siteName, message = "You aren't allowed to do that!")

@app.route('/favicon.ico')
def favicon():
	fancyLog("/favicon.ico", "File", "static/favicon.ico", 200)
	return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

@app.route('/sitemap.xml')
def sitemap():
	fancyLog("/sitemap.xml", "File", "static/sitemap.xml", 200)
	return send_from_directory(os.path.join(app.root_path, 'static'), 'sitemap.xml')

@app.route('/googlecec87f30263d281f.html')
def googleverifbsorwhatever():
	fancyLog("/googlecec87f30263d281f.html", "File", "static/googlecec87f30263d281f.html", 200)
	return send_from_directory(os.path.join(app.root_path, 'static'), 'googlecec87f30263d281f.html')

@app.route('/robots.txt')
def robots():
	fancyLog("/robots.txt", "File", "static/robots.txt", 200)
	return send_from_directory(os.path.join(app.root_path, 'static'), 'robots.txt')

@app.route('/humans.txt')
def humans():
	fancyLog("/humans.txt", "File", "static/humans.txt", 200)
	return send_from_directory(os.path.join(app.root_path, 'static'), 'humans.txt')

@app.route('/getid')
def getId():
	global siteName
	fancyLog("/getid", "File", "templates/getid.html", 200)
	return render_template(
		'getid.html',
		siteName=siteName,
		user_id=request.headers['X-Replit-User-Id'],
		user_name=request.headers['X-Replit-User-Name'],
		user_roles=request.headers['X-Replit-User-Roles']
	)

@app.route('/<string:key>', methods=['GET'])
def sendUrl(key):
	global siteName
	key = "short_url_" + key
	if not db[key]:
		fancyLog("/" + str(key), "File", "templates/error.html", 404)
		return render_template('error.html', code = "404", siteName=siteName, message = "That URL could not be found!")
	else:
		redirectUrl = db[key]
		fancyLog("/" + str(key), "Redirect", redirectUrl, 302)
		return redirect(redirectUrl, 302)

@app.route('/new', methods=['POST'])
def newEntry():
	global siteName
	if len(request.headers['X-Replit-User-Id']) != 0 and int(request.headers['X-Replit-User-Id']) in users:
		key = "short_url_" + newString()
		keys = list(db.keys())
		while key in keys:
			key = "short_url_" + newString()
			keys = list(db.keys())
		if not validators.url(str(request.form['url'])):
			fancyLog("/new", "File", "templates/submit.html", 400)
			return render_template(
				'submit.html',
				siteName=siteName,
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
		fancyLog("/new", "File", "templates/done.html", 200)
		return render_template('done.html', siteName=siteName, newUrl = url + key[10:])
	else:
		fancyLog("/new", "File", "templates/error.html", 401)
		return render_template('error.html', siteName=siteName, code = "401", message = "You aren't allowed to do that!")

@app.route('/newcustom', methods=['POST'])
def newCustom():
	global siteName
	if len(request.headers['X-Replit-User-Id']) != 0 and int(request.headers['X-Replit-User-Id']) in users:
		key = "short_url_" + request.form['id']
		keys = list(db.keys())
		if key in keys:
			return render_template('error.html', siteName=siteName, code = "401", message = "That ID Already Exists!")
		if not validators.url(str(request.form['url'])):
			fancyLog("/new", "File", "templates/manual.html", 400)
			return render_template(
				'manual.html',
				siteName=siteName,
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
		fancyLog("/newcustom", "File", "templates/done.html", 200)
		return render_template('done.html', siteName=siteName, newUrl = url + key[10:])
	else:
		fancyLog("/newcustom", "File", "templates/error.html", 401)
		return render_template('error.html', siteName=siteName, code = "401", message = "You aren't allowed to do that!")


@app.errorhandler(400)
def error_bad_request(e):
	global siteName
	fancyLog("Bad Request", "Error", "templates/error.html", 400)
	return render_template('error.html', siteName=siteName, code = "400", message = "Bad Request")

@app.errorhandler(401)
def error_unauthorized(e):
	global siteName
	fancyLog("Unauthorized", "Error", "templates/error.html", 401)
	return render_template('error.html', siteName=siteName, code = "401", message = "Unauthorized")

@app.errorhandler(403)
def error_forbidden(e):
	global siteName
	fancyLog("Forbidden", "Error", "templates/error.html", 403)
	return render_template('error.html', siteName=siteName, code = "403", message = "Forbidden")

@app.errorhandler(404)
def error_page_not_found(e):
	global siteName
	fancyLog("Page not Found", "Error", "templates/error.html", 404)
	return render_template('error.html', siteName=siteName, code = "404", message = "Page not Found")

@app.errorhandler(409)
def error_conflict(e):
	global siteName
	fancyLog("Conflict", "Error", "templates/error.html", 409)
	return render_template('error.html', siteName=siteName, code = "409", message = "Conflict")

@app.errorhandler(501)
def error_internal_server_error(e):
	global siteName
	fancyLog("Internal Server Error", "Error", "templates/error.html", 501)
	return render_template('error.html', siteName=siteName, code = "500", message = "Internal Server Error")

@app.errorhandler(501)
def error_not_implemented(e):
	global siteName
	fancyLog("Not Implemented", "Error", "templates/error.html", 501)
	return render_template('error.html', siteName=siteName, code = "501", message = "Not Implemented")

@app.errorhandler(502)
def error_bad_gateway(e):
	global siteName
	fancyLog("Bad Gateway", "Error", "templates/error.html", 502)
	return render_template('error.html', siteName=siteName, code = "502", message = "Bad Gateway")

app.run(host='0.0.0.0', port=8080)