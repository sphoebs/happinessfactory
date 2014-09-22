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
sys.path.append('flib/')
sys.path.append('DB/')

import webapp2
from urlparse import urlparse
import logging
import settings
import social_login
from PUser import PUser
import time


import jinja2
import os


template_dir=os.path.join(os.path.dirname(__file__), 'templates')
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    #extensions=['jinja2.ext.autoescape'],
    autoescape=True)


'''
def get_current_user(request, cookie_name):
        user_id = BaseHandler.parse_cookie(request.cookies.get(cookie_name), settings.LOGIN_COOKIE_DURATION)
        
        if user_id:
            logging.error("\n USER ID COOKIE DETECTED \n")
            logging.error('::get_current_user:: returning user' + user_id)
            user = PUser.query(PUser.user_id==user_id).get() 
            logging.error('\n ::user object:: returning user' + str(user))
            return PUser.get_by_user_id(user_id) 

  '''

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

      
 
        
        
        
class MainHandler(BaseRequestHandler):
    def get(self):
        
        '''
        user= get_current_user(self.request,'user')
        logging.error("returned user"+str(user))
        if user:
            params.update({'user':user})
            logging.error("USER EXISTS")
    
        '''
        params={}
        logging.error(self.request)
        page = urlparse(self.request.url).path
        #logging.error(LoginManager.get_login_URL(self.request, 'facebook'))

        if page == '/':
            self.render('index.html', params)
        else:
            self.render(page, params)
        #self.write('Hello world!') 
        
 
        

app = webapp2.WSGIApplication([

    ('/.*', MainHandler)
], debug=True)
