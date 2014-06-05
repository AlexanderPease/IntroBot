IntroBot
=================

Simple web app for automating two-way email introductions


Setup
======

Prior to installation, you'll need to do a few things:

* _Twitter_: Log into http://dev.twitter.com and set up a new application.  Note the "consumer key" and "consumer secret", which we'll need later on.
* Sign up for an account at http://sendgrid.com for email delivery


Configuration
-------------

General app settings are controlled via the settings.py file. You will need to provide dev/local values for the following settings:

* 'twitter_consumer_key' : '',
* 'twitter_consumer_secret' : '',
* 'sendgrid_user': '',
* 'sendgrid_secret': '',

Installation
------------

* start a local instance of mongo

./mongod

* OR, configure your app to use a cloud-based mongo instance, by setting "MONGODB_URL" and "DB_NAME" in settings.py

* Start the web server:

python tornado_server.py

* Site should be viewable at http://localhost:8001

Heroku Installation
-------------------
* The easiest way to get this working is to download the repo and push it to a Heroku instance. Get a MongoDB database using either MongoLab or MongoHQ. Heroku will automatically put your DB credentials into Heroku config; if you want to do any development locally, just creating a local_settings.py file that sets the same variables using os.environ['var_name']. 


Technology
===========

Built with:

 * Python / [Tornado](http://tornadoweb.org)
 * [Mongodb](http://www.mongodb.com/)
 * [Twitter](http://dev.twitter.com)
 * [Sendgrid](http://sendgrid.com/docs/API_Reference/)
