import tornado.web
import requests
import settings
import simplejson as json
import os
import httplib
import logging

from lib import userdb

class BaseHandler(tornado.web.RequestHandler):
  def __init__(self, *args, **kwargs):
    super(BaseHandler, self).__init__(*args, **kwargs)
      
    self.vars = {
      #'user': user,
      #'css_modified_time': css_modified_time
    }
                
  def render(self, template, **kwargs): 
    kwargs['current_path'] = self.request.uri 
    super(BaseHandler, self).render(template, **kwargs)

  ''' Optional HTML body supercedes plain text body in SendGrid API'''
  def send_email(self, from_user, to_user, subject, text, html=None, from_name=None):
    if settings.get('environment') != "prod":
      logging.info("If this were prod, we would have sent email to %s" % to_user)
      return
    else:
        return requests.post(
          "https://sendgrid.com/api/mail.send.json",
          data={
            "api_user":settings.get('sendgrid_user'),
            "api_key":settings.get('sendgrid_secret'),
            "from": from_user,
            "to": to_user,
            "subject": subject,
            "text": text,
            "html": html,
            "fromname": from_name
          },
          verify=False
        )
      
    
  def is_blacklisted(self, screen_name):
    u = userdb.get_user_by_screen_name(screen_name)
    if u and 'user' in u.keys() and 'is_blacklisted' in u['user'].keys() and u['user']['is_blacklisted']:
      return True
    return False

  def current_user_can(self, capability):
    """
    Tests whether a user can do a certain thing.
    """
    result = False
    u = userdb.get_user_by_screen_name(self.current_user)
    if u and 'role' in u.keys():
      try:
        if capability in settings.get('%s_capabilities' % u['role']):
          result = True
      except:
        result = False
    return result
