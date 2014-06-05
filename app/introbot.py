import app.basic
import tornado.web
import settings
import datetime
from lib import introdb
import requests

###########################
### Creates the initial intro email
### /
###########################
class Index(app.basic.BaseHandler):
	#@tornado.web.authenticated
	def get(self):
		#print self.current_user
		sent = self.get_argument('sent', '')
		err = self.get_argument('err', '')

		# Form fields
		to_name = self.get_argument('to_name', '')
		to_email = self.get_argument('to_email', '')
		for_name = self.get_argument('for_name', '')
		for_email = self.get_argument('for_email', '')
		purpose = self.get_argument('purpose', '')
		form = {'to_name': to_name, 'to_email': to_email, 'for_name': for_name, 'for_email': for_email, 'purpose': purpose}

		self.render('index.html', form=form, err=err, sent=sent)

	# If form is submitted correctly, send initial email
	#@tornado.web.authenticated
	def post(self):
		# Get submitted form data
		to_name = self.get_argument('to_name', '')
		to_email = self.get_argument('to_email', '')
		for_name = self.get_argument('for_name', '')
		for_email = self.get_argument('for_email', '')
		purpose = self.get_argument('purpose', '')
		intro = {'to_name': to_name, 'to_email': to_email, 'for_name': for_name, 'for_email': for_email, 'purpose': purpose}

		# TODO: Server side error handling? 

		# Save intro to database
		try:
			intro['sent_initial'] = datetime.datetime.now()
			introdb.save_intro(intro)
		except:
			return self.redirect('brittbot?err=%s' % 'Failed to save file to database. Email was not sent.')

		# Send initial email
		try:
			name = settings.get('name')
			email = settings.get('email')
			subject = "Intro to %s?" % intro['for_name']
			response_url = "%s/response" % settings.get('base_url')
			if "http://" not in response_url:
				response_url = "http://" + response_url
			text_body = 'Hi %s, %s wants to meet with you to %s If you are open to the connection please email reply to brittany@usv.com. This will automatically generate an email from brittany@usv.com to connect the two of you. Thanks! Brittany' % (intro['to_name'], intro['for_name'], intro['purpose'])
			html_body = 'Hi %s,<br><br> %s wants to meet with you to %s <br><br>If you are open to the connection please <a href="%s?id=%s">click here</a>. This will automatically generate an email from %s to connect the two of you. <br><br> Thanks! %s' % (intro['to_name'], intro['for_name'], intro['purpose'], response_url, intro['id'], email, name)
			response = self.send_email(name, intro['to_email'], subject, text_body, html_body, from_name=name)
			if response.status_code != 200:
				raise Exception 
			return self.redirect('?sent=%s (%s)' % (intro['to_name'], intro['to_email'])) # Always redirect after successful POST
		except:
			introdb.remove_intro(intro)
			return self.redirect('?err=%s' % 'Email failed to send.')


###########################
### Creates the actual intro email
### once the initial user has acquiesced
### /response
###########################
class Response(app.basic.BaseHandler):		
	def get(self):
		# Get intro from database
		intro_id = int(self.get_argument('id', ''))
		intro = introdb.get_by_id(intro_id)
		if not intro:
			self.render('response.html', intro=None, err="Sorry! I couldn't find this intro in my database. Please contact brittany@usv.com")
		# Check for already completed
		if 'connected' in intro.keys():
			self.render('response.html', intro=None, err="Your email has already been sent! Stop clicking the link!")

		subject = "%s <-> %s" % (intro['for_name'], intro['to_name'])
		body = 'Great that you guys are connecting!<br><br>(For context, %s wants to meet with %s to %s)<br><br>Thanks - Brittbot' % (intro['for_name'], intro['to_name'], intro['purpose'])
		try:
			response = self.send_email(settings.get('name') [intro['to_email'], intro['for_email']], subject, body, html=body, from_name="Brittany Laughlin")
			print response
			print 'Connection email sent to %s and %s' % (intro['to_email'], intro['for_email'])
		except: 
			self.render('response.html', intro=None, err="Sorry, there was a problem with our email server. Please try again or contact brittany@usv.com")
		
		intro['connected'] = datetime.datetime.now()
		introdb.save_intro(intro)
		return self.render('response.html', intro=intro, err=None)

