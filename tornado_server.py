import os
import tornado.httpserver
import tornado.httpclient
import tornado.ioloop
import tornado.options
import tornado.web

import logging

# settings is required/used to set our environment
import settings 

import app.basic
import app.twitter
import app.introbot


class Application(tornado.web.Application):
  def __init__(self):
    debug = (settings.get('environment') == "dev")
    app_settings = {
      "cookie_secret" : "change_me",
      "login_url": "/auth/twitter",
      "static_path" : os.path.join(os.path.dirname(os.path.abspath(__file__)), "static"),
      "template_path" : os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates"),
      "debug": debug,
    }

    handlers = [
      # twitter auth stuff
      (r"/auth/twitter/?", app.twitter.Auth),
      (r"/twitter", app.twitter.Twitter),

      (r'/$', app.introbot.Index),
      (r"/response", app.introbot.Response),
    ]

    tornado.web.Application.__init__(self, handlers, **app_settings)

def main():
  tornado.options.define("port", default=8001, help="Listen on port", type=int)
  tornado.options.parse_command_line()
  logging.info("starting tornado_server on 0.0.0.0:%d" % tornado.options.options.port)
  http_server = tornado.httpserver.HTTPServer(request_callback=Application(), xheaders=True)
  http_server.listen(tornado.options.options.port)
  tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
  main()
