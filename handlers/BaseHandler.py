
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

FB_LOGIN_URL= "https://www.facebook.com/dialog/oauth"
FB_GET_TOKEN_URI= ""
FB_GET_INFO_URI= ""
GOOGLE_LOGIN_URI= "https://accounts.google.com/o/oauth2/auth"
GOOGLE_GET_TOKEN_URI= 'https://accounts.google.com/o/oauth2/token'
GOOGLE_GET_INFO_URI= "" 
    
class LoginManager():
    
    @staticmethod
    def get_login_URL(request, provider, params={}):
        callback_url=request.host_url
        #request.url.split('?')[0]
        
        if provider=='facebook':
            url= FB_LOGIN_URL + "?client_id=" + secrets.FB_APP_ID + "&redirect_uri="+ callback_url+"/fb/oauth_callback"
            
        
        if provider == 'google':
            url= GOOGLE_LOGIN_URI + "?client_id="+secrets.GOOGLE_APP_ID+"&redirect_uri="+callback_url+"/google/oauth_callback"+"&response_type=code&scope=email"
            
            
        return url
            
            
            
        
    @staticmethod
    def handle_oauth_callback (request, provider):
        
        
        error = request.get('error')

        if error:
             logging.error(error)
             return None, None, error
            
        #verify csrf state
        
        #extract access token from the parameters
        code = request.get('code')
        callback_url=request.url.split('?')[0]
 
        
        #exchange code for token
        if provider=='facebook':
                url="https://graph.facebook.com/oauth/access_token?client_id=604940769614321&redirect_uri="+callback_url+"&client_secret="+secrets.FB_APP_SECRET+"&code="+code
                result = urllib2.urlopen(url).read()
                if result:
                    access_token, expiration= result.lstrip("access_token=").split("&expires=")
                    url="https://graph.facebook.com/me?access_token="+access_token
                    return json.loads(urllib2.urlopen(url).read()), access_token, None
                else: return None, None, 'No Result'
        
        elif provider =='google':
                payload = {
                          'code': code,
                          'client_id': secrets.GOOGLE_APP_ID,
                          'client_secret': secrets.GOOGLE_APP_SECRET,
                          'redirect_uri': callback_url,
                          'grant_type': 'authorization_code'
                        }
                # get access token from the request token
                #        logging.error('uri for'+self.uri_for('ciao', _full=True))
                resp = urlfetch.fetch(
                            url=GOOGLE_GET_TOKEN_URI,
                            payload=urlencode(payload),
                            method=urlfetch.POST,
                            headers={'Content-Type': 'application/x-www-form-urlencoded'}
                        )
            # get user data using access token
                    
                
                auth_info=json.loads(resp.content)
                logging.error('auth_info')
                logging.error(auth_info)
                    
                    
                url='https://www.googleapis.com/oauth2/v3/userinfo?{0}'
                target_url = url.format(urlencode({'access_token':auth_info['access_token']}))
                resp=urlfetch.fetch(target_url).content
                user_data = json.loads(resp)
                if 'id' not in user_data and 'sub' in user_data:
                    user_data['id'] = user_data['sub']

                return user_data, access_token, None
                '''
                logging.error("callback:USER data")
                logging.error(user_data)

                user= User.query(User.google_id==user_data['id']).fetch(1)

                logging.error("callback:USER from query")
                logging.error(user)
                '''
        
        
        
        
        
        else: return None, None, 'invalid provider'
            
        
       
            
            
 

    
    
