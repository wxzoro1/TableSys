import tornado.web
from tornado.web import RequestHandler 
import conf
import os
import dbconn
import json
import datetime

#cursor/read-write Json/json encoder
class NewRequestHandler(RequestHandler):
    def db_cursor(self, autocommit=False):
        return dbconn.SimpleSqlBlock(autocommit=autocommit)
    def read_json(self):
        json_obj = json.loads(self.request.body)
        return json_obj
    def write_json(self, data):
        json_str = json.dumps(data, cls=JsonDataEncoder)
        self.set_header('Content-type', 'application/json; charset=UTF-8')
        self.write(json_str)

#Json解码
class JsonDataEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        elif isinstance(obj, (decimal.Decimal)) :
            return float(obj)
        else:
            return json.JSONEncoder.default(self, obj) 

#错误页面处理
class HtplHandler(NewRequestHandler):
    def get(self, path):
        if not path: 
            path = 'index'
        page = os.path.join( path +'.html')
        print(page)
        try: 
            if path == 'teatable':
                self.redirect('teatable.html')  
            else:    
                self.set_header("Content-Type", "text/html; charset=UTF-8")
                self.render(page)
        except IOError as e:
            if not os.path.exists(page): 
                raise tornado.web.HTTPError(404)
            raise   

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

#学生表
class StudentHandler(NewRequestHandler):
    def get(self, sn):
        print(11111111111)
        sql = '''
        select * from student
        '''
        with self.db_cursor() as dc:
            if sn :
                sn = int(sn)
                sql += " WHERE sn=%s"
                dc.execute(sql, [sn])
                self.write_json(dc.fetchone_dict())
            else:
                sql += 'ORDER BY sno'
                dc.execute(sql)
                self.write_json(dc.fetchall_dicts())

    def post(self, sn):
        pub = self.read_json()
        with self.db_cursor() as dc:
            sql = '''
            INSERT INTO student
                (sno, sname, gender, cla, major, institute, enrolled)
                VALUES(%s, %s, %s, %s, %s, %s, %s) RETURNING sn;
            '''
            dc.execute(sql, [pub.get('sno') ,pub.get('sname'), pub.get('gender'), pub.get('cla'),
            pub.get('major'), pub.get('institute'), pub.get('enrolled')])
            sn = dc.fetchone()[0]
            pub['sn']=sn
            self.write_json(pub)

    def put(self, sn):
        pub = self.read_json()
        with self.db_cursor() as dc:
            sql = ''' 
            UPDATE student SET 
                sno = %s, sname = %s, gender= %s, cla= %s, major= %s,institute= %s, enrolled= %s
            WHERE sn=%s;
            '''
            dc.execute(sql, [pub['sno'], pub['sname'], pub['gender'], pub['cla'], pub['major'], 
            pub['institute'], pub['enrolled'], sn])
            dc.commit()
        self.write_json(pub)

    def delete(self, sn):
        sn = int(sn)
        with self.db_cursor() as cur:
            sql = "DELETE FROM student WHERE sn= %s"
            cur.execute(sql, [sn])
    
#教师表
class TeacherHandler(NewRequestHandler):
    def get(self, sn):
        sql = '''
        select * from teacher
        '''
        with self.db_cursor() as dc:
            if sn :
                sn = int(sn)
                sql += " WHERE sn=%s"
                dc.execute(sql, [sn])
                self.write_json(dc.fetchone_dict())
            else:
                sql += 'ORDER BY tno'
                dc.execute(sql)
                self.write_json(dc.fetchall_dicts())

    def post(self, sn):
        pub = self.read_json()
        with self.db_cursor() as dc:
            sql = '''
            INSERT INTO teacher 
                (tno, tname, gender, institute, enrolled)
                VALUES(%s, %s, %s, %s, %s) RETURNING sn;
            '''
            dc.execute(sql, [pub.get('tno') ,pub.get('tname'), pub.get('gender'), 
            pub.get('institute'), pub.get('enrolled')])
            sn = dc.fetchone()[0]
            pub['sn']=sn
            self.write_json(pub)

    def put(self, sn):
        pub = self.read_json()
        with self.db_cursor() as dc:
            sql = ''' 
            UPDATE teacher SET 
                tno = %s, tname = %s, gender= %s, institute= %s, enrolled= %s
            WHERE sn=%s;
            '''
            dc.execute(sql, [pub['tno'], pub['tname'], pub['gender'],
            pub['institute'], pub['enrolled'], sn])
            dc.commit()
        self.write_json(pub)

    def delete(self, sn):
        sn = int(sn)
        with self.db_cursor() as cur:
            sql = "DELETE FROM teacher WHERE sn= %s"
            cur.execute(sql, [sn])

