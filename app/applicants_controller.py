import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
import datetime
import pdb

# config
DATABASE = 'applicants.db'
DEBUG = True
SECRET_KEY = 'y0s#$t0m0'
USERNAME = 'admin'   # TODO: allow more than 1 user
PASSWORD = 'd0n@t3ll@'  # TODO: allow more than 1 user


app = Flask(__name__)
app.config.from_object(__name__)


##############################################
# DATABASE FUNCTIONS
# Open connection to DB before each request
# Close after each request
##############################################

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

# def init_db():
# 	with closing(connect_db()) as db:
# 		with app.open_resource('schema.sql', mode='r') as f:
# 			db.cursor().executescript(f.read())
# 		db.commit()

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()


##############################################
# SUBMIT APPLICANT INFO
# Forms for applicant to fill out info
##############################################

@app.route('/')
def landing_page():
	session['logged_in'] = True  # TODO: change this to pick the specific user
	return render_template('landing_page.html')

@app.route('/start', methods=['POST'])
def start_app():
	pdb.set_trace()
	query = 'insert into applicants (first_name, last_name, region, phone, email, phone_type, source, over_21, reason, workflow_state, created_at, updated_at) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
	g.db.execute(
		query,
		[
			request.form['first-name'],
			request.form['last-name'],
			request.form['region'],
			request.form['phone'],
			request.form['email'],
			None,
			request.form['source'],
			None,
			None,
			'started',
			str(datetime.datetime.now()),
			str(datetime.datetime.now())
		]
	)
	g.db.commit()
	flash('Successfully started application!')
	return redirect(url_for('background_check'))

@app.route('/background')
def background_check():
	return render_template('background_check.html')

@app.route('/authorize_bg', methods=['POST'])
def authorize_bg():
	# pdb.set_trace()
	if request.form.get('authorize', None):
		return redirect(url_for('confirmation_page'))
	else:
		flash('Please authorize a background check in order to proceed')
		return redirect(url_for('background_check'))

@app.route('/confirmation')
def confirmation_page():
	return render_template('confirmation_page.html')


##############################################
# LOGIN AND LOGOUT
# Don't need to authenticate with password
# But store session based on user's email
##############################################



##############################################
# RUN APP
##############################################


if __name__ == '__main__':
	app.run()