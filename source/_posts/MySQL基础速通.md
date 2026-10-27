---
title: "📖 MySQL 基础语法速通：SQL 从零到入门的保姆级笔记"
date: 2026-08-12 16:50
description: 一篇从零开始的 MySQL SQL 速通笔记，覆盖 DDL、DML、DQL、DCL、常用函数、约束、多表查询与事务，每条语句都带注释和语法说明，适合初学者照着敲。
categories: [后端数据库]
tags: [MySQL, 笔记, 零基础教程]
cover: ../img/anime-tech-mysql-20260812.jpg
---

# 📖 MySQL 基础语法速通：<span style="color:pink">零基础也能跟着敲</span>

## 📝 前言

这份笔记是整理给自己复习用的，也顺手分享给刚入门的你。当初学 SQL 的时候，我最先被四个缩写搞懵了：DDL、DML、DQL、DCL，名字长得像，作用还各管一摊 😵。所以这篇开头先把它们捋清楚，后面每一块都按「**语法模板 → 代码示例 → 踩坑提醒**」来写。

SQL 关键字大小写不敏感（`select` 和 `SELECT` 都能跑），为了看着清爽，代码里我统一用了小写——没错，就是这么随性 😎。

话不多说，上车吧 🚗

## 🗂️ SQL 到底分几类

SQL（Structured Query Language，结构化查询语言）按功能可以分成四大类：

| 分类 | 英文全称 | 负责什么 | 一句话记住 |
| :--- | :--- | :--- | :--- |
| **DDL** | Data Definition Language | 定义**库和表的结构**（创建、删除、修改表） | 管结构 |
| **DML** | Data Manipulation Language | 对表里的**数据**做增删改 | 管数据 |
| **DQL** | Data Query Language | 查询表里的数据 | 管取数 |
| **DCL** | Data Control Language | 管数据库**用户和权限** | 管权限 |

> 💡 学习顺序建议：先 DDL 把表建起来 → 用 DML 往里塞数据 → 再用 DQL（**出场率最高**）查数据。DCL 平时接触少，一般是 DBA 在管，了解即可。

## ① DDL：数据定义语言

### DDL-数据库操作

**查询**：

```sql
# 查看当前 MySQL 服务器里有哪些数据库
show databases;

# 查看当前正在使用的是哪个数据库
select database();
```

**创建**：

```sql
# 语法：create database [if not exists] 数据库名;
# if not exists：如果这个库已经存在，就不报错直接跳过（很实用，写脚本必备）
create database if not exists database_test_first;
```

**删除**：

```sql
# 语法：drop database [if exists] 数据库名;
# ⚠️ 注意：删库会连库里的表和所有数据一起删掉，删之前一定确认好名字！
drop database if exists database_test_first;
```

**使用**：

```sql
# 语法：use 数据库名; —— 切换到指定库，之后的操作都默认在这个库里执行
use database_test_first;
```

### DDL-表操作（查询）

```sql
# ① 查看当前数据库下所有表
show tables;

# ② desc 表名; —— 查看表结构（字段名、字段类型、注释、是否为空等）
desc user_table;

# ③ 查看某张表的完整建表语句（还能看到引擎、字符集这些隐藏信息）
# 注意：show create 后面要跟 table，别漏了！
show create table user_table;
```

### DDL-表操作（创建）

```sql
# 语法：create table 表名(
#         字段名1 字段类型 comment '字段注释',
#         ...
#      ) comment '表注释';
create table table_user(
    id     int          comment '编号',
    name   varchar(10)  comment '名字',
    age    int          comment '年龄',
    gender varchar(1)   comment '性别'
) comment '用户表';
```

下面这张 `emp` 员工表是后面 DML 的主角，字段类型挑得很典型，挨个认识一下：

```sql
create table emp(
    id        int            comment '编号',
    workno    varchar(10)    comment '工号',
    name      varchar(10)    comment '姓名',
    gender    char(1)        comment '性别',
    age       tinyint unsigned comment '年龄',
    idcard    char(18)       comment '身份证号',
    entrydate date           comment '入职时间'
) comment '员工表';
```

顺带把里面出现的几种常见类型记一下：

| 类型 | 含义 | 备注 |
| :--- | :--- | :--- |
| `int` | 整数 | |
| `varchar(n)` | 可变长度字符串 | 最多存 n 个字符，按实际长度存，省空间 |
| `char(n)` | 定长字符串 | 固定占 n 个字符，性能更好 |
| `tinyint unsigned` | 无符号小整数 | `unsigned` = 非负，范围 0~255 |
| `date` | 日期 | 格式 `yyyy-MM-dd` |

> 💡 `char` 和 `varchar` 的区别：比如性别存 `char(1)`、手机号存 `char(11)`，长度固定用 `char`；姓名这种长短不一的用 `varchar`。

### DDL-表操作（修改）

```sql
# 给 emp 表加一个新字段「昵称」nickname，类型 varchar(20)
# 语法：alter table 表名 add 字段名 类型 comment '注释';
alter table emp add nickname varchar(20) comment '昵称';
```

```sql
# 同时修改「字段名」和「字段类型」：把 nickname 改成 username，并换成 varchar(30)
# 语法：alter table 表名 change 旧字段名 新字段名 类型 comment '注释';
alter table emp change nickname username varchar(30) comment '用户名';
```

### DDL-表操作（删除）

```sql
# 删除一个字段：把刚才的 username 字段删掉
# 语法：alter table 表名 drop 字段名;
alter table emp drop username;
```

### DDL-表操作（修改表名）

```sql
# 把表 emp 改名为 employee
# 语法：alter table 旧表名 rename to 新表名;
alter table emp rename to employee;
```

### DDL-表操作（删除表）

