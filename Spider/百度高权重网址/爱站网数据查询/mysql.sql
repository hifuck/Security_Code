create database ip_database;
use ip_database;
#创建主数据库


create table indexx(
id int primary key auto_increment,
ip varchar(80),
ipget varchar(1),
datatime varchar(80)
)charset=utf8;

create table result(
id int primary key auto_increment,
ip varchar(80),
address VARCHAR(80),
url varchar(80),
urltitle varchar(80),
port varchar(80),
datatime varchar(80)
)charset=utf8;


