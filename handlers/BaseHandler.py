
import webapp2
import os
import jinja2

template_dir=os.path.join(os.path.dirname(__file__), 'templates')
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

       
            
        webapp2.RequestHandler.dispatch(self)

    # try:
       # Dispatch the request.
       #webapp2.RequestHandler.dispatch(self)
    # finally:
       # Save all sessions.
       #self.session_store.save_sessions(self.response)


