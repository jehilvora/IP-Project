from flask import Flask, render_template, redirect, url_for, request, session
import os
import MySQLdb

#App initialization
app = Flask(__name__)
#Secret Key for session
app.secret_key = os.urandom(12)

#Database connection to database name 'online_judge'. Ensure user and password is same
db = MySQLdb.connect('localhost', 'root', 'root123', 'online_judge')

@app.route("/saveAndEvaluate/<int:problem_id>",methods=['GET','POST'])
def saveAndEvaluate(problem_id):
	cursor = db.cursor()
	code = request.form['code']
	cursor.execute("insert into submission values(0,'C','WA','','%s',%d) " % (session['username'],problem_id))
	sub_id=cursor.execute("select LAST_INSERT_ID()")
	filePath="./static/submissions/%s" % (session['username'])
	if not os.path.exists(filePath):
		os.makedirs(filePath)
	codeFile = open(filePath+'/%d.c' % (int(sub_id)),"w+")
	codeFile.write(code)
	codeFile.close()
	return code

@app.route("/editor/<int:problem_id>",methods=['GET','POST'])
def editor(problem_id):
	return render_template('Editor1.html',pid=problem_id)

# Route for handling login page
@app.route("/", methods=['GET'])
def home():
	messages = request.args.get('messages')
	#logged_in is the key in session variable for current login status
	if session.get("logged_in"):
		return redirect(url_for('dashboard'))
	else:
		return render_template('login.html', messages = messages)

@app.route("/signUpHandler", methods=['GET', 'POST'])
def signUpHandler():
	#Add a new User to the database. Currently storing passwords as plain-text. Will substitute for sha256.
	userName = request.form['uname']
	psw = request.form['psw']
	cursor = db.cursor()
	# Retrieve all users
	userData = getAllValues("select register_no from users")
	userData = [x[0] for x in userData]
	messages = None
	# Check for new user in current users
	if userName not in userData:
		cursor.execute("insert into users values ('%s','%s')" % (userName, psw))
		db.commit()
	else:
		messages = "User already exists"
	return redirect(url_for('home', messages = messages))

@app.route('/loginHandler', methods=['GET', 'POST'])
def loginHandler():
	userName = request.form['uname']
	psw = request.form['psw']
	reqPsw = getSingleValue("select password from users where register_no = '%s'" % userName)
	if reqPsw != None and psw == reqPsw[0]:
			session['username'] = userName
			session['logged_in'] = True
			return redirect(url_for('dashboard'))
	else:
		return render_template('login.html', messages="Wrong username or password")

@app.route("/dashboard", methods=['GET'])
def dashboard():
	return render_template("dashboard.html")

@app.route("/problems/<category>", methods=['GET'])
def problems(category):
	# Get all problems under given category
	problems = getAllValues("select problem_name from problem where category_name = '%s'" % category)
	return render_template("problems.html", problems = problems)

@app.route("/singleProblem/<problem_name>")
def singleProblem(problem_name):
	# Get information for single problem
	problemInfo = getSingleValue("select * from problem where problem_name = '%s'" % problem_name)
	return render_template("singleProblem.html", problemInfo = problemInfo)


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

def getAllValues(query):
	"""
		Returns a single tuple of data from database
		query : a mysql query for information
	"""
	cursor = db.cursor()
	cursor.execute(query)
	return cursor.fetchall()

if __name__ == "__main__":
	app.run(debug=True)