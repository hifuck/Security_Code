create database if not exists Langzi_Scan_3;
use Langzi_Scan_3;
create table if not exists Sec_Scan_Index(
    id int primary key auto_increment,
    url varchar(80),
    links_get int(1) default 0,
    back_get int(1) default 0,
    unauth_get int(1) default 0,
    port_get int(1) default 0,
    info_get int(1) default 0
)charset =utf8mb4;
alter table Sec_Scan_Index add unique(url);

create table if not exists Sec_Get_Links(
    id int primary key auto_increment,
    url varchar(100),
    links longtext,
    sql_get int(1) default 0 comment '获取sql注入',
    xss_get int(1) default 0 comment '获取xss or csrf等等',
    inc_get int(1) default 0 comment '获取文件包含',
    exec_get int(1) default 0 comment '获取代码执行',
    vlun_get int(1) default 0 comment '获取其他类型漏洞'

)charset =utf8mb4;
alter table Sec_Get_Links add unique(url);

create table if not exists Sec_Ip_Vluns(
    id int primary key auto_increment,
    url varchar(100),
    ip varchar(16),
    unau_get int(1) default 0 comment '获取未授权访问',
    wpas_get int(1) default 0 comment '获取弱口令',
    vlun_get int(1) default 0 comment '获取其他类型漏洞'

)charset =utf8mb4;
alter table Sec_Ip_Vluns add unique(ip);


