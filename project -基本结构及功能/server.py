import tornado.web #web框架模块
import tornado.ioloop #核心I/O循环模块
import conf
from application import Application





if __name__ == "__main__":
    app = Application()
    app.listen(conf.options["port"])   #只能在单进程下使用
    tornado.ioloop.IOLoop.instance().start()