#教室表
class ClassroomHandler(NewRequestHandler):
    def get(self, sn):
        sql = '''
        select * from classroom
        '''
        with self.db_cursor() as dc:
            if sn :
                sn = int(sn)
                sql += " WHERE sn=%s"
                dc.execute(sql, [sn])
                self.write_json(dc.fetchone_dict())
            else:
                sql += 'ORDER BY sn'
                dc.execute(sql)
                self.write_json(dc.fetchall_dicts())

    def post(self, sn):
        pub = self.read_json()
        with self.db_cursor() as dc:
            sql = '''
            INSERT INTO classroom
                (campus, building, croom)
                VALUES(%s, %s, %s) RETURNING sn;
            '''
            dc.execute(sql, [pub.get('campus') ,pub.get('building'), pub.get('croom')])
            sn = dc.fetchone()[0]
            pub['sn']=sn
            self.write_json(pub)

    def put(self, sn):
        pub = self.read_json()
        with self.db_cursor() as dc:
            sql = ''' 
            UPDATE classroom SET 
                campus = %s, building = %s, croom= %s
            WHERE sn=%s;
            '''
            dc.execute(sql, [pub['campus'], pub['building'], pub['croom'], sn])
            dc.commit()
        self.write_json(pub)

    def delete(self, sn):
        sn = int(sn)
        with self.db_cursor() as dc:
            sql = "DELETE FROM classroom WHERE sn= %s"
            dc.execute(sql, [sn])

#学院表
class CollegeHandler(NewRequestHandler):
    def get(self, sn):
        sql = '''
        select * from college
        '''
        with self.db_cursor() as dc:
            if sn :
                sn = int(sn)
                sql += " WHERE sn=%s"
                dc.execute(sql, [sn])
                self.write_json(dc.fetchone_dict())
            else:
                sql += 'ORDER BY sn'
                dc.execute(sql)
                self.write_json(dc.fetchall_dicts())

    def post(self, sn):
        pub = self.read_json()
        with self.db_cursor() as dc:
            sql = '''
            INSERT INTO college
                (institute, major, cla)
                VALUES(%s, %s, %s) RETURNING sn;
            '''
            dc.execute(sql, [pub.get('institute') ,pub.get('major'), pub.get('cla')])
            sn = dc.fetchone()[0]
            pub['sn']=sn
            self.write_json(pub)

    def put(self, sn):
        pub = self.read_json()
        with self.db_cursor() as dc:
            sql = ''' 
            UPDATE college SET 
                institute = %s, major = %s, cla= %s
            WHERE sn=%s;
            '''
            dc.execute(sql, [pub['institute'], pub['major'], pub['cla'], sn])
            dc.commit()
        self.write_json(pub)

    def delete(self, sn):
        sn = int(sn)
        with self.db_cursor() as cur:
            sql = "DELETE FROM college WHERE sn= %s"
            cur.execute(sql, [sn])

