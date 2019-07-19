create table if not exists Sec_Get_Links(
    id int primary key auto_increment,
    url varchar(100),
    links varchar(6000),
    sql_get int(1) default 0 comment '获取sql注入',
    xss_get int(1) default 0 comment '获取xss or csrf等等',
    inc_get int(1) default 0 comment '获取文件包含',
    exec_get int(1) default 0 comment '获取代码执行',
    vlun_get int(1) default 0 comment '获取其他类型漏洞'

)charset =utf8mb4;
alter table Sec_Get_Links add unique(url);