```sql
# 删除整张表（结构和数据都没了），if exists 同理是防报错
# 语法：drop table [if exists] 表名;
drop table if exists table_user;

# truncate：删除表中所有数据，但保留表结构（表还在，只是空了）
# 语法：truncate table 表名;
truncate table employee;
```

> 💡 `truncate` 和后面 DML 的 `delete` 都能清数据，区别是：`truncate` 只能整表清空、速度快；`delete` 可以带 `where` 按条件删、也能回滚。

## ② DML：数据操作语言

### 插入数据

```sql
# 语法①（推荐）：insert into 表名(字段1, 字段2, ...) values (值1, 值2, ...);
#    —— 值要和字段一一对应；括号里不出现的字段会用默认值

insert into employee (id, workno, name, gender, age, idcard, entrydate)
values (1, '1', '小文', '男', 18, '123456789012345678', '2006-07-07');

insert into employee (id, workno, name, gender, age, idcard, entrydate)
values (2, '2', '小新', '女', 18, '123456789012345679', '2006-07-15');

# 语法②（简写）：insert into 表名 values (值1, 值2, ...);
#    —— 省略字段名，值的顺序必须和建表时的字段顺序【完全一致】，少一个都会报错

insert into employee values (3, 3, '小雨', '女', 19, '123456789012345672', '2025-09-02');
insert into employee values (4, 4, '小玉', '女', 20, '123456789012345673', '2024-09-01');

# 语法③（批量插入）：values 后面用逗号分隔多组值，一次插多行
# insert into 表名 values (..),(..),(..);
```

### 更新和删除

```sql
# 更新语法：update 表名 set 字段1=值1, 字段2=值2 ... where 条件;
# ⚠️ where 是灵魂：一旦忘写 where，就会更新整张表的所有行！

update employee set name = '张三' where id = 1;            # 把 id=1 的员工的姓名改成张三

update employee set name = '小张', gender = '女' where id = 1;  # 同时改多个字段，用逗号隔开

update employee set entrydate = '2024-09-01';   # ❌ 没有 where，所有人的入职时间都被改成同一天！

# 删除语法：delete from 表名 where 条件;
delete from employee where id = 4;   # 删除 id=4 这一条记录

delete from employee;                # ❌ 没有 where = 清空整张表所有数据
```

## ③ DQL：数据查询语言

DQL 是日常打交道最多的，下面的语句全部基于这份建表+造数脚本，**建议先跑一遍，让 emp 表里有数据**再继续：

```sql
# -------- 数据准备：建表 --------
# 语法：create table ...（和前面 DDL 一样，注意这次多了 workaddress 工作地址字段）
create table emp(
    id          int              comment '编号',
    workno      varchar(10)      comment '工号',
    name        varchar(10)      comment '姓名',
    gender      char             comment '性别',
    age         tinyint unsigned comment '年龄',
    idcard      char(18)         comment '身份证号',
    workaddress varchar(50)      comment '工作地址',
    entrydate   date             comment '入职时间'
) comment '员工表';

# -------- 数据准备：一次性批量插入 16 条数据 --------
insert into emp (id, workno, name, gender, age, idcard, workaddress, entrydate)
values
(1, '1', '柳岩', '女', 20, '123456789012345678', '北京', '2000-01-01'),
(2, '2', '张无忌', '男', 18, '123456789012345670', '北京', '2005-09-01'),
(3, '3', '韦一笑', '男', 38, '123456789712345670', '上海', '2005-08-01'),
(4, '4', '赵敏', '女', 18, '123456757123845670', '北京', '2009-12-01'),
(5, '5', '小昭', '女', 16, '123456769012345678', '上海', '2007-07-01'),
(6, '6', '杨逍', '男', 28, '12345678931234567X', '北京', '2006-01-01'),
(7, '7', '范瑶', '男', 40, '123456789212345670', '北京', '2005-05-01'),
(8, '8', '黛绮丝', '女', 38, '123456157123645670', '天津', '2015-05-01'),
(9, '9', '范凉凉', '女', 45, '123156789012345678', '北京', '2010-04-01'),
(10, '10', '陈友谅', '男', 53, '123456789012345670', '上海', '2011-01-01'),
(11, '11', '张士诚', '男', 55, '123567897123465670', '江苏', '2015-05-01'),
(12, '12', '常遇春', '男', 32, '123446757152345670', '北京', '2004-02-01'),
(13, '13', '张三丰', '男', 88, '123656789012345678', '江苏', '2020-11-01'),
(14, '14', '灭绝', '女', 65, '123456719012345670', '西安', '2019-05-01'),
(15, '15', '胡青牛', '男', 70, '12345674971234567X', '西安', '2018-04-01'),
(16, '16', '周芷若', '女', 18, null, '北京', '2012-06-01');
# 周芷若的 idcard 故意给了 null，后面演示 IS NULL 和 COUNT 就靠它了 👀
```

### DQL-基础查询

```sql
# 语法：select 字段列表 from 表名;

select name, workno, age from emp;      # 只查这三列
select * from emp;                       # * 代表查全部列（图省事可以，正式项目别滥用）

# as 给字段起「别名」，别名只在结果里显示，不影响原表；as 还能省略（用空格隔开）
select workaddress as '工作地址' from emp;
select workaddress '工作地址' from emp;   # 省略 as 的等价写法

# distinct 去重：同一个工作地址只保留一条，不重复显示
select distinct workaddress '工作地址' from emp;
```

### DQL-条件查询

先认识一下 `where` 后面能用的各种运算符：