#课程计划
class ScourseHandler(NewRequestHandler):
    def get(self, sn):
        sql = '''
        SELECT * FROM coursepre
        '''    
        with self.db_cursor() as dc:
            if  len(sn)>3 and isinstance(sn, str):
                print(111111111)
                sql += " WHERE term='%s'" %(sn)
                dc.execute(sql)
                print(sql)
                self.write_json(dc.fetchall_dicts())
            elif  0<len(sn)<3 :
                print(22222222222)
                sn = int(sn)
                sql += " WHERE sn='%s'" 
                dc.execute(sql,[sn]) 
                self.write_json(dc.fetchone_dict())
            else:  
                print(33333333333333)
                sql += 'ORDER BY courseno' 
                dc.execute(sql)
                self.write_json(dc.fetchall_dicts())                              

    def post(self, sn):
        pub = self.read_json()
        with self.db_cursor() as dc:
            sql = '''
            INSERT INTO coursepre 
                (term, courseno, cname, credit, property)
                VALUES(%s, %s, %s, %s, %s) RETURNING sn;
            '''
            dc.execute(sql, [pub.get('term'),pub.get('courseno') ,pub.get('cname'), 
            pub.get('credit'), pub.get('property')])
            sn = dc.fetchone()[0]
            pub['sn']=sn
            self.write_json(pub)

    def put(self, sn):
        pub = self.read_json()
        with self.db_cursor() as dc:
            sql = ''' 
            UPDATE coursepre SET 
                courseno=%s,  cname=%s, credit=%s, property=%s
            WHERE sn=%s;
            '''
            dc.execute(sql, [pub['courseno'], pub['cname'], pub['credit'], pub['property'], sn])
            dc.commit()
        self.write_json(pub)

    def delete(self, sn):
        sn = int(sn)
        with self.db_cursor() as cur:
            sql = "DELETE FROM coursepre WHERE sn= %s"
            cur.execute(sql, [sn])

#开始排课
class SctableHandler(NewRequestHandler):
    def get(self, sn):
        sql = '''
        select c.sn, c.term, c.courseno, cs.cname as cname, cs.credit as credit, cs.property as property,
        c.tno , t.tname as tname, c.cla, c.week, c.weekday, c.period, c.campus, 
        c.building, c.croom from ctable c
        inner join teacher as t	on c.tno = t.tno
        inner join coursepre as cs on c.courseno = cs.courseno
        '''    
        with self.db_cursor() as dc:
            if  len(sn)>3 and isinstance(sn, str):
                print(sn)
                sql += " WHERE c.term='%s'" %(sn)
                dc.execute(sql)
                print(sql)
                self.write_json(dc.fetchall_dicts())
            elif  0<len(sn)<3:
                sn = int(sn)
                sql += " WHERE c.sn='%s'" 
                dc.execute(sql,[sn]) 
                self.write_json(dc.fetchone_dict())
            else:  
                print(33333333333333)
                sql += 'ORDER BY courseno' 
                dc.execute(sql)
                self.write_json(dc.fetchall_dicts())                              

    def post(self, sn):
        pub = self.read_json()
        with self.db_cursor() as dc:
            sql ='''
            select term, weekday, period, tno, courseno from ctable 
            where tno =%s and term=%s and weekday = %s and period = %s
            '''
            dc.execute(sql,[pub.get('tno'), pub.get('term'), pub.get('weekday'), pub.get('period')])
            course = dc.fetchall()
            print(course)
            print(len(course))
        if len(course) != 0:
            self.write_error("教师冲突")
        else:
            pub = self.read_json()
            with self.db_cursor() as dc:
                sql ='''
                select term, weekday, period, cla, courseno from ctable
                where cla=%s and term=%s and weekday = %s and period = %s
                '''
                dc.execute(sql, [pub.get('cla'), pub.get('term'), pub.get('weekday'), pub.get('period')])
                cla = dc.fetchall()
                print(len(cla))
            if len(cla) != 0 :
                self.write_error('班级(学生)冲突')

            else:
                pub = self.read_json()
                with self.db_cursor() as dc:
                    sql = '''
                    select term, weekday, period, campus, building, croom, courseno from ctable
                    where campus = %s and building = %s and croom = %s and term = %s and weekday = %s
                    and period = %s 
                    '''
                    dc.execute(sql, [pub.get('campus'), pub.get('building'), pub.get('croom'), pub.get('term'),
                    pub.get('weekday'), pub.get('period')])
                    crm = dc.fetchall()
                    print(len(crm))
                if len(crm) != 0 :
                    self.write_error('教室冲突')
                else:
                    with self.db_cursor() as dc:
                        sql = '''
                        INSERT INTO ctable 
                            (term, courseno, tno, cla, week, weekday, period, campus, building, croom)
                            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING sn;
                        '''
                        dc.execute(sql, [pub.get('term'),pub.get('courseno') ,pub.get('tno'), 
                        pub.get('cla'), pub.get('week'), pub.get('weekday'), pub.get('period'), pub.get('campus'),
                        pub.get('building'), pub.get('croom')])
                        sn = dc.fetchone()[0]
                        pub['sn']=sn
                        self.write_json(pub)

    def put(self, sn):
        pub = self.read_json()
        with self.db_cursor() as dc:
            sql = ''' 
            UPDATE ctable SET 
                courseno=%s , tno=%s, cla=%s, week=%s, weekday=%s, period=%s, 
                campus=%s, building=%s, croom=%s 
            WHERE sn=%s;
            '''
            dc.execute(sql, [pub['courseno'],pub['tno'],pub['cla'],pub['week'],
            pub['weekday'],pub['period'],pub['campus'],pub['building'],pub['croom'], sn])
            dc.commit()
        self.write_json(pub)

    def delete(self, sn):
        sn = int(sn)
        with self.db_cursor() as cur:
            sql = "DELETE FROM ctable WHERE sn= %s"
            cur.execute(sql, [sn])

