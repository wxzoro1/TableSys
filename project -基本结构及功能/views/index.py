import tornado.web
from tornado.web import RequestHandler 
import conf
import os

#传参数
class HomeHandler(RequestHandler): 
    def get(self, *args, **kwargs):
        temp = 100
        flag = 0
        per = {
            "name":"jack",
            "age":13
        }
        stus = [
            {"name":"suri","age":"20"},
            {"name":"suri","age":"20"}
        ]   
        self.render("home.html", num = temp, per=per, flag = flag, stus = stus)
#读json
import json
class Json1Handler(RequestHandler): #json
    def get(self, *args, **kwargs):
        per = {
            "name":"sunck",
            "age":"18",
            "height":175,
            "weight":7
        }
        self.write(per)
#设置头
class HeaderHandler(RequestHandler): 
    def set_default_headers(self):
        self.set_header("Content-Type", "text/html; charset= UTF-8")
    def get(self, *args, **kwargs):
        pass
    def post(self, *args, **kwargs):
        pass
#重定向
class RedirectHandler(RequestHandler): 
    def get(self, *args, **kwargs):
        self.redirect("/")
#错误处理
class ErrorHandler(RequestHandler): 
    def write_error(self, status_code, **kwargs):
        if status_code == 500:
            code = 500
            #返回500界面
            self.write("服务器内部错误")
        elif status_code == 404:
            code = 404
            #返回404界面
            self.write("资源不存在")
        self.set_status(code)
    def get(self, *args, **kwargs):
        flag = self.get_query_argument("flag")
        if flag == '0':
            self.send_error(500)
        self.write("right")
#获得post参数
class PostfileHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render("postfile.html")
    def post(self, *args, **kwargs):
        name = self.get_argument("username")
        passwd = self.get_argument("passwd")
        print(name,passwd)
        self.write("im good")
#上传文件
class UpfileHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render("upfile.html")
    def post(self, *args, **kwargs):
        filesDict = self.request.files
        for inputname in filesDict:
            fileArr = filesDict[inputname]
            for fileObj in fileArr:
                filePath = os.path.join(conf.BASE_DIRS,
                "upfile/" + fileObj.filename)
                with open (filePath, "wb") as f:
                    f.write(fileObj.body)
        self.write("上传完毕")
#继承
class CatHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render("cat.html",title="cat")
#读数据库
class StudentsHandler(RequestHandler):
    def get(self, *args, **kwargs):
        stus = []
        self.render("student.html", stus = stus)
        