---
title: cs186学习-笔记1
tags: 
- database
- sql
- cs186
date: 2020-11-21 22:13
---

# intro
数据库是每个开发人员都绕不开的领域，并且数据库作为软三大系统软件之一，其中荟萃了几乎所有的计算机思想和工程技术，不论是从事任何领域，学习了解数据库的设计和实现都能有所收获。

[cs186](https://cs186berkeley.net/)这门课是数据库入门课，由浅入深的介绍了一个简单的数据库如何设计和实现的

## 准备工作
- 准备一个支持`sql`的数据库（sqlite，mysql，tidb等都行）
- 进入数据库命令行
- 创建一个表
```sql
CREATE TABLE person (name Text,age bigint,num_dogs bigint);
insert into person (name,`age`,num_dogs) values ('Ace',20,4),('Ada',18,3),('Ben',7,2),('Cho',27,3);
```
## 基本sql语句
进入数据库
```bash
sqlite3 test.db
sqlite> .header on
```
### 查询语句
基本格式：
```sql
SELECT <col> FROM <tbl>;
```
举例：
```sql
sqlite> SELECT name,num_dogs FROM person;
name|num_dogs
Ace|4
Ada|3
Ben|2
Cho|3
```
这里数据返回的顺序其实是不一定固定的，除非加上了`order by`子句

### 过滤数据
通常我们只是关系数据库中某些部分的数据，这是就需要将数据做一定的筛选，以满足我们的要求，`WHERE`子句就是一个很好的工具：
基本格式：
```sql
SELECT <cols> FROM <tbl> WHERE <predicate>
```
例如，上面的表中，如果我们只关心成年人拥有的狗的数量：
```sql
sqlite> SELECT name,age,num_dogs FROM person WHERE age >= 18;
name|age|num_dogs
Ace|20|4
Ada|18|3
Cho|27|3
```

### bool 操作
当有更复杂的条件时，可以使用`bool`操作符`AND, NOT, OR`，比如，这里我们想知道有3只以上的狗的成年人有哪些：
```sql
sqlite> SELECT name,age,num_dogs FROM person WHERE age >= 18 AND num_dogs > 3;
name|age|num_dogs
Ace|20|4
```

### NULL相关
NULL是一个特别的值，任意类型都可以赋值为`NULL`，因此需要时刻注意的是，任何值都可能是NULL，因此需要关注`NULL`的一些特性；
1. 任何和NULL的运算，得到的都是NULL，例如，如果x是NULL，那么`if x > 3`得到的也是NULL，甚至`x = NULL`也是NULL，如果要判断一个值是不是NULL，可以使用`IS NULL`或者`IS NOT NULL`
2. `NULL`在bool判断中，表示false
3. 在bool 操作中，如果表达式不对NULL值求值就能确定`true`或者`false`，那么该表达式为`true`或者`false`，否则，则为NULL

### 聚合
在包含`group by`的语句中，having和where的区别：
```sql
SELECT <cols> FROM <tbl>
WHERE <predicate> -- 在group by之前执行
GROUP BY <cols>
HAVING <predicate>; -- 在group by之后执行 
```
这里的执行顺序是：`from where -> group by -> having -> select`;

需要注意的是，聚合操作，会将多行结果变成一行，因此，如果sql语句中包含了group by和聚合函数，则select 的列，则只能是被聚合的列（即跟在group by后面的列或者在AVG,SUM等函数中的列）