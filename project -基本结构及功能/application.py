import tornado.web
import conf
from views import index
import os

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/json1", index.Json1Handler),
            (r"/header", index.HeaderHandler),
            (r"/index", index.RedirectHandler),
            (r"/iserror", index.ErrorHandler),
            (r"/postfile", index.PostfileHandler),
            (r"/upfile", index.UpfileHandler),
            (r"/cat", index.CatHandler),
            (r"/students", index.StudentsHandler),
            ###静态文件首页放在最下面###
            (r"/(.*)$", tornado.web.StaticFileHandler, 
            {"path":os.path.join(conf.BASE_DIRS,"static/html"),
            "default_filename":"index.html"}),
            ]
        super(Application,self).__init__(handlers,**conf.settings)
