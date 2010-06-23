from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from bumpy import bumpy

class PullHandler(webapp.RequestHandler):
    def __init__(self):
        self._bumpy = bumpy.Bumpy()

    def get(self):
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        self.response.out.write(self._bumpy.pull(self.request.path).encode('utf-8'))

def main():
    application = webapp.WSGIApplication([('/pull.*', PullHandler)], debug=True)
    run_wsgi_app(application)                                    

if __name__ == '__main__':
    main()