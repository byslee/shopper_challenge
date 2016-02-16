# shopper_challenge

Notes:

* Original starter code was a Rails app. I haven't used Ruby nor Rails in depth before. Gave it a try but ran into problems while trying to install Nokogiri, tried to fix it for ~1 hour.
* Decided to write app in Python/Flask from scratch and then integrate with any necessary parts from the starter app. (Since I am familiar with Python, and Flask is a lightweight framework so it's easy and fast to get it set up.)



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
TODO (if I had more time)
=============================

Running list of TODOs for myself

* Change text on pages to flashed messages

These are things that I know should be implemented, but there wasn't time to.

* Validate entries into form fields and raise error if not well-formed
* Use JavaScript & Ajax on funnel analytics to change chart without having to load a new page






