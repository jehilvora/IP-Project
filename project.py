from flask import Flask, render_template, redirect, url_for, request, session
import os
import subprocess
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
	sub_id = request.args.get('sub_id')
	filePath="./static/submissions/%s/%s.c" % (session['username'],sub_id)
	code = ""
	#os.chdir(filePath)
	if os.path.exists(filePath):
		codeFile = open(filePath,"r")
		code = codeFile.read()
		codeFile.close()
	return render_template('editor.html', pid=problem_id , code = code)

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
	problem_data = getAllValues("select problem_name,p.problem_id,sum(case when Status != 'NULL' then 1 else 0 end) allsubs,sum(case when Status = 'AC' then 1 else 0 end) success from problem as p LEFT JOIN submission as s on s.problem_id=p.problem_id group by s.problem_id order by p.problem_id")
	return render_template("problems.html", problem = problem_data)

@app.route("/singleProblem/<problem_name>")
def singleProblem(problem_name):
	# Get information for single problem
	problemInfo = getSingleValue("select * from problem where problem_name = '%s'" % problem_name)
	get_status = getSingleValue("select count(*) from submission as s,problem as p where problem_name = '%s' and p.problem_id=s.problem_id and Status='AC' and register_no='%s' " % (problem_name,session['username']))
	if get_status[0]>0:
		status="True"
	else:
		status="False"
	return render_template("singleProblem.html", problemInfo = problemInfo , status = status)

@app.route("/singleProblem/<problem_name>/mySubmissions")
def mySubmissions(problem_name):
	submissions=getAllValues("select sub_id,Status,register_no,s.problem_id,problem_name from submission as s,problem as p where s.problem_id = p.problem_id and problem_name = '%s' and register_no = '%s'" % (problem_name,session['username']))
	return render_template("mySubmissions.html", submissions = submissions , problem_name = problem_name)

@app.route("/singleProblem/<problem_name>/allSubmissions")
def allSubmissions(problem_name):
	submissions=getAllValues("select sub_id,Status,register_no,s.problem_id,problem_name from submission as s,problem as p where s.problem_id = p.problem_id and problem_name = '%s'" % (problem_name))
	return render_template("allSubmissions.html", submissions = submissions)

@app.route("/logout", methods=['GET', 'POST'])
def logout():
	#set logged_in to false to remove user from sessioname
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