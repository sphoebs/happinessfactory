
import webapp2
import os
import jinja2
import logging
from google.appengine.api import urlfetch

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

class LoginHandler(BaseRequestHandler):
    
    def get (self):
        logging.error(self.request.arguments())
        self.write(self.request.arguments())
        #verify csrf state
        
        #extract access token from the parameters
        code = self.request.get('code')
        self.write('code:'+ code)
        
        #exchange code for token
        url="https://graph.facebook.com/oauth/access_token?client_id=604940769614321&redirect_uri=http://cnn.com}&client_secret=044fcf7b30beb0a91505b5c76afe4c14&code="+code
        result=urlfetch(url)
        self.write(result)
        
        
        #inspect access token
        #GET graph.facebook.com/debug_token?input_token={token-to-inspect}&access_token={app-token-or-admin-token}
        
        
        
        #self.redirect('http://cnn.com?token='+token)
        pass
    
    