#教师课表
class TtableHandler(RequestHandler):
    def db_cursor(self, autocommit=False):
        return dbconn.SimpleSqlBlock(autocommit=autocommit)
    def get(self, tn, term):
        print(tn,term)
        if term is None:
            term = '2018-2019-2'
        if term[-1] == '1':
            term = term[0:9] + '学年春'
        elif term[-1] == '2':
            term = term[0:9] + '学年秋'
        print(term,tn)

        sql = '''
        select cs.term, cs.courseno, cs.tno, c.cname, c.credit, c.property,
        cs.cla, cs.week, cs.weekday, cs.period, cs.campus, cs.building,
        cs.croom from ctable as cs
        inner join coursepre as c on c.courseno = cs.courseno
        '''
        with self.db_cursor() as dc:
            print(8888888888)
            tn = str(tn)
            sql += "where  cs.term = '%s' and  cs.tno = '%s'" %(term, tn)
            dc.execute(sql)
            items = dc.fetchall()
        print(items)
        self.set_header("Content-Type", "text/html; charset=UTF-8")
        self.render('teatable.html', items = items)
 
#学生课表
class StableHandler(RequestHandler):
    def db_cursor(self, autocommit=False):
        return dbconn.SimpleSqlBlock(autocommit=autocommit)
    def get(self, sn, term):
        print(sn,term)
        if term is None:
            term = '2018-2019-2'
        if term[-1] == '1':
            term = term[0:9] + '学年春'
        elif term[-1] == '2':
            term = term[0:9] + '学年秋'
        print(term,sn)

        sql = '''
        select cs.term, s.sno, cs.courseno, c.cname, c.credit, c.property, t.tname,
        cs.cla, cs.week, cs.weekday, cs.period, cs.campus, cs.building,
        cs.croom from ctable as cs
        inner join coursepre as c  on c.courseno = cs.courseno
        inner join teacher   as t  on t.tno      = cs.tno
        inner join college   as co on co.cla     = cs.cla
        inner join student   as s  on s.cla      = co.cla
        '''
        with self.db_cursor() as dc:
            print(8888888888)
            sn = str(sn)
            sql += "where  cs.term = '%s' and  s.sno = '%s'" %(term, sn)
            dc.execute(sql)
            items = dc.fetchall()
        print(items)
        self.set_header("Content-Type", "text/html; charset=UTF-8")
        self.render('stutable.html', items = items)

        