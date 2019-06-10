import os
BASE_DIRS = os.path.dirname(__file__) #路径优化

#数据库配置
import dbconn
dbconn.register_dsn("host=localhost dbname=StaticInfo user=postgres password=")

#参数
options = {
    "port":8888
}

#配置
settings = {
    "static_path":os.path.join(BASE_DIRS, "static"),
    "template_path":os.path.join(BASE_DIRS, "templates"),
    "debug":True   
}