| 运算符 | 含义 | 例子 |
| :--- | :--- | :--- |
| `>` `<` `>=` `<=` | 大于 / 小于 / 大于等于 / 小于等于 | `age > 20` |
| `=` | 等于 | `gender = '女'` |
| `<>` / `!=` | 不等于（两种写法都对） | `age <> 88` |
| `between ... and ...` | 在某个范围内（含两端） | `age between 20 and 40` |
| `in (...)` | 命中括号里的任意一个值 | `age in (18, 20, 40)` |
| `like` | 模糊匹配：`_` 代表任意**1**个字符，`%` 代表任意**多个**字符 | `name like '__'` |
| `is null` / `is not null` | 是空 / 非空 | `idcard is null` |
| `and / &&`、`or / \|\|` | 逻辑「与」「或」 | `age > 18 and age < 30` |

```sql
# 语法：select 字段 from 表名 where 条件;

select * from emp where age = 88;            # = 等于（找出张三丰，88 岁那位）
select * from emp where age < 20;            # < 小于
select * from emp where age <= 20;           # <= 小于等于
select * from emp where idcard is null;      # 判断空值【必须用 is null】，不能写成 = null
select * from emp where idcard is not null;  # 非空
select * from emp where age != 88;           # != 不等于
select * from emp where age <> 88;           # <> 也是不等于（SQL 标准写法）
select * from emp where age >= 15 && age <= 25;  # && 相当于 and（18/20 岁这批人）
select * from emp where gender = '女' && age < 25;  # 25 岁以下的女生
select * from emp where age = 18 || age = 20 || age = 40;  # || 相当于 or

# 上面那串 or 写得太啰嗦，in 一句搞定：命中列表里任意一个值
select * from emp where age in (18, 20, 40);

# like 模糊查询：_ 一个字符，% 任意个字符
select * from emp where name like '__';     # 名字刚好是两个字的人
select * from emp where idcard like '%X';   # 身份证号以 X 结尾的人
```

### DQL-聚合函数

聚合函数把「一整列数据」汇总成一个结果，常配合分组一起用：

| 函数 | 作用 |
| :--- | :--- |
| `count(字段)` | 统计**非 null** 的个数；`count(*)` 统计总行数 |
| `sum(字段)` | 求和 |
| `avg(字段)` | 平均值 |
| `max(字段)` / `min(字段)` | 最大值 / 最小值 |

```sql
select count(*) from emp;            # 表里一共有多少行（16）
select count(id) from emp;           # id 非空的个数
select count(idcard) from emp;       # idcard 非空的个数（周芷若那行是 null，不会被算进去，所以会少一个）
select avg(age) from emp;            # 所有人平均年龄
select max(age) from emp;            # 最大年龄（张三丰 88）
select min(age) from emp;            # 最小年龄
select sum(age) from emp where workaddress='西安';   # 聚合函数也能配 where 先过滤再汇总
```

### DQL-分组查询

```sql
# 语法：select 分组字段, 聚合函数 from 表名 where 条件 group by 分组字段 having 分组后过滤;

select count(*) from emp group by gender;          # 按性别分组，统计每组各多少人
select gender, avg(age) from emp group by gender;  # 查性别，以及每个性别的平均年龄

# 案例：统计年龄<45的员工中，各工作地址的人数，只要人数>=3的组
select workaddress, count(*) address_count
from emp
where age < 45                # ① where：分组【前】，先对原始行过滤（不能写聚合函数）
group by workaddress          # ② 按工作地址分组
having address_count >= 3;    # ③ having：分组【后】，再对整组结果过滤（可以用聚合/别名）
```

> ⚠️ 面试常考的点：`where` 和 `having` 的区别。**where 在分组前过滤原始行，不能接聚合函数；having 在分组后过滤组，可以接 `count()/avg()` 这类聚合函数。**

### DQL-排序查询

```sql
# 语法：select ... from 表名 order by 字段1 [asc | desc], 字段2 [asc | desc];
# asc 升序（默认，可省略）；desc 降序

select * from emp order by age asc;             # 按年龄从小到大
select * from emp order by age desc;            # 按年龄从大到小
select * from emp order by age;                 # 不写就是默认升序
select * from emp order by entrydate desc;      # 按入职时间倒序，入职最晚的排最前
select * from emp order by age asc, entrydate desc;  # 多字段排序：先按年龄升序，年龄相同再按入职时间降序
```

### DQL-分页查询

```sql
# 语法：select ... limit 起始索引, 每页条数;  —— 注意起始索引从 0 开始算
select * from emp limit 0, 10;     # 第 1 页：从第 0 条开始取 10 条
select * from emp limit 10, 10;    # 第 2 页：从第 10 条开始取 10 条

# 📌 算分页起始索引的公式：起始索引 = (页码 - 1) × 每页条数
# 比如每页 10 条：第1页=limit 0,10，第2页=limit 10,10，第3页=limit 20,10
```

### DQL-案例练习

把前面学的串起来练手 👇

```sql
# ① 查询年龄 20~23 岁之间的女员工
select * from emp where age in(20,21,22,23) and gender='女';

# ② 查询 20~40 岁、姓名是三个字的男员工（'___' 三个下划线 = 名字三个字）
select * from emp where gender='男' and age between 20 and 40 and name like '___';

# ③ 统计 60 岁以下员工中，男女各有多少人
select gender, count(*) from emp where age<60 group by gender;

# ④ 查询 35 岁及以下员工的姓名、年龄、入职时间，先按年龄升序，年龄相同的按入职时间降序
select name, age, entrydate from emp where age<=35 order by age asc, entrydate desc;

# ⑤ 查询 20~40 岁的男员工，按年龄升序，年龄相同的按入职时间升序
select * from emp where gender='男' and age between 20 and 40 order by age asc, entrydate asc;
```

## ④ DCL：数据控制语言

管「谁能登录、能用哪些库」的，平时自己玩基本用不上，但面试会问，照着敲一遍有印象就行。

### DCL-用户管理

