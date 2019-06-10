----------------------------------------基础信息--------------------------------------------------
--学生表
DROP TABLE IF EXISTS student;
CREATE TABLE IF NOT EXISTS student  (
    sn            INTEGER,          --序号
    sno           VARCHAR(10),      --学号
    sname         TEXT,             --姓名
    gender        CHAR(1),          --性别(F/M/O)
    cla           TEXT,             --班级
    major         TEXT,             --专业
    institute     TEXT,             --学院
    enrolled      DATE,             --入学时间
    PRIMARY KEY(sno)
);
-- 给sn创建一个自增序号
CREATE SEQUENCE seq_student_sn 
    START 1 INCREMENT 1 OWNED BY student.sn;
ALTER TABLE student ALTER sn 
    SET DEFAULT nextval('seq_student_sn');
-- 学号唯一
CREATE UNIQUE INDEX idx_student_no ON student(sno);

--教师表
DROP TABLE IF EXISTS teacher;
CREATE TABLE IF NOT EXISTS teacher   (
    sn            INTEGER,         --序号
    tno           VARCHAR(7),      --教职工号
    tname         TEXT,            --教师姓名
    gender        CHAR(1),         --性别(F/M/O)
    institute     TEXT,            --学院
    enrolled      DATE,            --工作年份
    PRIMARY KEY(tno)
);
-- 给sn创建一个自增序号
CREATE SEQUENCE seq_teacher_sn 
    START 1 INCREMENT 1 OWNED BY teacher.sn;
ALTER TABLE teacher ALTER sn 
    SET DEFAULT nextval('seq_teacher_sn');
-- 教职工号唯一
CREATE UNIQUE INDEX idx_teacher_no ON teacher(tno);

--教秘表
DROP TABLE IF EXISTS secretary;
CREATE TABLE IF NOT EXISTS secretary   (
    sn            INTEGER,          --序号
    seno          VARCHAR(7),       --教秘号
    name          TEXT,             --姓名
    gender        CHAR(1),          --性别(F/M/O)
    enrolled      DATE,             --工作年份
    PRIMARY KEY(seno)
);
-- 给sn创建一个自增序号
CREATE SEQUENCE seq_secretary_sn 
    START 1 INCREMENT 1 OWNED BY secretary.sn;
ALTER TABLE secretary ALTER sn 
    SET DEFAULT nextval('seq_secretary_sn');
-- 教秘号唯一
CREATE UNIQUE INDEX idx_secretary_no ON secretary(seno);

--教室表
DROP TABLE IF EXISTS classroom;
CREATE TABLE IF NOT EXISTS classroom  (
    sn            INTEGER,          --序号
    campus        TEXT,             --校区
    building      TEXT,             --教学楼
    croom         TEXT,             --教室
    PRIMARY KEY(sn)
);
-- 给sn创建一个自增序号
CREATE SEQUENCE seq_classroom_sn 
    START 1 INCREMENT 1 OWNED BY classroom.sn;
ALTER TABLE classroom ALTER sn 
    SET DEFAULT nextval('seq_classroom_sn');

--学院规划表
DROP TABLE IF EXISTS college;
CREATE TABLE IF NOT EXISTS college  (
    sn            INTEGER,          --序号
    institute     TEXT,             --学院
    major         TEXT,             --专业
    cla           TEXT,             --班级
    PRIMARY KEY(cla)
);
-- 给sn创建一个自增序号
CREATE SEQUENCE seq_college_sn 
    START 1 INCREMENT 1 OWNED BY college.sn;
ALTER TABLE college ALTER sn 
    SET DEFAULT nextval('seq_college_sn');

----------------------------------------------课程预备-----------------------------------------------------
--选择学期
--课程表简表  
DROP TABLE IF EXISTS coursepre;
CREATE TABLE IF NOT EXISTS coursepre  (
    sn            INTEGER,          --序号
    term          TEXT,             --学期(已选)
    courseno      INTEGER,          --课程号(待填写)
    cname         TEXT,             --课程名(待填写)
    credit        INTEGER,          --学分(待填写)
    property      TEXT,             --课程属性(待填写)
    PRIMARY KEY(courseno)
);
-- 给sn创建一个自增序号
CREATE SEQUENCE seq_coursepre_sn 
    START 1 INCREMENT 1 OWNED BY coursepre.sn;
ALTER TABLE coursepre ALTER sn 
    SET DEFAULT nextval('seq_coursepre_sn');   
-- 课程号唯一
CREATE UNIQUE INDEX idx_coursepre_no ON coursepre(courseno);


---------------------------------------------排课阶段----------------------------------------------------------
--再选择课程
--课程方案表（给课程添加老师，班级，时间，教室 ）
DROP TABLE IF EXISTS ctable;
CREATE TABLE IF NOT EXISTS ctable(
    sn            INTEGER,           --序号 
    term          TEXT,              --学期(已选)
    courseno      INTEGER,           --课程号(待填写)
    tno           VARCHAR(7),        --教职工号(待填写)
    cla           TEXT,              --班级(待填写)
    week          TEXT,              --周次(待填写)
    weekday       TEXT,              --星期(待填写)
    period        TEXT,              --节次(待填写)
    campus        TEXT,              --校区(待填写)
    building      TEXT,              --教学楼(待填写)
    croom         TEXT,              --教室(待填写)
    PRIMARY KEY(courseno)
);
-- 给sn创建一个自增序号
CREATE SEQUENCE seq_ctable_sn 
    START 1 INCREMENT 1 OWNED BY ctable.sn;
ALTER TABLE ctable ALTER sn 
    SET DEFAULT nextval('seq_ctable_sn');
-----------------------------------------------外键---------------------------------------------------------------------------
ALTER TABLE student
    ADD CONSTRAINT s_cla_fk FOREIGN KEY (cla) REFERENCES college(cla);
ALTER TABLE ctable
    ADD CONSTRAINT c_cla_fk FOREIGN KEY (cla) REFERENCES college(cla);
ALTER TABLE ctable
    ADD CONSTRAINT college_tno_fk FOREIGN KEY (tno) REFERENCES teacher(tno);
ALTER TABLE ctable
    ADD CONSTRAINT ct_cc_fk FOREIGN KEY (courseno) REFERENCES coursepre(courseno);













    


