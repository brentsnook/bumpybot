from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from bumpy import bumpy

class PushHandler(webapp.RequestHandler):
    def __init__(self):
        self._bumpy = bumpy.Bumpy()

    def post(self):
	    self._bumpy.push(self.request.path, self.request.body)
        
def main():
    application = webapp.WSGIApplication([('/push.*', PushHandler)], debug=True)
    run_wsgi_app(application)                                    

if __name__ == '__main__':
    main()