```sql
# ① 创建用户
# 语法：create user '用户名'@'主机' identified by '密码';
# 主机部分：'localhost' = 只允许本机登录；'%' = 允许任意主机远程登录
create user 'test_01'@'localhost' identified by '123456';
create user 'test_02'@'%' identified by '123456';

# ② 修改用户密码：把 test_02 的密码改成 1234，并把认证方式指定为 mysql_native_password
#    （老版本客户端兼容用；MySQL 8.0 默认是新认证 caching_sha2_password）
alter user 'test_02'@'%' identified with mysql_native_password by '1234';
```

### DCL-权限控制

```sql
# ① 查看某用户的权限
# 语法：show grants for '用户名'@'主机';
show grants for 'test_02'@'%';

# ② 授权：grant 权限 on 库名.表名 to '用户名'@'主机';
# 这里的 test_01.* 表示 test_01 库下的所有表；all 表示所有权限
# 语法：grant 权限列表 on 数据库名.表名 to '用户名'@'主机';
grant all on test_01.* to 'test_02'@'%';

# ③ 收回权限：把刚才授出去的收回来
# 语法：revoke 权限列表 on 数据库名.表名 from '用户名'@'主机';
revoke all on test_01.* from 'test_02'@'%';
```

## 🛠️ 常用函数

MySQL 内置了一堆函数，写查询时能省不少事，重点记几个常用的。

### 字符串函数

| 函数 | 作用 |
| :--- | :--- |
| `concat(a, b, ...)` | 把多个字符串拼起来 |
| `lower(s)` / `upper(s)` | 全部转小写 / 大写 |
| `lpad(s, n, p)` / `rpad(s, n, p)` | 用 p 把 s 左/右填充到 n 位 |
| `trim(s)` | 去掉字符串**首尾**的空格 |
| `substring(s, 起始位置, 长度)` | 截取子串，⚠️ 起始位置从 **1** 开始 |

```sql
select concat('Hello','MySQL');          # 拼接 → HelloMySQL
select lower('Hello');                   # 小写 → hello
select upper('Hello');                   # 大写 → HELLO
select lpad('01',5,'_');                 # 左填充 → ___01
select rpad('01',5,'_');                 # 右填充 → 01___
select trim(' Hello MySQL ');            # 去首尾空格 → Hello MySQL
select substring('Hello MySQL',1,5);     # 从第1位截5个 → Hello

# 实战：把员工的工号统一补足成 5 位（不足左边补 0），比如 '1' → '00001'
update emp set workno=lpad(workno,5,'0');
```

### 数值函数

| 函数 | 作用 |
| :--- | :--- |
| `ceil(x)` | 向上取整 |
| `floor(x)` | 向下取整 |
| `mod(x, y)` | 取模（返回 x 除以 y 的余数） |
| `rand()` | 返回 0~1 之间的随机数 |
| `round(x, n)` | 四舍五入，保留 n 位小数 |

```sql
select ceil(1.5);          # → 2
select floor(1.9);         # → 1
select mod(5,3);           # → 2
select rand();             # → 一个 0~1 的随机小数
select round(2.345,2);     # → 2.35

# 综合小案例：生成一个 6 位数字的随机验证码（随机数×1000000→取整→左补0到6位）
select lpad(round(rand()*1000000,0),6,'0');
```

### 日期函数

| 函数 | 作用 |
| :--- | :--- |
| `curdate()` / `curtime()` | 当前日期 / 当前时间 |
| `now()` | 当前日期 + 时间 |
| `year(d)` / `month(d)` / `day(d)` | 提取日期的年 / 月 / 日 |
| `date_add(d, interval 值 单位)` | 在日期上加上一个间隔 |
| `datediff(d1, d2)` | 两个日期相差的天数（d1 - d2） |

```sql
select curdate();                                  # 当前日期
select curtime();                                  # 当前时间
select now();                                      # 当前日期时间
select year(now());                                # 今年的年份
select month(now());                               # 当前月份
select day(now());                                 # 今天是几号
select date_add(now(), interval 2 month);          # 当前时间往后推 2 个月
select datediff('2026-12-01','2026-11-15');        # → 16 天

# 实战：算每个员工入职到现在多少天，按天数倒序（工龄短的排前面）
select name, datediff(curdate(), entrydate) as 'entrydays'
from emp
order by entrydays desc;
```

### 流程函数（if / case）

可以在 SQL 里写「判断」，不用把数据搬到程序里再算。

```sql
select if(true,'OK','Error');          # if(条件, 真值, 假值) → OK
select ifnull('','Default');           # ifnull(a, b)：a 为 null 就返回 b
select ifnull(null,'Default');         # → Default

# case ... when 做「等值判断」：
# 语法：case 字段 when 值1 then 结果1 when 值2 then 结果2 ... else 兜底结果 end
select name,
       (case workaddress when '北京' then '一线城市' when '上海' then '一线城市' else '二线城市' end) as '工作地址'
from emp;
```

再来一个更常用的 case 写法——**搜索式 case**（when 后面直接写条件），顺便认识一下建表 + 造数 + 查询的完整流程：

```sql
# 先建一张学员成绩表
create table score(
    id      int         comment 'ID',
    name    varchar(20) comment '姓名',
    math    int         comment '数学',
    english int         comment '英语',
    chinese int         comment '语文'
) comment '学员成绩表';

# 插入 3 条成绩数据
insert into score(id, name, math, english, chinese)
values (1, 'Tom', 67, 88, 95),
       (2, 'Rose', 23, 66, 90),
       (3, 'Jack', 56, 98, 76);

# 用 case when 把每科分数转成 优秀/及格/不及格 三个等级
# 语法：case when 条件1 then 结果1 when 条件2 then 结果2 ... else 兜底 end
select
    id,
    name,
    (case when math    >= 85 then '优秀' when math    >= 60 then '及格' else '不及格' end) '数学',
    (case when english >= 85 then '优秀' when english >= 60 then '及格' else '不及格' end) '英语',
    (case when chinese >= 85 then '优秀' when chinese >= 60 then '及格' else '不及格' end) '语文'
from score;
```

