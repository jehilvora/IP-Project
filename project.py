from flask import Flask, render_template, redirect, url_for, request, session
import os
import subprocess
import MySQLdb

#App initialization
app = Flask(__name__)
#Secret Key for session
app.secret_key = os.urandom(12)

#Database connection to database name 'online_judge'. Ensure user and password is same
db = MySQLdb.connect('localhost', 'root', 'root@123', 'online_judge')

@app.route("/saveAndEvaluate/<int:problem_id>",methods=['GET','POST'])
def saveAndEvaluate(problem_id):
	cursor = db.cursor()
	code = request.form['code']
	cursor.execute("insert into submission values(0,'C','WA','','%s',%d) " % (session['username'],problem_id))
	sub_id = getSingleValue("select max(sub_id) from submission")[0]
	db.commit()
	sub_id = int(sub_id)
	filePath="./static/submissions/%s" % (session['username'])
	if not os.path.exists(filePath):
		os.makedirs(filePath)
	codeFile = open(filePath+'/%d.c' % ((sub_id)),"w+")
	codeFile.write(code)
	codeFile.close()
	os.chdir(filePath)
	status=subprocess.call("gcc %d.c -o %d" % (sub_id,sub_id),shell=True)
	if status:
		os.chdir("C:\IP-Project")
		return "compilation error"
	output=subprocess.check_output("%d" % sub_id)
	os.chdir("C:\IP-Project\static\problems")
	subprocess.call("gcc %d.c -o %d" % (problem_id,problem_id),shell=True)
	expected_output=subprocess.check_output("%d" % problem_id)
	if output!=expected_output:
		os.chdir("C:\IP-Project")		
		return "Wrong Output"	
	cursor.execute("update submission set Status='AC' where problem_id=%d and register_no='%s' and sub_id=%d" % (problem_id,session['username'],sub_id))
	db.commit()
	os.chdir("C:\IP-Project")
	return "Successful Submission"

@app.route("/editor/<int:problem_id>",methods=['GET','POST'])
def editor(problem_id):
	return render_template('editor.html',pid=problem_id)

# Route for handling login page
@app.route("/", methods=['GET'])
def home():
	messages = request.args.get('messages')
	#logged_in is the key in session variable for current login status
	if session.get("logged_in"):
		return redirect(url_for('dashboard'))
	else:
		return render_template('login.html', messages = messages)

@app.route("/profile", methods=['GET'])
def profile():
	return render_template("profile.html")

@app.route("/about", methods=['GET'])
def about():
	return render_template("about.html")

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
	problem_submissions = getAllValues("select count(*) from submission group by problem_id")
	correct_submissions = getAllValues("select count(*) from submission where Status = 'AC' group by problem_id")
	accuracy = []
	problem_submissions = [x[0] for x in problem_submissions]
	correct_submissions = [x[0] for x in correct_submissions]
	for x,y in zip(problem_submissions,correct_submissions):
		accuracy.append("%.2f" % ((y*100)/x))
	length=len(problem_submissions)
	print(length)
	get_status=getAllValues("select count(*) from submission where Status = 'AC' and register_no = %s group by problem_id" % session['username'])
	get_status = [x[0] for x in get_status]
	status = []
	for a in get_status:
		if a>0:
			status.append("True")
		else:
			status.append("False")
	return render_template("problems.html", problem = problems , acc = accuracy , sub = problem_submissions , status = status , len = length)

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