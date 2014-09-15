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
from BaseHandler import BaseRequestHandler, LoginManager
from PUser import PUser


class LoginHandler(BaseRequestHandler):
    def get(self):
        
        if '/fb/oauth_callback' in self.request.url:
            logging.error("\n \n FB request: "+str(self.request.url))
            
            oauth_user_dictionary, access_token, errors = LoginManager.handle_oauth_callback(self.request, 'facebook')
            
            user, result = PUser.FB_add_or_get(oauth_user_dictionary, access_token)
        
        elif '/google/oauth_callback' in self.request.url:
            #oauth_user_dict, access_token, errors = LoginManager.handle_fb_callback(self.request)
            #user, result = PUser.FB_add_or_get(oauth_user_dict, access_token)
            #set cookie
            #redirect
            pass
        else:
            logging.error('illegal callback invocation')
        
              
        
class MainHandler(BaseRequestHandler):
    def get(self):
        
        
        logging.error(self.request)
        page = urlparse(self.request.url).path
        logging.error(LoginManager.get_login_URL(self.request, 'facebook'))
        params = {'fb_login_url': LoginManager.get_login_URL(self.request, 'facebook'),
                 'google_login_url': LoginManager.get_login_URL(self.request, 'google')}
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