## 🔒 约束

约束就是给表的字段加一堆「规矩」：哪些数据能存、哪些不能存，数据库直接帮你把第一道关，省得脏数据进表。先把常用约束过一遍：

| 约束 | 关键字 | 作用 |
| :--- | :--- | :--- |
| 非空约束 | `not null` | 该字段的值不能是 null |
| 唯一约束 | `unique` | 该字段的值不能重复（null 除外） |
| 主键约束 | `primary key` | 主键：非空 + 唯一，每行数据的「身份证」 |
| 默认约束 | `default 值` | 没传值时，用这个默认值顶上 |
| 自增约束 | `auto_increment` | 数值自动 +1（一般配主键用） |
| 检查约束 | `check` | 按条件检查，不满足就不让存 |
| 外键约束 | `foreign key` | 让本表字段引用另一张表的主键（见下节） |

### 约束演示

```sql
-- 建一张 user 表，把上面的约束挨个用上
-- 语法：字段名 类型 [primary key] [auto_increment] [not null] [unique] [default 值] [check(条件)] [comment '注释']
create table user(
    id     int primary key auto_increment comment 'id主键',      -- 主键 + 自增：id 不用手动传
    name   varchar(10) not null unique comment '姓名',           -- 非空 + 唯一：不能空、不能重名
    age    int check ( age > 0 && age <= 120 ) comment '年龄',   -- 检查：年龄必须 1~120 之间
    status char(1) default '1' comment '状态',                   -- 默认：没传就用 '1'
    gender char(1) comment '性别'
) comment '用户表';
```

接下来这几条 insert 是**故意用来触发各种约束报错**的，一条条复制执行，看它拦住了谁 👇

```sql
-- ✅ 正常插入（两条一起插）
insert into user(name, age, status, gender) values ('TOM1', 19, '1', '男'), ('TOM2', 25, '0', '男');
-- ✅ 正常插入
insert into user(name, age, status, gender) values ('TOM3', 19, '1', '男');

-- ❌ TOM3 已经存在了，name 违反 unique 唯一约束 → 报错
insert into user(name, age, status, gender) values ('TOM3', 20, '1', '男');
-- ❌ name 给了 null，违反 not null 非空约束 → 报错（age=-1 其实也违反 check）
insert into user(name, age, status, gender) values (null, -1, '1', '男');
-- ❌ age=122 超出 120，违反 check 检查约束 → 报错
insert into user(name, age, status, gender) values ('TOM5', 122, '1', '男');
-- ❌ age=-1 违反 check → 报错
insert into user(name, age, status, gender) values ('TOM5', -1, '1', '男');
-- ❌ 左边写了 4 个字段（name,age,status,gender），右边却只给了 3 个值 → 字段数和值数对不上，语法层面就报错
insert into user(name, age, status, gender) values ('TOM5', -1, '男');
```

> ⚠️ 表名叫 `user` 会和 MySQL 自带的 `mysql.user` 系统表有点撞名，练习能跑就行，**正式项目建议叫 `tb_user`** 更安全。
> 💡 `check` 约束在 **MySQL 8.0.16 之后才真正生效**，再老的版本只做语法解析、不拦截数据，如果发现 check 没拦住，先检查版本。

### 外键约束

外键让两张表产生「引用关系」：比如每个员工都必须属于一个真实存在的部门，`emp.dept_id` 只能指向 `dept` 表里有的部门 id，孤儿数据就别想进来。

> 💡 先声明：下面会用到 `dept`（部门）和 `emp`（员工）两张表。如果上一步你已经建过 `user` 表，下面第一段重复建 `user` 会报 `table already exists`——本小节用不到 user 表，**直接跳过那段就行**。

```sql
-- ====== 数据准备：部门表 ======
create table dept(
    id   int auto_increment comment 'ID' primary key,
    name varchar(50) not null comment '部门名称'
) comment '部门表';

insert into dept (id, name) values (1, '研发部'), (2, '市场部'), (3, '财务部'), (4, '销售部'), (5, '总经办');
select * from dept;   -- 先看一眼部门数据

-- ====== 数据准备：员工表 ======
-- 注意 dept_id 这一列：它就是待会要挂外键的「外键字段」
create table emp(
    id        int auto_increment comment 'ID' primary key,
    name      varchar(50) not null comment '姓名',
    age       int comment '年龄',
    job       varchar(20) comment '职位',
    salary    int comment '薪资',
    entrydate date comment '入职时间',
    managerid int comment '直属领导ID',
    dept_id   int comment '部门ID'
) comment '员工表';

insert into emp (id, name, age, job, salary, entrydate, managerid, dept_id) values
(1, '金庸', 66, '总裁', 20000, '2000-01-01', null, 5),
(2, '张无忌', 20, '项目经理', 12500, '2005-12-05', 1, 1),
(3, '杨逍', 33, '开发', 8400, '2000-11-03', 2, 1),
(4, '韦一笑', 48, '开发', 11000, '2002-02-05', 2, 1),
(5, '常遇春', 43, '开发', 10500, '2004-09-07', 3, 1),
(6, '小昭', 19, '程序员鼓励师', 6600, '2004-10-12', 2, 1);

-- 追加剩下 11 条记录，直接复制执行
insert into emp (id, name, age, job, salary, entrydate, managerid, dept_id) values
(7, '灭绝', 60, '财务总监', 8500, '2002-09-12', 1, 3),
(8, '周芷若', 19, '会计', 48000, '2006-06-02', 7, 3),
(9, '丁敏君', 23, '出纳', 5250, '2009-05-13', 7, 3),
(10, '赵敏', 20, '市场部总监', 12500, '2004-10-12', 1, 2),
(11, '鹿杖客', 56, '职员', 3750, '2006-10-03', 10, 2),
(12, '鹤笔翁', 19, '职员', 3750, '2007-05-09', 10, 2),
(13, '方东白', 19, '职员', 5500, '2009-02-12', 10, 2),
(14, '张三丰', 88, '销售总监', 14000, '2004-10-12', 1, 4),
(15, '俞莲舟', 38, '销售', 4600, '2004-10-12', 14, 4),
(16, '宋远桥', 40, '销售', 4600, '2004-10-12', 14, 4),
(17, '陈友谅', 42, null, 2000, '2011-10-12', 1, null);

select * from emp;   -- 看一眼员工数据
select * from dept;
```

