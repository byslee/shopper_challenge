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
	# pdb.set_trace()
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
# FUNNEL ANALYTICS
##############################################


def get_funnel_json(start_date, end_date):

	# TODO: modify this query
	# group by date and sum
	# select between created_at and updated_at
	# order by date -- do this in Python or SQL


	query = 'select created_at, workflow_state from applicants where created_at >= ' + start_date + ' and updated_at <= ' + end_date + ') order by workflow_state'
	cur = g.db.execute(query)
	for row in cur.fetchall():
		# do pdb to check what format this is returned in
		print row


	# group cohorts by the week in which they applied
	# remember to add backwards to create funnel:
	# ie. if snapshot shows applied=5 and quiz_started=10
	# we should set applied = 15 = current # of applied + current # of quiz_started

	# break the time period into weeks
	# simplifying assumption given time constraints:
	# 	user selects start_date as Monday and end_date as Sunday
	#	ie. we discard the periods at end and beginning if they aren't a full week

	# weeks = {}

	# start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
	# end = datetime.datetime.strptime(end_date, '%Y-%m-%d')

	# current_week_title = ''
	# current_week_contents = {
	# 	'applied': 0,
	# 	'quiz_started': 0,
	# 	'quiz_completed': 0,
	# 	'onboarding_requested': 0,
	# 	'onboarding_completed': 0,
	# 	'hired': 0,
	# 	'rejected': 0
	# }

	# for row in results:
	# 	date_created = row[0]   # TODO: convert to datetime
	# 	if date_created.weekday() == 0:
	# 		# this is Monday. break off a new week.
	# 		current_week_title = # set this
	# 		current_week_contents = # clear and reset
	# 	else:
	# 		# add to the existing week.
	# 		current_week_contents = # update this based on whatever workflow state is

	data = {}
	# data = {
	#     "2014-12-01-2014-12-07": {
	#         "applied": 100,
	#         "quiz_started": 50,
	#         "quiz_completed": 20,
	#         "onboarding_requested": 10,
	#         "onboarding_completed": 5,
	#         "hired": 1,
	#         "rejected": 0
	#     },
	#     "2014-12-08-2014-12-14": {
	#         "applied": 200,
	#         "quiz_started": 75,
	#         "quiz_completed": 50,
	#         "onboarding_requested": 20,
	#         "onboarding_completed": 10,
	#         "hired": 5,
	#         "rejected": 0
	#     },
	#     "2014-12-15-2014-12-21": {
	#         "applied": 70,
	#         "quiz_started": 20,
	#         "quiz_completed": 10,
	#         "onboarding_requested": 0,
	#         "onboarding_completed": 0,
	#         "hired": 0,
	#         "rejected": 0
	#     },
	#     "2014-12-22-2014-12-28": {
	#         "applied": 40,
	#         "quiz_started": 20,
	#         "quiz_completed": 15,
	#         "onboarding_requested": 5,
	#         "onboarding_completed": 1,
	#         "hired": 1,
	#         "rejected": 0
	#     }
	# }
	return data

@app.route('/funnel_dashboard')
def funnel_dashboard():
	return render_template('funnel_dashboard.html')

@app.route('/funnel_display', methods=['GET', 'POST'])
def funnel_display():
	start_date = request.form['start']
	end_date = request.form['end']
	funnel_data = get_funnel_json(start_date, end_date)
	funnel_data = {}
	return render_template('funnel_display.html', funnel_data=funnel_data)
	


##############################################
# RUN APP
##############################################


if __name__ == '__main__':
	app.run()