from flask import Flask, render_template, redirect, url_for, request, session
import os
import subprocess
import MySQLdb
import matplotlib.pyplot as plt

#App initialization
app = Flask(__name__)
#Secret Key for session
app.secret_key = os.urandom(12)

#Database connection to database name 'online_judge'. Ensure user and password is same
db = MySQLdb.connect('localhost', 'root', 'root123', 'online_judge')

@app.route("/saveAndEvaluate/<int:problem_id>",methods=['GET','POST'])
def saveAndEvaluate(problem_id):
	programStatus = "Accepted!"
	problem_name = getSingleValue("select problem_name from problem where problem_id = %d" % problem_id)[0]
	cursor = db.cursor()
	code = request.form['code']
	cursor.execute("insert into submission values(0,'C','WA','%s',%d,NOW()) " % (session['username'],problem_id))
	sub_id = getSingleValue("select max(sub_id) from submission")[0]
	db.commit()
	sub_id = int(sub_id)
	filePath="C:/IP-Project/static/submissions/%s" % (session['username'])
	if not os.path.exists(filePath):
		os.makedirs(filePath)
	codeFile = open(filePath+'/%d.c' % ((sub_id)),"w+")
	codeFile.write(code)
	codeFile.close()
	os.chdir(filePath)
	status=subprocess.call("gcc %d.c -o %d" % (sub_id,sub_id),shell=True)
	if status:
		os.chdir("C:\IP-Project")
		cursor.execute("update submission set Status='CE' where sub_id = %d" % sub_id)
		programStatus = "Compilation Error!"
	else:
		output=subprocess.check_output("%d.exe < C:\IP-Project\static\problems\%d.txt" % (sub_id,problem_id), shell=True)
		os.chdir("C:\IP-Project\static\problems")
		subprocess.call("gcc %d.c -o %d" % (problem_id,problem_id),shell=True)
		expected_output=subprocess.check_output("%d.exe < C:\IP-Project\static\problems\%d.txt" % (problem_id, problem_id), shell=True)
		if output!=expected_output:
			os.chdir("C:\IP-Project")		
			programStatus = "Wrong Answer!"	
		else:
			cursor.execute("update submission set Status='AC' where problem_id=%d and register_no='%s' and sub_id=%d" % (problem_id,session['username'],sub_id))
			os.chdir("C:\IP-Project")
		db.commit()
	return redirect(url_for('mySubmissions', problem_name = problem_name, programStatus = programStatus))

@app.route("/editor/<int:problem_id>",methods=['GET','POST'])
def editor(problem_id):
	sub_id = request.args.get('sub_id')
	filePath="C:/IP-Project/static/submissions/%s/%s.c" % (session['username'],sub_id)
	code = ""
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
	userInfo = getSingleValue("select * from users where register_no = '%s'" % session['username'])
	stats = getSingleValue("select sum(case when Status='AC' then 1 else 0 end), sum(case when Status='WA' then 1 else 0 end), sum(case when Status='CE' then 1 else 0 end) from submission where register_no = '%s'" % session['username'])
	activity = getAllValues("select problem_name,Language,time,Status from submission s, problem p where p.problem_id=s.problem_id and register_no = '%s' order by time desc limit 5" % session['username'])
	stats = [x if x != None else 0 for x in stats]
	if stats != None:
		plt.clf()
		plt.pie(stats, labels=('AC','WA','CE'), autopct='%1.1f%%')
		plt.title('Submission Statistics')
		plt.savefig('C:\IP-Project\static\img\%s.png' % session['username'])
	return render_template("profile.html", userInfo = userInfo, stats = stats, activity = activity)

@app.route("/about", methods=['GET'])
def about():
	return render_template("about.html")

@app.route("/signUpHandler", methods=['GET', 'POST'])
def signUpHandler():
	#Add a new User to the database. Currently storing passwords as plain-text. Will substitute for sha256.
	userName = request.form['uname']
	psw = request.form['psw']
	register_no = request.form['regno']
	email = request.form['email']
	desc = request.form['desc']
	cursor = db.cursor()
	# Retrieve all users
	userData = getAllValues("select register_no from users")
	userData = [x[0] for x in userData]
	messages = None
	# Check for new user in current users
	if userName not in userData:
		cursor.execute("insert into users values ('%s','%s','%s','%s','%s')" % (register_no, psw, email, userName, desc))
		db.commit()
	else:
		messages = "User already exists"
	return redirect(url_for('home', messages = messages))

@app.route('/loginHandler', methods=['GET', 'POST'])
def loginHandler():
	register_no = request.form['regno']
	psw = request.form['psw']
	reqPsw = getSingleValue("select password from users where register_no = '%s'" % register_no)
	if reqPsw != None and psw == reqPsw[0]:
			session['username'] = register_no
			session['logged_in'] = True
			return redirect(url_for('dashboard'))
	else:
		return render_template('login.html', messages="Wrong username or password")

@app.route("/dashboard", methods=['GET'])
def dashboard():
	return render_template("dashboard.html")

@app.route("/lab", methods = ['GET' , 'POST'])
def lab():
	categories = getAllValues("select name from category")
	return render_template('lab.html', categories = categories)


@app.route("/problems/<category>", methods=['GET'])
def problems(category):
	problem_data = getAllValues("select problem_name,p.problem_id,sum(case when Status != 'NULL' then 1 else 0 end) allsubs,sum(case when Status = 'AC' then 1 else 0 end) success from problem as p LEFT JOIN submission as s on s.problem_id=p.problem_id where p.category_name='%s' group by p.problem_id order by p.problem_id" % category)
	tags = [x[0] for x in getAllValues("select * from problem_tags")]
	return render_template("problems.html", problem = problem_data, tags = tags)

@app.route("/singleProblem/<problem_name>")
def singleProblem(problem_name):
	# Get information for single problem
	problemInfo = getSingleValue("select * from problem where problem_name = '%s'" % problem_name)
	get_status = getSingleValue("select count(*) from submission as s,problem as p where problem_name = '%s' and p.problem_id=s.problem_id and Status='AC' and register_no='%s' " % (problem_name,session['username']))
	description=""
	filePath="C:/IP-Project/static/problemStatement/%d.txt" % (problemInfo[0])
	if os.path.exists(filePath):
		descriptionFile = open(filePath,"r")
		description = descriptionFile.read()
		print("desc"+description)
		descriptionFile.close()
	if get_status[0]>0:
		status="True"
	else:
		status="False"
	return render_template("singleProblem.html", problemInfo = problemInfo , status = status , problemStatement = description)

@app.route("/singleProblem/<problem_name>/mySubmissions")
def mySubmissions(problem_name):
	programStatus = request.args.get('programStatus')
	submissions=getAllValues("select sub_id,Status,register_no,s.problem_id,problem_name,time from submission as s,problem as p where s.problem_id = p.problem_id and problem_name = '%s' and register_no = '%s' order by time desc" % (problem_name,session['username']))
	flag="M"
	return render_template("submissions.html", submissions = submissions , problem_name = problem_name , flag = flag, programStatus = programStatus)

@app.route("/singleProblem/<problem_name>/allSubmissions")
def allSubmissions(problem_name):
	submissions=getAllValues("select sub_id,Status,register_no,s.problem_id,problem_name,time from submission as s,problem as p where s.problem_id = p.problem_id and problem_name = '%s' order by time desc" % (problem_name))
	flag="A"
	return render_template("submissions.html", submissions = submissions , flag = flag)

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