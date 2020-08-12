create database if not exists `learn-python-mysql` default charset=`utf8mb4`;
use `learn-python-mysql`;

drop table if exists `tb_subject`;
create table `tb_subject`
(
	`no` integer auto_increment comment '学科编号',
    `name` varchar(50) not null comment '学科名称',
    `intro` varchar(1000) not null default '' comment '学科介绍',
    `is_host` boolean not null default 0 comment '是不是热门学科',
    primary key (`no`)
);
-- 创建老师表
drop table if exists `tb_teacher`;
create table `tb_teacher`
(
    `no` integer auto_increment comment '老师编号',
    `name` varchar(20) not null comment '老tb_teachertb_teacher师姓名',
    `sex` boolean not null default 1 comment '老师性别',
    `birth` datetime not null comment '出生日期',
    `intro` varchar(1000) not null default '' comment '老师介绍',
    `photo` varchar(255) default null default '' comment '老师照片',
    `goodcount` integer not null default 0 comment '好评数',
    `badcount` integer not null default 0 comment '差评数',
    `sno` integer not null comment '所属学科',
    primary key (`no`),
    foreign key (`sno`) references `tb_subject` (`no`)
);

-- 查询学科表全部信息
select * from `tb_subject`;


insert into `tb_user`
    (`username`, `password`, `tel`, `reg_date`)
values
    ('wangdachui', '1c63129ae9db9c60c3e8aa94d3e00495', '13122334455', now()),
    ('hellokitty', 'c6f8cf68e5f68b0aa4680e089ee4742c', '13890006789', now());
select * from `tb_user`;
