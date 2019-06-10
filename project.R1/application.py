import tornado.web
import conf
from views import index
import os


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/s/student/([0-9]+)?", index.StudentHandler),
            (r"/s/teacher/([0-9]+)?", index.TeacherHandler),
            (r"/s/classroom/([0-9]+)?", index.ClassroomHandler),
            (r"/s/college/([0-9]+)?", index.CollegeHandler),
            (r"/s/scourse/(.*)?", index.ScourseHandler),
            (r"/s/sctable/(.*)?", index.SctableHandler),
            (r"/teatable/([0-9]{7})(.{9}-1|.{9}-2)?", index.TtableHandler),
            (r"/stutable/([0-9]{10})(.{9}-1|.{9}-2)?", index.StableHandler),
            (r"/upfile", index.UpfileHandler),
            (r'/(.*)', index.HtplHandler),
            ]
        super(Application,self).__init__(handlers,**conf.settings)
