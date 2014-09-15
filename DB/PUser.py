from GFuser import GFUser
from google.appengine.ext import ndb




class PUser(GFUser):
    isAdmin = ndb.BooleanProperty()
    isPlanner = ndb.BooleanProperty()
    favorites = ndb.StringProperty(repeated=True)
    pass


