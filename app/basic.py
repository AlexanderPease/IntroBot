import tornado.web
import requests
import settings
import simplejson as json
import os
import httplib
import logging


class BaseHandler(tornado.web.RequestHandler):
  def __init__(self, *args, **kwargs):
    super(BaseHandler, self).__init__(*args, **kwargs)
                
  def render(self, template, **kwargs): 
    kwargs['current_path'] = self.request.uri 
    super(BaseHandler, self).render(template, **kwargs)

  # Reads current user based on cookies set in twitter.py
  def get_current_user(self):
    return self.get_secure_cookie("username")

  ''' Optional HTML body supercedes plain text body in SendGrid API'''
  def send_email(self, from_user, to_user, subject, text, html=None, from_name=None):
    #if settings.get('environment') != "prod":
    #  print "If this were prod, we would have sent email to %s" % to_user
    #  return

    data = {
        "api_user":settings.get('sendgrid_user'),
        "api_key":settings.get('sendgrid_secret'),
        "from": from_user,
        "to": to_user,
        "subject": subject,
        "text": text,
        "html": html,
        "fromname": from_name
      }
    print 'Sending...'
    print data
    return requests.post(
      "https://sendgrid.com/api/mail.send.json",
      data = data,
      verify = False
      )
