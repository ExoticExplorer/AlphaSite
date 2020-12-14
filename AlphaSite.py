from flask import Flask, redirect, url_for, render_template, flash, request, session
from flask_mysqldb import MySQL
from flask_socketio import SocketIO, send

app = Flask(__name__)

app.config['SECRET_KEY'] = 'c948da6e78e546046a326b8b03d3fc6e'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'rsj2003'
app.config['MYSQL_DB'] = 'flaskapp'

mysql = MySQL(app)
socketio = SocketIO(app)

@app.route('/')
@app.route('/join', methods=["GET", "POST"])
def join():
	if request.method == "POST":
		server_details = request.form
		name = server_details['name']
		password = server_details['password']
		server_type = server_details['server_type']
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM servers WHERE (name, password) = (%s, %s)", (name, password))
		if cur.fetchone():
			session["loggedIn"] = True
			return redirect(f'/{name}')
		else:
			flash("Name and password do not match, or the server does not exist")
			return render_template("join.html")
	return render_template("join.html")

@app.route('/create', methods=["GET", "POST"])
def create():
	if request.method == "POST":
		server_details = request.form
		name = server_details['name']
		password = server_details['password']
		server_type = server_details['server_type']
		cur = mysql.connection.cursor()
		if cur.execute("SELECT * FROM servers WHERE (name) = (%s)", [name]):
			flash("Server already exists")
			return render_template("create.html")
		else:
			cur.execute("INSERT INTO servers(Name, password, type) VALUES (%s, %s, %s)", (name, password, server_type))
			mysql.connection.commit()
			cur.close()
			flash("Server created succesfully")
			return redirect(f'/{name}')

	return render_template("create.html")

@app.route('/<page>', methods=["GET", "POST"])
def page(page):	
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM servers WHERE (name) = (%s)", [page])
	x = cur.fetchone()
	if x is None:
		return redirect(url_for("server_not_found"))
	if x[2] == "public":
		return render_template("page.html", page=page)
	if x[2] == "private":
		if "loggedIn" in session:
			return render_template("page.html", page=page)
		else:
			flash("server is private")
			return redirect(url_for("join"))


@app.route('/server_not_found')
def server_not_found():
	return render_template("server_not_found.html")

@socketio.on('message')
def handleMessage(msg):
	print('Message :' + msg)
	send(msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)
