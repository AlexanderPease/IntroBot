import urllib
import json
from mongo import db
import pymongo, logging

''' Returns all intros '''
def get_all():
	return list(db.introbot.find())

''' Returns intro from given id '''
def get_by_id(intro_id):
    return db.introbot.find_one({'id':intro_id})

''' Saves an intro to the database. Intro arg is a dict.
	Can be brand new or updating existing. '''
def save_intro(intro):
	if 'id' not in intro.keys() or intro['id'] == '':
	    # need to create a new intro id
	    intro['id'] = int(db.introbot.count() + 1)
	    print intro
	return db.introbot.update({'id':intro['id']}, intro, upsert=True)

def remove_intro(intro):
	if 'id' in intro.keys():
		return db.introbot.remove({'id':intro['id']})


