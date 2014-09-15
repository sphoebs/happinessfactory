#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import sys
sys.path.append('handlers/')
sys.path.append('DB/')

import webapp2
from urlparse import urlparse
import logging
import BaseHandler
import settings
from BaseHandler import BaseRequestHandler, LoginManager
from PUser import PUser
import time

def get_current_user(request, cookie_name):
        user_id = BaseHandler.parse_cookie(request.cookies.get(cookie_name), settings.LOGIN_COOKIE_DURATION)
        
        if user_id:
            logging.error("\n USER ID COOKIE DETECTED \n")
            logging.error('::get_current_user:: returning user' + user_id)
            user = PUser.query(PUser.user_id==user_id).get() 
            logging.error('\n ::user object:: returning user' + str(user))
            return PUser.get_by_user_id(user_id) 
        
        
class LoginHandler(BaseRequestHandler):
    def get(self):
        
        if '/fb/oauth_callback' in self.request.url:
            logging.error("\n \n FB request: "+str(self.request.url))
            
            oauth_user_dictionary, access_token, errors = LoginManager.handle_oauth_callback(self.request, 'facebook')
            
            user, result = PUser.add_or_get_user(oauth_user_dictionary, access_token, 'facebook')

            
        elif '/google/oauth_callback' in self.request.url:
            oauth_user_dictionary, access_token, errors = LoginManager.handle_oauth_callback(self.request, 'google')
            
            user, result = PUser.add_or_get_user(oauth_user_dictionary, access_token, 'google')
            #set cookie
            #redirect
            pass
        else:
            logging.error('illegal callback invocation')
        
        logging.error("\n USER:")
        logging.error(oauth_user_dictionary)
        logging.error(user)
        logging.error("\n END USER:")
        BaseHandler.set_cookie(self.response, "user", str(user.user_id), expires=time.time() + settings.LOGIN_COOKIE_DURATION, encrypt=True)
        self.redirect('/login.html')     
        
        
        
class MainHandler(BaseRequestHandler):
    def get(self):
        
        params = {'fb_login_url': LoginManager.get_login_URL(self.request, 'facebook'),
                 'google_login_url': LoginManager.get_login_URL(self.request, 'google')}    
        user= get_current_user(self.request,'user')
        logging.error("returned user"+str(user))
        if user:
            params.update({'user':user})
            logging.error("USER EXISTS")
    
        
        logging.error(self.request)
        page = urlparse(self.request.url).path
        #logging.error(LoginManager.get_login_URL(self.request, 'facebook'))

        if page == '/':
            self.render('index.html', params)
        else:
            self.render(page, params)
        #self.write('Hello world!') 
        
 
        

app = webapp2.WSGIApplication([
    ('/fb/oauth_callback/?',LoginHandler),
    ('/google/oauth_callback/?',LoginHandler),
    ('/.*', MainHandler)
], debug=True)