给两张表加上外键，看语法：

```sql
-- 语法：alter table 子表 add constraint 约束名 foreign key (子表字段) references 父表(父表主键);
alter table emp add constraint fk_emp_dept_id foreign key (dept_id) references dept(id);
-- 效果：emp 的 dept_id 只能填 dept 表里真实存在的 id；不加 on update/on delete 时默认是 restrict（有员工引用的部门，禁止删/改）
```

> ⚠️ **约束名不能重复**：同一个库里 `fk_emp_dept_id` 只能存在一个。下面两段是「**两种外键行为二选一**」的演示，别一次性连着跑，想换一种就先把上一次的外键 drop 掉。

```sql
-- 删除外键：alter table 表名 drop foreign key 约束名;
alter table emp drop foreign key fk_emp_dept_id;

-- 演示①：on update cascade on delete cascade —— 部门主键更新/部门删除时，员工行跟着【级联】更新/删除
alter table emp add constraint fk_emp_dept_id foreign key (dept_id) references dept(id)
on update cascade on delete cascade;

-- 演示②：on update set null on delete set null —— 部门被删/被改时，员工对应的 dept_id 自动置为 null（保留员工，只是变成"无部门"）
alter table emp add constraint fk_emp_dept_id foreign key (dept_id) references dept(id)
on update set null on delete set null;
```

| 行为 | 效果 | 场景 |
| :--- | :--- | :--- |
| `restrict`（默认，不加动作） | 有员工引用的部门，禁止删除/修改主键 | 默认推荐，最安全 |
| `on delete cascade` | 删部门时，连带删除该部门的员工 | 部门没了员工也没意义 |
| `on delete set null` | 删部门时，员工保留、`dept_id` 变 null | 部门删了但员工还要留用 |

## 🔗 多表查询

前面 DQL 都是在**一张表**里折腾，但真实项目的数据是分散在好几张表里的：员工存员工表、部门存部门表，想查「张三属于哪个部门」就得把表**连起来**查，这就是多表查询。

先看表之间有哪几种「关系」：

- **一对多（多对一）**：一个部门有多个员工。在「多」的一方（员工表）加外键 `dept_id`，前面外键小节就是它。
- **多对多**：一个学生可以选多门课，一门课有多个学生。需要一张**中间表**来记录对应关系。
- **一对一**：一个用户的身份证信息就一条。任意一方加外键并约束为 `unique` 即可。

### 多表查询-多表关系（建演示数据）

下面这几张表专门用来演示三种关系，建完不用纠结，重点是看懂结构：

```sql
-- ====== 多对多：学生 ↔ 课程（需要中间表 student_course） ======
create table student(
    id   int auto_increment primary key comment '主键ID',
    name varchar(10) comment '姓名',
    no   varchar(10) comment '学号'
) comment '学生表';

insert into student values (null, '黛绮丝', '2000100101'), (null, '谢逊', '2000100102'), (null, '殷天正', '2000100103'), (null, '韦一笑', '2000100104');

create table course(
    id   int auto_increment primary key comment '主键ID',
    name varchar(10) comment '课程名称'
) comment '课程表';

insert into course values (null, 'Java'), (null, 'PHP'), (null, 'MySQL'), (null, 'Hadoop');

-- 中间表：只存「哪个学生选了哪门课」两个外键，把两边关联起来
create table student_course(
    id        int auto_increment comment '主键' primary key,
    studentid int not null comment '学生ID',
    courseid  int not null comment '课程ID',
    constraint fk_courseid  foreign key (courseid)  references course (id),
    constraint fk_studentid foreign key (studentid) references student (id)
) comment '学生课程中间表';

insert into student_course values (null, 1, 1), (null, 1, 2), (null, 1, 3), (null, 2, 2), (null, 2, 3), (null, 3, 4);

-- ====== 一对一：用户基本信息 ↔ 用户教育信息（userid 加了 unique，一条用户最多一条学历信息） ======
create table tb_user(
    id     int auto_increment primary key comment '主键ID',
    name   varchar(10) comment '姓名',
    age    int comment '年龄',
    gender char(1) comment '1: 男 , 2: 女',
    phone  char(11) comment '手机号'
) comment '用户基本信息表';

create table tb_user_edu(
    id            int auto_increment primary key comment '主键ID',
    degree        varchar(20) comment '学历',
    major         varchar(50) comment '专业',
    primaryschool varchar(50) comment '小学',
    middleschool  varchar(50) comment '中学',
    university    varchar(50) comment '大学',
    userid        int unique comment '用户ID',   -- unique 就保证了「一对一」
    constraint fk_userid foreign key (userid) references tb_user(id)
) comment '用户教育信息表';

insert into tb_user(id, name, age, gender, phone) values
(null, '黄渤', 45, '1', '18800001111'),
(null, '冰冰', 35, '2', '18800002222'),
(null, '码云', 55, '1', '18800008888'),
(null, '李彦宏', 50, '1', '18800009999');

insert into tb_user_edu(id, degree, major, primaryschool, middleschool, university, userid) values
(null, '本科', '舞蹈', '静安区第一小学', '静安区第一中学', '北京舞蹈学院', 1),
(null, '硕士', '表演', '朝阳区第一小学', '朝阳区第一中学', '北京电影学院', 2),
(null, '本科', '英语', '杭州市第一小学', '杭州市第一中学', '杭州师范大学', 3),
(null, '本科', '应用数学', '阳泉第一小学', '阳泉区第一中学', '清华大学', 4);
```

