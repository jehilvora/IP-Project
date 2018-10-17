from flask import Flask, render_template, redirect, url_for, request, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(12)

# Route for handling login page
@app.route("/", methods=['GET'])
def home():
	if session.get("logged_in"):
		return redirect(url_for('homePage'))
	else:
		return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	userName = 'admin'
	if request.form['username'] == userName and request.form['password'] == 'password':
		session['username'] = userName
		session['logged_in'] = True
		return redirect(url_for('homePage'))
	else:
		return "<h2>Invalid ID</h2>"

@app.route("/homepage", methods=['GET'])
def homePage():
	return render_template("homepage.html")

if __name__ == "__main__":
	app.run(debug=True)