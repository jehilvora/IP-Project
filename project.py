from flask import Flask, render_template, redirect, url_for, request, session
import os
import MySQLdb

#App initialization
app = Flask(__name__)
#Secret Key for session
app.secret_key = os.urandom(12)

#Database connection to database name 'online_judge'. Ensure user and password is same
db = MySQLdb.connect('localhost', 'root', 'root@123', 'online_judge')

# Route for handling login page
@app.route("/", methods=['GET'])
def home():
	#logged_in is the key in session variable for current login status
	if session.get("logged_in"):
		return redirect(url_for('homePage'))
	else:
		return render_template('login.html')

@app.route('/loginHandler', methods=['GET', 'POST'])
def loginHandler():
	#Login Database format
	#
	#+-------------+--------------+------+-----+---------+-------+
	#| Field       | Type         | Null | Key | Default | Extra |
	#+-------------+--------------+------+-----+---------+-------+
	#| register_no | varchar(10)  | NO   | PRI | NULL    |       |
	#| password    | varchar(256) | YES  |     | NULL    |       |
	#+-------------+--------------+------+-----+---------+-------+

	# Yet to add user addition functionality
	userName = request.form['uname']
	psw = request.form['psw']
	reqPsw = getSingleValue("select password from users where register_no = '%s'" % userName)
	if reqPsw != None and psw == reqPsw[0]:
			session['username'] = userName
			session['logged_in'] = True
			return redirect(url_for('homePage'))
	else:
		return "<h2>Invalid Username or Password</h2>"

@app.route("/homepage", methods=['GET'])
def homePage():
	return render_template("homepage.html")

@app.route("/logout", methods=['GET', 'POST'])
def logout():
	#set logged_in to false to remove user from session
	session.clear()
	return redirect(url_for('home'))


def getSingleValue(query):
	"""
		Returns a single tuple of data from database
		query : a mysql query for information
	"""
	cursor = db.cursor()
	cursor.execute(query)
	return cursor.fetchone()

if __name__ == "__main__":
	app.run(debug=True)