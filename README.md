# shopper_challenge

Notes:

* Original starter code was a Rails app. I haven't used Ruby nor Rails in depth before. Gave it a try but ran into problems while trying to install Nokogiri, tried to fix it for ~1 hour.
* Decided to write app in Python/Flask from scratch and then integrate with any necessary parts from the starter app. (Since I am familiar with Python, and Flask is a lightweight framework so it's easy and fast to get it set up.)
* Design decisions/tradeoffs noted at bottom of this doc



=============================
GET MY CODE
=============================
$ git clone https://github.com/byslee/shopper_challenge.git  
$ cd shopper_challenge  

=============================
INSTALL FLASK (5 min)
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
Design Decisions
=============================

Funnel Analytics

* Fetch all records between start and end at once (only make 1 database call), store in memory, then perform group-by analysis using Python? OR, group into weeks in Python, make 1 database call for each week?
* Which one is faster? --> Depends on how costly making each call to the database is vs. how fast the group by is in Python versus SQL.
* I am not familiar enough with above to make a decision. I will default to using less database calls (I think it is faster, plus fewer reads = less potential for error) and processing all of the data in Python. I would guess there are maybe ~50K shopper applicants per year, Python should be able to handle that easily.

=============================
TODO & Design Notes
=============================

Running list of TODOs for myself

* Change text on pages to flashed messages
* Nice display for the funnel
* Backend validation for date picker on funnel: end_date > start_date

These are things that I know should be implemented, but there wasn't time to.

* Validate entries into form fields and raise error if not well-formed (front-end validation)
* Use JavaScript & Ajax on funnel analytics to change chart without having to load a new page
* Front-end validation for date picker on funnel

Nice-to-have: things I would do if I had unlimited time.

* Progress bar on Shopper Applicant page to indicate where they are in the flow.




