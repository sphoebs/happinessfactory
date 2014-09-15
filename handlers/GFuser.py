from google.appengine.ext import ndb



class GFUser(ndb.Model):
    user_id= ndb.StringProperty(required=True)
    
    
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    
    first_name = ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)
    full_name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    
    fb_user_id = ndb.StringProperty() #facebook user-id
    fb_first_name = ndb.StringProperty(required=True)
    fb_last_name = ndb.StringProperty(required=True)
    fb_email = ndb.StringProperty(required=True)
    fb_profile = ndb.StringProperty()
    fb_locale = ndb.StringProperty()
    fb_name = ndb.StringProperty()
    fb_gender= ndb.StringProperty()
    fb_access_token = ndb.StringProperty()
    
    google_user_id = ndb.StringProperty()
    picture=ndb.StringProperty()
    google_profile = ndb.StringProperty()
    locale = ndb.StringProperty()
    google_locale = ndb.StringProperty()
    google_access_token = ndb.StringProperty()
    
    

    @staticmethod
    def get_all_users():
        return GFUser.query()
    
    
    @staticmethod
    def FB_add_or_get(user_response, access_token, update=False):
        '''
        adds the user, if new, and returns it,  else just returns the user
        '''
        user_query = GFUser.query(ndb.OR(
                                    GFUser.fb_user_id == user_response['id'],
                                    GFUser.email == user_response['email'].lower()
                                    )
                            )
        
        user= user_query.get()
            
        if  user and user.fb_user_id: 
            
            user.fb_access_token = access_token
            return user, ['FB_user_exists']
        
        status=[]
        
        if not user:
            user= GFUser()
            user.user_id="FB_"+user_response['id']
            user.first_name = user_response['first_name']
            user.last_name = user_response['last_name']
            user.email = user_response['email']
            user.full_name = user_response['name']
            status.append('user_added')
         
        else: status.append('FB_user_data_added')
            
        #add FB details
        user.fb_user_id = user_response['id']
        user.fb_first_name = user_response['first_name']
        user.fb_last_name = user_response['last_name']
        user.fb_email = user_response['email']
        user.fb_profile = user_response['link']
        user.fb_locale = user_response['locale']
        user.fb_name = user_response['name']
        user.fb_gender = user_response['gender']
        user.fb_access_token = access_token
        
        user.put()
        return user, status
       
            
    @staticmethod
    def google_add_or_get(user_response, update=False):
        '''
        adds the user, if new, and returns it,  else just returns the user
        '''
        user_query = GFUser.query(ndb.OR(
                                    GFUser.google_user_id == user_response['id'],
                                    GFUser.email == user_response['email'].lower()
                                    )
                            )
        
        user= user_query.get()
            
        if  user and user.google_user_id: return user, ['Google_user_exists']
        
        status=[]
        
        if not user:
            user= GFUser()
            user.user_id="google_"+user_response['id']
            user.first_name = user_response['first_name']
            user.last_name = user_response['last_name']
            user.email = user_response['email']
            user.full_name = user_response['name']
            status.append('user_added')
         
        else: status.append('google_user_data_added')
            
        #add FB details
        user.XXXXXXXXX_user_id = user_response['id']
        user.fb_first_name = user_response['first_name']
        user.fb_last_name = user_response['last_name']
        user.fb_email = user_response['email']
        user.fb_profile = user_response['link']
        user.fb_locale = ser_response['locale']
        user.fb_name = user_response['name']
        user.fb_gender = user_response['gender']
        
        user.put()
        return user, status    
    
    
    
    
        
      
    
    
    '''
    full_name = ndb.StringProperty(required=True)
    
    google_user_id = ndb.StringProperty()
    picture=ndb.StringProperty()
    google_profile = ndb.StringProperty()
    locale = ndb.StringProperty()
    google_locale = ndb.StringProperty()
    google_access_token = ndb.StringProperty(required=True)
    isAdmin = ndb.BooleanProperty()
    isPlanner = ndb.BooleanProperty()
    favorites = ndb.StringProperty(repeated=True)
    
   
    {u'id': u'10152334516046006', u'gender': u'male', u'timezone': 2, u'verified': True, u'name': u'Fabio Casati' u'en_US', u'updated_time': u'2013-12-23T17:51:43+0000', 
    '''