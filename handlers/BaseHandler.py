
import webapp2
import os
import jinja2
import logging
from google.appengine.api import urlfetch
import urllib2
from urlparse import urlparse
import json
import secrets

from GFuser import GFUser


template_dir=os.path.join(os.path.dirname(__file__), '../templates')
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    #extensions=['jinja2.ext.autoescape'],
    autoescape=True)



class BaseRequestHandler(webapp2.RequestHandler):
    
    
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)



    def render(self, template_name, template_vars={}):
     values={}
     values.update(template_vars)
     try:
       template=JINJA_ENVIRONMENT.get_template(template_name)
       self.write(template.render(**values))
     except:
       logging.error("Rendering Exception for " + template_name)
       self.abort(404)



    def dispatch(self):
        logging.error('URL:' + self.request.url)
       
            
        webapp2.RequestHandler.dispatch(self)

    # try:
       # Dispatch the request.
       #webapp2.RequestHandler.dispatch(self)
    # finally:
       # Save all sessions.
       #self.session_store.save_sessions(self.response)

class LoginManager():
    @staticmethod
    def handle_fb_callback (request):
        
        #verify csrf state
        
        #extract access token from the parameters
        code = request.get('code')
        callback_url=request.url.split('?')[0]
 
        
        #exchange code for token
        url="https://graph.facebook.com/oauth/access_token?client_id=604940769614321&redirect_uri="+callback_url+"&client_secret="+secrets.FB_APP_SECRET+"&code="+code
        
        
        result = urllib2.urlopen(url).read()
        if result:
            access_token, expiration= result.lstrip("access_token=").split("&expires=")
            url="https://graph.facebook.com/me?access_token="+access_token
            return json.loads(urllib2.urlopen(url).read()), access_token, None
        else: return None, None, 'No Result'
            
            
 

    
    
