# shopper_challenge

Notes:

* Original starter code was a Rails app. I haven't used Ruby nor Rails in depth before. Gave it a try but ran into problems while trying to install Nokogiri, tried to fix it for ~1 hour.
* Decided to write app in Python/Flask from scratch and then integrate with any necessary parts from the starter app. (Since I am familiar with Python, and Flask is a lightweight framework so it's easy and fast to get it set up.)
* Design decisions/tradeoffs noted at bottom of this doc
* Step-by-step instructions on how to run the app are below



=============================
GET MY CODE
=============================
$ git clone https://github.com/byslee/shopper_challenge.git  
$ cd shopper_challenge  

=============================
INSTALL FLASK (< 5 min)
=============================

More details at: http://flask.pocoo.org/docs/0.10/installation/#installation  

$ sudo pip install virtualenv  
Successfully installed virtualenv-14.0.6  

$ cd shopper_challenge  
$ virtualenv venv  
Installing setup tools, pip, wheel...done.  

$ . venv/bin/activate  
(venv) $ pip install Flask  
Successfully installed Flask-0.10.1 Jinja2-2.8 MarkupSafe-0.23 Werkzeug-0.11.4 itsdangerous-0.24  

=============================
SETUP DATABASE
=============================
$ cd shopper_challenge/app  
$ sqlite3 applicants.db < schema.sql  

=============================
RUN THE APP
=============================
$ cd shopper_challenge  
$ . venv/bin/activate  
(venv) $ cd app  
(venv) $ python run_app.py  
Go to localhost:5000 in browser

=============================
FUNNEL ANALYTICS
============================= 
$ cd shopper_challenge  
$ . venv/bin/activate  
(venv) $ cd app  
(venv) $ python run_app.py  
Go to localhost:5000/funnel_dashboard in browser 

To test with dummy data:  
$ cd shopper_challenge  
$ cd app  
$ sqlite3 applicants.db < schema.sql  
$ sqlite3 applicants.db < dummy.sql  
In the browser: Go to /funnel_dashboard and select dates from Dec 1 2014 to Dec 28 2014



=============================
Design Decisions
=============================

Funnel Analytics

* Fetch all records between start and end at once (only make 1 database call), store in memory, then perform group-by analysis using Python? OR, group into weeks in Python, make 1 database call for each week?
* Which one is faster? --> Depends on how costly making each call to the database is vs. how fast the group by is in Python versus SQL.
* I am not familiar enough with above to make a decision. I will default to using less database calls (I think it is faster, plus fewer reads = less potential for error) and processing all of the data in Python. I would guess there are maybe ~50K shopper applicants per year, Python should be able to handle that easily.

=============================
Outstanding TODOs
=============================

Master list in descending order of priority

* Fine tune the hero image & text on landing page. White subheading is hard to read. Tried putting translucent overlay under it but couldn't get it exactly right.
* Allow user to retrieve application status keyed off email
* Better validation messages -- highlighting the specific field that is missing, passing form data with redirect so that user doesn't have to re-type everything again
* Better funnel visualization
* Faster funnel query -- Python versus SQL
* Frontend validation of form fields on the application form & date picker on funnel dashboard - better UX: instead of notifying the user of mistake after they submit, prevent them from making the mistake in the first place

Nice to haves

* Use JavaScript & Ajax on funnel display to change chart without having to load a new page
* Progress bar on Shopper Applicant page to indicate where they are in the flow




