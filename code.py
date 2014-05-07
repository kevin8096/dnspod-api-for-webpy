import web
import os
urls = (
    '/test', 'hello',
    '/test2', 'hi',
    )
class hello:
    def __init__(self):
        self.render = web.template.render(os.path.join(os.path.dirname(__file__), 'templates/'))
        
    def GET(self,name=None):
        return self.render.index('kevin')

class hi:
    def GET(self):
	return " hi python!!"



application = web.application(urls, globals()).wsgifunc()
