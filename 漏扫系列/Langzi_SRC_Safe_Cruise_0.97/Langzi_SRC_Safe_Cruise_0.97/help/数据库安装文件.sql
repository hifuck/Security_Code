create database if not exists Langzi_Scan;
use Langzi_Scan;

create table if not exists Sec_Index(
    id int primary key auto_increment,
    url varchar(80),
    extrurs int(1) default 0 comment '爬行获取静态链接和动态参数，状态：0/1',
    extrurr int(1) default 0 comment '爬行获取命令执行需要的url，状态：0/1',
    unauth int(1) default 0 comment '（获取未授权需要的url，状态：0/1）',
    subdomain int(1) default 0 comment '获取子域名，既需要爬行页面相关内容，状态：0/1）',
    gitsvn int(1) default 0 comment '扫描gitsvn源码泄露，状态：0/1）',
    backup int(1) default 0 comment '扫描源码泄露，状态：0/1）',
    info int(1) default 0 comment '（扫描敏感信息路径泄露与开放端口服务，状态：0/1）',
    cors int(1) default 0 comment '（扫描sors劫持，状态：0/1）',
    other_vlun int(1) default 0 comment '获取其他类型漏洞，状态：0/1）',
    create_time timestamp DEFAULT CURRENT_TIMESTAMP


)charset =utf8mb4;
alter table Sec_Index add unique(url);



create table if not exists Sec_Links_0(
    id int primary key auto_increment,
    url varchar(100),
    links longtext comment '静态链接，类型是一个列表',
    sqls int(1) default 0 comment '获取sql注入',
    create_time timestamp DEFAULT CURRENT_TIMESTAMP

)charset =utf8mb4;
alter table Sec_Links_0 add unique(url);


create table if not exists Sec_Links_1(
    id int primary key auto_increment,
    url varchar(100) comment '记住，这里是按照深度分类，数量较小',
    links longtext comment '（一个列表，其中保存动态超链接）',
    sqls int(1) default 0 comment '（扫描SQL注入，状态：0/1）',
    xss int(1) default 0 comment '（扫描xss，状态：0/1）',
    urls int(1) default 0 comment '（扫描url跳转，状态：0/1）',
    lfi int(1) default 0 comment '（扫描文件包含，文件读取，状态：0/1）',
    rce int(1) default 0 comment '（扫描命令执行，状态：0/1）',
    create_time timestamp DEFAULT CURRENT_TIMESTAMP

)charset =utf8mb4;
alter table Sec_Links_1 add unique(url);


create table if not exists Sec_Links_2(
    id int primary key auto_increment,
    url varchar(100)comment '记住，这里是按照路径相似度分类，数量较大',
    links longtext comment '（一个列表，其中保存动态超链接）',
    sqls int(1) default 0 comment '（扫描SQL注入，状态：0/1）',
    xss int(1) default 0 comment '（扫描xss，状态：0/1）',
    urls int(1) default 0 comment '（扫描url跳转，状态：0/1）',
    lfi int(1) default 0 comment '（扫描文件包含，文件读取，状态：0/1）',
    rce int(1) default 0 comment '（扫描命令执行，状态：0/1）',
    create_time timestamp DEFAULT CURRENT_TIMESTAMP

)charset =utf8mb4;
alter table Sec_Links_2 add unique(url);




create table if not exists Sec_R_links(
    id int primary key auto_increment,
    url varchar(100),
    links longtext comment '（一个字典，其中保存按照命令执行漏洞类型的url链接，比如action，do，jsp，php等）',
    rce int(1) default 0 comment '（扫描命令执行，状态：0/1）',
    ssf int(1) default 0 comment '（扫描ssrf，状态：0/1）',
    create_time timestamp DEFAULT CURRENT_TIMESTAMP

)charset =utf8mb4;
alter table Sec_R_links add unique(url);

create table if not exists Sec_success(
    id int primary key auto_increment,
    url varchar(100),
    vlun_type longtext comment '保存成功状态',
    create_time timestamp DEFAULT CURRENT_TIMESTAMP
)charset =utf8mb4;


create table if not exists Sec_Ip_Vluns(
    id int primary key auto_increment,
    url varchar(100),
    ip varchar(16),
    unau_get int(1) default 0 comment '获取未授权访问',
    wpas_get int(1) default 0 comment '获取弱口令',
    port_get int(1) default 0 comment '获取开放端口的信息',
    other_vlun int(1) default 0 comment '获取其他类型漏洞',
    create_time timestamp DEFAULT CURRENT_TIMESTAMP

)charset =utf8mb4;
alter table Sec_Ip_Vluns add unique(ip);


create table if not exists Sec_Urls(
    id int primary key auto_increment,
    url varchar(80) COMMENT '所有爬行的网页中的链接保存一下,这个功能由子域名爆破的web模块实现',
    title varchar (80) comment '网页标题',
    power varchar (80) comment '网址使用脚本语言',
    server varchar (80) comment '网址服务器类型',
    content longtext comment '网页内容，到时候可以做URL采集判断',
    create_time timestamp DEFAULT CURRENT_TIMESTAMP

)charset =utf8mb4;
alter table Sec_Urls add unique(url);

create table if not exists Sec_Fail_Links(
    id int primary key auto_increment,
    url varchar(80) COMMENT '所有爬行的网页中的链接访问失败的保存一下',
    get_links int(1) default 0 comment '如果需要再次使用，可以做判断',
    create_time timestamp DEFAULT CURRENT_TIMESTAMP

)charset =utf8mb4;
alter table Sec_Fail_Links add unique(url);