### 多表查询-笛卡尔积

直接拿两张表一起查会得到一个「**笛卡尔积**」：17 个员工 × 5 个部门 = 85 行大杂烩，绝大多数是没意义的乱配对 👇

```sql
-- ❌ 没有任何连接条件：emp 每一行都跟 dept 每一行配一遍 = 笛卡尔积（17 × 5 = 85 行）
select * from emp, dept;
```

怎么消除？加一个连接条件，让两表按「部门对得上」来配对：

```sql
-- ✅ 加上连接条件：只保留 emp.dept_id = dept.id 的行，剩下的才是「员工 + 自己部门」
select * from emp, dept where emp.dept_id = dept.id;
```

### 多表查询-内连接 / 外连接 / 自连接

继续用外键小节那两张 `dept` / `emp` 表（**没建的话先回去跑一遍数据准备**）。

```sql
-- ====== 内连接：只返回两表【都能对上】的行（有部门的员工） ======
-- 隐式内连接（where 写法）：select 字段 from 表A, 表B where 连接条件;
select emp.name, dept.name from emp, dept where emp.dept_id = dept.id;

-- 显式内连接（join 写法，更推荐）：select 字段 from 表A inner join 表B on 连接条件;
select emp.name, dept.name from emp inner join dept on emp.dept_id = dept.id;

-- ====== 外连接：保留一边的【全部】行，另一边没有就用 null 补齐 ======
-- 左连接：保留左表 emp 全部 17 人，没有部门的员工（陈友谅 dept_id 为 null）也会出现，dept 那边显示 null
select e.*, d.name from emp e left join dept d on e.dept_id = d.id;

-- 右连接：保留右表 dept 全部 5 个部门，员工对不上就用 null 补齐
select d.*, e.* from emp e right join dept d on e.dept_id = d.id;

-- ====== 自连接：自己跟自己连（员工表里靠 managerid 指认领导） ======
-- 同一张表起两个别名 a、b，就能当两张表用
-- 隐式写法（内连接效果）：金庸是董事长没有领导，不会被查出
select a.name, b.name from emp a, emp b where a.managerid = b.id;

-- 左连接写法：把没有领导的（金庸）也保留下来，领导列显示 null
select a.name '员工', b.name '领导' from emp a left join emp b on a.managerid = b.id;
```

> 💡 一句话区分：**内连接 = 两边都有才算；左连接 = 左表全要、右表尽力配；右连接 = 右表全要、左表尽力配。** 实际开发里左连接最常用。

### 多表查询-联合查询（union）

把多条 select 的**结果上下拼起来**，注意拼的两段列数、列类型要一致：

```sql
-- 需求：把「工资 < 5000 的人」和「年龄 > 50 的人」拼在一起查
-- 鹿杖客工资 3750 又年龄 56，两段都会命中他

-- union all：直接上下拼接，不去重（鹿杖客会出现两次，共 9 行）
select * from emp where salary < 5000
union all
select * from emp where age > 50;

-- union：拼接并【去重】（鹿杖客只留一次，共 8 行）
select * from emp where salary < 5000
union
select * from emp where age > 50;
```

### 多表查询-子查询

子查询就是**嵌套在别的 SQL 里的 select**（套娃查询 😆）。按子查询返回的结果分成四种，先记个表：

| 类型 | 子查询返回的结果 | 常用关键字 |
| :--- | :--- | :--- |
| 标量子查询 | 单行单列（一个值） | `=` `>` `<` 等比较符 |
| 列子查询 | 单列多行（一列值） | `in` / `any` / `all` / `some` |
| 行子查询 | 单行多列（一行记录） | `=` 配合 `(a, b) = (...)` |
| 表子查询 | 多行多列（一张临时表） | 放到 `from` 后面当表用 |

```sql
-- ====== 标量子查询：查「销售部」有哪些员工 ======
-- 先查出销售部的 id（1 个值），再拿它当条件去查 emp
select * from emp where dept_id = (select id from dept where name = '销售部');

-- 子查询也常配合比较符：查入职时间比「方东白」晚的员工
select * from emp where entrydate > (select entrydate from emp where name = '方东白');

-- ====== 列子查询：查「销售部或市场部」的员工 ======
-- in：命中子查询返回的任意一个 id 就行
select * from emp where dept_id in (select id from dept where name = '销售部' or name = '市场部');

-- all：和子查询返回的【所有值】比，相当于比最大值还大 —— 查比财务部所有人工资都高的员工
select salary from emp where dept_id = (select id from dept where name = '财务部');
select * from emp where salary > all (select salary from emp where dept_id = (select id from dept where name = '财务部'));
-- 📌 注意：财务部里会计周芷若工资高达 48000，没人比她还高，所以这条结果会是【空表】——空不是报错，是正常的！

-- any：和子查询返回的【任意一个值】比，相当于比最小值大就行 —— 查比研发部任意一人工资高的员工
select salary from emp where dept_id = (select id from dept where name = '研发部');
select * from emp where salary > any (select salary from emp where dept_id = (select id from dept where name = '研发部'));

-- ====== 行子查询：查和张无忌「工资 + 直属领导」都一样的员工 ======
select salary, managerid from emp where name = '张无忌';
-- 用一行来整体比较：字段顺序要和子查询 select 的一致
select * from emp where (salary, managerid) = (select salary, managerid from emp where name = '张无忌');

-- ====== 表子查询：把子查询结果当成一张【临时表】来 join（必须起别名 e） ======
-- 先看 2006 年之后入职的有谁
select * from emp where entrydate > '2006-01-01';
-- 再把上面这坨结果包成一张表 e，去 left join 部门表
select * from (select * from emp where entrydate > '2006-01-01') e left join dept d on e.dept_id = d.id;
```

