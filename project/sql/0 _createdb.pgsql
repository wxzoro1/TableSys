DROP DATABASE IF EXISTS scdb;

DROP ROLE IF EXISTS scdb; 

-- 创建一个登陆角色（用户），用户名scdbo, 缺省密码pass
CREATE ROLE scdbo LOGIN
  ENCRYPTED PASSWORD 'md568cefad35fed037c318b1e44cc3480cf' -- password: pass
  NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE;

CREATE DATABASE scdb WITH OWNER = scdbo ENCODING = 'UTF8';
   