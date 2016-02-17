import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
import datetime
import pdb
import json

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

def format_week_title(monday_date):      # takes a datetime object
	sunday_date = monday_date + datetime.timedelta(days=6)
	return monday_date.strftime('%Y-%m-%d') + '-' + sunday_date.strftime('%Y-%m-%d')


def get_funnel_json(start_date, end_date):

	data = {}

	# query constraints: compare created_at <= end_date, not updated_at <= end_date
	# because if we use updated_at, we'll miss counting those people who were updated more
	# recently than end_date, but actually joined during (start_date to end_date)
	query = 'select created_at, workflow_state from applicants where created_at >= ? and created_at <= ?'
	cur = g.db.execute(
		query,
		[
			start_date,
			end_date
		]
	)

	# hack: fill this out later to prevent problems with group by week (if we're missing dates)
	# gives sorted list of all dates between start date and end date
	all_dates = []
	current = datetime.datetime.strptime(start_date, '%Y-%m-%d')
	end = datetime.datetime.strptime(end_date, '%Y-%m-%d')
	while current <= end:
		all_dates.append(current)
		current = current + datetime.timedelta(days=1)

	# I haven't grouped by date because created_at stores datetime, not date
	# I'm not as familiar with SQL -- maybe there is an easy way around this
	# Below, group cohorts by date they started
	grouped_by_date = {}
	for date in all_dates:
		grouped_by_date[date] = {}
	for row in cur.fetchall():
		create_date = datetime.datetime.strptime(row[0], '%Y-%m-%d')
		workflow_state = row[1]
		if workflow_state not in grouped_by_date[create_date]:
			grouped_by_date[create_date][workflow_state] = 1
		else:
			grouped_by_date[create_date][workflow_state] += 1

	# print grouped_by_date

	# now group cohorts by the week in which they applied
	# simplifying assumptions given time constraints:
	# 	user selects start_date as Monday and end_date as Sunday
	current_week_title = ''
	current_week_contents = {}
	for day in all_dates:
		entry = grouped_by_date[day]
		# pdb.set_trace()
		if day.weekday() == 0:  # this is Monday
			# break off old week
			if len(current_week_title) > 0:
				data[current_week_title] = current_week_contents
			# start new week
			current_week_title = format_week_title(day)
			current_week_contents = {
				'applied': entry.get('applied', 0),
				'quiz_started': entry.get('quiz_started', 0),
				'quiz_completed': entry.get('quiz_completed', 0),
				'onboarding_requested': entry.get('onboarding_requested', 0),
				'onboarding_completed': entry.get('onboarding_completed', 0),
				'hired': entry.get('hired', 0),
				'rejected': entry.get('rejected', 0)
			}
		else:
			for key in entry:
				current_week_contents[key] += entry[key]

	# QUESTION about endpoints
	# Do we need to add backwards to create funnel? Or will that be handled by funnel visualization code?
	# ie. if current snapshot in time shows applied=5 and quiz_started=10 for a week
	# Should we should set applied = 15 = current # of applied + current # of quiz_started
	# otherwise the buckets give a distribution, not a funnel

	# TODO: dict is unordered -- how to fix?
	# 	Could store data as list of lists -- but then json.dumps() keeps it as a list, not dict
	return json.dumps(data)

@app.route('/funnel_dashboard')
def funnel_dashboard():
	return render_template('funnel_dashboard.html')

@app.route('/funnel_display', methods=['GET', 'POST'])
def funnel_display():
	# TODO: validation methods
	# 	Make sure that start_date < end_date
	# 	Make sure that start_date = Monday and end_date = Sunday (simplifying assumption given time constraints)
	start_date = request.form['start']
	end_date = request.form['end']
	funnel_data = get_funnel_json(start_date, end_date)
	return render_template('funnel_display.html', funnel_data=funnel_data)
	


##############################################
# RUN APP
##############################################


if __name__ == '__main__':
	app.run()