## 💱 事务

事务解决的是「**一组 SQL 必须要么全成功、要么全失败**」的问题。最经典的例子就是转账：A 扣 1000、B 加 1000，万一扣完钱那一步 B 加钱失败了，钱就凭空消失了——把这两步包成一个**事务**，只要有一步出错就整个回滚，钱就不会丢。

### 事务-操作演示

```sql
-- ====== 数据准备：账户表 ======
create table account(
    id    int auto_increment primary key comment '主键ID',
    name  varchar(10) comment '姓名',
    money int comment '余额'
) comment '账户表';

insert into account(id, name, money) values (null, '张三', 2000), (null, '李四', 2000);

-- 恢复数据：方便你反复演示（把两个账户余额都改回 2000）
update account set money = 2000 where name = '张三' or name = '李四';

-- 默认 MySQL 是「自动提交」的，每条 SQL 自己就是一个小事务
select @@autocommit;        -- 查看自动提交开关：1 = 开启
set @@autocommit = 0;       -- 关闭自动提交：之后必须手动 commit 才会落库（仅当前会话生效）

-- ====== 手动控制事务三步走：开启 → 执行操作 → 提交/回滚 ======
start transaction;          -- ① 开启事务

update account set money = money - 1000 where name = '张三';   -- ② 张三扣 1000
update account set money = money + 1000 where name = '李四';   -- ② 李四加 1000

commit;                     -- ③ 全部成功 → 提交，数据真正写入
rollback;                   -- ③ 如果中间哪步出错了 → 回滚，所有操作作废（数据回到开启事务前的状态）
```

> ⚠️ `commit` 和 `rollback` 是**二选一**的，不是都执行！上面演示先 commit 了，后面的 rollback 已经没有意义（事务都提交了）。想试回滚效果，就把 `commit` 那行换成 `rollback`，再 `select * from account;` 看看余额是不是没变。

### 事务-四大特性（ACID）

| 特性 | 英文 | 通俗理解 |
| :--- | :--- | :--- |
| **原子性** | Atomicity | 事务里的操作要么全成、要么全没，不可分割 |
| **一致性** | Consistency | 事务前后数据总量不变（钱不会多也不会少） |
| **隔离性** | Isolation | 多个事务同时跑时互不干扰 |
| **持久性** | Durability | 提交后数据永久保存，断电重启也不丢 |

### 事务-并发事务问题

两个事务同时操作同一批数据时，就可能出下面三个问题（多开两个命令行窗口才能演示出效果）：

- **脏读**：一个事务读到**另一个还没提交**的修改（读到的是"没定稿的脏数据"）。比如 A 改了钱还没 commit，B 就读到了。
- **不可重复读**：同一个事务内，两次读**同一行**，结果却不一样（因为中间有别人 commit 改了它）。
- **幻读**：同一个事务内，两次查**同一范围**，发现行数多了/少了，像见了鬼一样（因为中间有别人插入了新行）。

### 事务-隔离级别

数据库用「隔离级别」来权衡上面的问题，级别越高越安全、但并发性能也越差：

| 隔离级别 | 脏读 | 不可重复读 | 幻读 |
| :--- | :---: | :---: | :---: |
| `read uncommitted`（读未提交） | 可能 | 可能 | 可能 |
| `read committed`（读已提交） | 已解决 | 可能 | 可能 |
| `repeatable read`（可重复读，**MySQL 默认**） | 已解决 | 已解决 | 可能* |
| `serializable`（串行化） | 已解决 | 已解决 | 已解决 |

> *InnoDB 引擎在 `repeatable read` 下其实用间隙锁把幻读也基本挡住了，但理论上标准层面它仍不算彻底解决。
> 面试问到就背：**级别从低到高 = 读未提交 → 读已提交 → 可重复读 → 串行化**，MySQL 默认 `repeatable read`。

对应的 SQL 语句收个尾：

```sql
-- 语法：set [session | global] transaction isolation level 隔离级别;
set session transaction isolation level read committed;   -- 把当前会话隔离级别设为「读已提交」

-- 查看当前隔离级别（MySQL 8.0 用 transaction_isolation；5.7 是 tx_isolation）
select @@transaction_isolation;
```

## ✅ 写在最后

把全文最常见的语法浓缩成一张速查表，忘了随时回来瞄一眼：

| 想干嘛 | 一句话语法 |
| :--- | :--- |
| 建库 / 建表 | `create database 库名;` / `create table 表名(...);` |
| 增数据 | `insert into 表名(字段...) values (值...);` |
| 删数据 | `delete from 表名 where 条件;`（**别忘 where**） |
| 改数据 | `update 表名 set 字段=值 where 条件;`（**别忘 where**） |
| 查数据 | `select 字段 from 表名 where 条件 group by 分组 having 过滤 order by 排序 limit 分页;` |
| 表之间关联 | `select ... from 表A [left / inner] join 表B on 关联条件;` |
| 子查询 | `where 字段 in / = / > all / > any (select ...)`，或 `from (select ...) 别名` |
| 约束 | `primary key` / `not null` / `unique` / `default` / `check` / `foreign key` |
| 常用函数 | `concat / lower / substring / round / now / ifnull / case when` |
| 管用户权限 | `create user`、`grant`、`revoke` |
| 事务 | `start transaction;` 干活后 `commit;` 或 `rollback;` |

我踩过最大的坑就是 **update / delete 忘写 where**，一个回车下去整张表的数据就没了 😅，所以标题上大写加粗三遍：**where！where！where！**

希望这份速通笔记对你有帮助～SQL 是个熟能生巧的东西，多敲几遍自然就顺了。我们下一篇博客见！👋
