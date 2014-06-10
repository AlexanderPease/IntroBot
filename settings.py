import os
import time
import tornado.options

# Environmenal settings for heroku#
# If you are developing for heroku and want to set your settings as environmental vars
# create settings_local_environ.py in the root folder and use:
# os.environ['KEY'] = 'value'
# to simulate using heroku config vars
# this is better than using a .env file and foreman
# since it still allows you to see logging.info() output.
# Make sure to also put import os in this settings_local_environ.py


try:
  import settings_local_environ
except:
  pass
  
time.tzset()

tornado.options.define("environment", default="dev", help="environment")
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__)))

options = {
  'dev' : {
    'mongo_database' : {'host' : os.environ.get('MONGODB_URL'), 'port' : 27017, 'db' : os.environ.get('DB_NAME')},
    'base_url' : os.environ.get('BASE_URL'),
  },
  'test' : {
    'mongo_database' : {'host' : os.environ.get('MONGODB_URL'), 'port' : 27017, 'db' : os.environ.get('DB_NAME')},
    'base_url' : os.environ.get('BASE_URL'),
  },
  'prod' : {
    'mongo_database' : {'host' : os.environ.get('MONGODB_URL'), 'port' : 27017, 'db' : os.environ.get('DB_NAME')},
    'base_url' : 'www.usv.com',
  },
  'production' : {
    'mongo_database' : {'host' : os.environ.get('MONGODB_URL'), 'port' : 27017, 'db' : os.environ.get('DB_NAME')},
    'base_url' : 'www.usv.com',
  }
}

default_options = {
  'active_theme': "default",
  'site_title': "IntroBot",
  'site_intro': "This is a website where people talk",
  'base_url': os.environ.get("BASE_URL"),
  
  'project_root': os.path.abspath(os.path.join(os.path.dirname(__file__))),

  # twitter details
  'twitter_consumer_key' : '',
  'twitter_consumer_secret' : '',

  # sendgrid details
  'sendgrid_user': os.environ.get("SENDGRID_USER"),
  'sendgrid_secret': os.environ.get("SENDGRID_SECRET"),

  # Your name and email, used in the IntroBot message
  'name': 'Test_Name', # Must be a single word, no spaces
  'email': 'john@test.com',

  # Twitter handles that can log in and use your IntroBot 
  'usernames':[
    os.environ.get("USERNAME"),
  ],

  
  'module_dir': os.path.join(PROJECT_ROOT, 'templates/modules')
}

def get(key):
  # check for an environmental variable (used w Heroku) first
  if os.environ.get('ENVIRONMENT'):
    env = os.environ.get('ENVIRONMENT')
  else:
    env = tornado.options.options.environment

  if env not in options:
    raise Exception("Invalid Environment (%s)" % env)

  if key == 'environment':
    return env

  v = options.get(env).get(key) or os.environ.get(key.upper()) or default_options.get(key)

  if callable(v):
    return v

  if v is not None:
    return v

  return default_options.get(key)
