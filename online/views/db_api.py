#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2017-11-06 10:13:37
# @Last Modified by:   Administrator
# @Last Modified time: 2017-12-21 09:06:48

# thePD = pd.DataFrame(list(table_Initiation.objects.values('立项识别码',
# '父项立项识别码')))

# from collections import Iterable
# isinstance('abc',Iterable) # 判断目标是否可迭代


from django.db import connection
import online.userConst as uc
from online.models import *
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import never_cache
from django.db.models import Count, Min, Max, Sum
import pandas as pd
import numpy as np
import hashlib
import sys
import json
import decimal
import datetime
import time
import oss2

# 格式化字符串


def thousands(n): return '{:>,.2f}'.format(n)


def percents(n): return '{:>.2f}'.format((n or 0) * 100) + '%'

# HASH加密函数


def hash_sha256(string):
    '''
        Return a RSA string.
    '''
    m = hashlib.sha256()
    m.update(string.encode('utf8'))
    return m.hexdigest()

# 将对象转化为字典


def classToDict(obj):
    '''
        Transfer a object to a dictionary.
    '''
    is_list = obj.__class__ == [].__class__
    is_set = obj.__class__ == set().__class__
    if is_list or is_set:
        obj_arr = []
        for o in obj:
            dict = {}
            dict.update(o.__dict__)
            obj_arr.append(dict)
        return obj_arr
    else:
        dict = {}
        dict.update(obj.__dict__)
        return dict

# Json的参数，用来转化date和decimal


class CJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
            # try:
            #     if len(str(obj).split('.')[1]) <= 2:    # 说明是浮点型
            #         return thousands(float(obj))
            #     else:   # 说明是百分比
            #         return percents(float(obj))
            # except:
            #     return float(obj)
        else:
            return json.JSONEncoder.default(self, obj)


def dictfetchall(cursor):
    '''
        Return all rows from a cursor as a dict
    '''
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

# 树型数据


def format_Details_By_Tree():
    # 预自建过程
    sql1 = '''
        CREATE TEMPORARY TABLE IF NOT EXISTS tmp_UDID_table (立项识别码 INT);
        '''
    sql2 = '''
        CREATE TEMPORARY TABLE IF NOT EXISTS tmp_pay_table (立项识别码 INT, 已分配概算 DECIMAL(12, 2), 已付款 DECIMAL(12, 2));
        '''
    sql3 = '''
        TRUNCATE TABLE tmp_UDID_table;
        '''
    sql4 = '''
        TRUNCATE TABLE tmp_pay_table;
        '''
    # 将自身的立项识别码及全部子项的立项识别码导入表tmp_UDID_table
    sql5 = '''
        DROP PROCEDURE IF EXISTS get_all_children;
        '''
    sql6 = '''
        CREATE PROCEDURE `get_all_children` (areaId INT)
        BEGIN
            DECLARE sTemp VARCHAR(4000);
            DECLARE sTempChd VARCHAR(4000);
            SET sTemp = '$';
            SET sTempChd = cast(areaId as char);
            INSERT INTO tmp_UDID_table (立项识别码) VALUES(areaId);
            WHILE sTempChd is not NULL DO
                SET sTemp = CONCAT(sTemp,',',sTempChd);
                INSERT INTO tmp_UDID_table (立项识别码) SELECT 立项识别码 FROM tabel_立项信息 WHERE FIND_IN_SET(父项立项识别码,sTempChd)>0;
                SELECT group_concat(立项识别码) INTO sTempChd FROM tabel_立项信息 WHERE FIND_IN_SET(父项立项识别码,sTempChd)>0;
            END WHILE;
        END;
    '''
    # 遍历立项信息表，将立项识别码-项下已付款存入临时表tmp_pay_table
    sql7 = '''
        drop procedure if exists proc_tmp;
        '''
    sql8 = '''
        create procedure `proc_tmp`()
        BEGIN
            declare done int default 0;
            declare UDID bigint;
            declare idCur cursor for select 立项识别码 from tabel_立项信息 ORDER BY 立项识别码;
            declare continue handler for not FOUND set done = 1;
            open idCur;
            REPEAT
                fetch idCur into UDID;
                if not done THEN
                    TRUNCATE TABLE tmp_UDID_table;
                    CALL get_all_children(UDID);
                    INSERT INTO tmp_pay_table (立项识别码, 已分配概算, 已付款)
                        (SELECT UDID,
                        (SELECT SUM(项目概算) FROM tabel_立项信息 WHERE 父项立项识别码=UDID),
                        ifnull(SUM(本次付款额),0) FROM tabel_付款信息 WHERE 立项识别码 IN (SELECT 立项识别码 FROM tmp_UDID_table));
                end if;
            until done end repeat;
            close idCur;
        END;
        '''
    sql9 = '''
        CALL proc_tmp();
    '''
    # 正式
    sql10 = '''SELECT           I.立项识别码 AS 立项识别码, ifnull(分项名称, 项目名称) AS 项目名称, 合同名称, 项目概算,
                                  已分配概算/项目概算 AS 概算已分配率, T.已付款/项目概算 AS 概算付款比,
                                  招标方式, 中标价, 合同值_最新值 AS 合同值, P.已付款/合同值_最新值 AS 合同付款比, T.已付款, 分包合同数量
                 FROM             (SELECT * FROM tabel_立项信息 ORDER BY 立项识别码) AS I
                       LEFT JOIN  tabel_招标信息 AS B ON I.立项识别码=B.立项识别码
                       LEFT JOIN  tabel_合同信息 AS C ON I.立项识别码=C.立项识别码
                       LEFT JOIN  (SELECT 立项识别码, COUNT(*) AS 分包合同数量 FROM tabel_分包合同信息 GROUP BY 立项识别码) AS D ON I.立项识别码=D.立项识别码
                       LEFT JOIN  (SELECT 立项识别码, SUM(本次付款额) AS 已付款 FROM tabel_付款信息 GROUP BY 立项识别码) AS P ON I.立项识别码=P.立项识别码
                       LEFT JOIN  tmp_pay_table AS T ON I.立项识别码=T.立项识别码
           '''
    sql11 = '''SELECT 立项识别码, 父项立项识别码 FROM tabel_立项信息'''
    with connection.cursor() as cursor:
        cursor.execute(sql1)
        cursor.execute(sql2)
        cursor.execute(sql3)
        cursor.execute(sql4)
        cursor.execute(sql5)
        cursor.execute(sql6)
        cursor.execute(sql7)
        cursor.execute(sql8)
        cursor.execute(sql9)
        cursor.execute(sql10)
        data = dictfetchall(cursor)
        cursor.execute(sql11)
        hierarchy = list(map(list, cursor.fetchall()))
    # 将列表形式的数据格式化成字典型的
    dict_data = {}
    for da in data:
        key = da.pop('立项识别码')
        dict_data[key] = da
    # 将层级数据结构转化为dataframe
    array_hierarchy = np.array(hierarchy)
    frame_hierarchy = pd.DataFrame(
        array_hierarchy, columns=['立项识别码', '父项立项识别码'])

    def get_All_Roots():
        frame = frame_hierarchy[frame_hierarchy['父项立项识别码'].isnull()]
        list_frame = frame['立项识别码'].values.tolist()
        return [[x, 0] for x in list_frame]

    def get_All_Children(UDID, deep=0):    # 只获取子代，不获得更深后代
        frame = frame_hierarchy[frame_hierarchy['父项立项识别码'] == UDID]
        list_frame = frame['立项识别码'].values.tolist()
        return [[x, deep + 1] for x in list_frame]
    # 开始迭代获取数据层级
    roots_info = get_All_Roots()
    # 访问这些根节点，取得每个根节点的所有子项，存入其中

    def fix_treeTable_datas(roots_info):
        # 取得逻辑骨架，再将细节附着在骨架上
        i = 0
        while i < len(roots_info):
            UDID = roots_info[i][0]
            deep = roots_info[i][1]
            children = get_All_Children(UDID, deep)
            if children:
                prefix = roots_info[:(i + 1)]
                suffix = roots_info[(i + 1):]
                roots_info = prefix + children + suffix
            i += 1
        for i in range(len(roots_info)):
            Id, Level = roots_info[i]
            roots_info[i] = {'立项识别码': Id, '层级': Level}
            roots_info[i].update(dict_data.get(Id))
        return roots_info
    return fix_treeTable_datas(roots_info)


def read_For_TreeList():
    # 正式
    sql = '''SELECT 立项识别码 AS Id, ifnull(分项名称, 项目名称) AS name, 父项立项识别码 AS PId
               FROM tabel_立项信息
           ORDER BY 立项识别码
          '''
    with connection.cursor() as cursor:
        cursor.execute(sql)
        return dictfetchall(cursor)


def old_read_For_TreeList():
    # 正式
    sql = '''SELECT 立项识别码 AS Id, ifnull(分项名称, 项目名称) AS name, 父项立项识别码 AS PId
               FROM tabel_立项信息
           ORDER BY 立项识别码
          '''
    with connection.cursor() as cursor:
        cursor.execute(sql)
        return dictfetchall(cursor)

# 单位管理


def read_For_Company_GridDialog(where_sql='', where_list=[], order_sql='', order_list=[]):
    sql = 'SELECT {} FROM tabel_单位信息 '.format(
        ', '.join(uc.CompanyColLabels)) + where_sql + ' ' + order_sql
    sql_list = where_list + order_list
    with connection.cursor() as cursor:
        cursor.execute(sql, sql_list)
        return dictfetchall(cursor)
        # return [list(x) for x in cursor.fetchall()]


def save_For_Company_GridDialog(**data):
    '''
        This function can insert/update data for table_Company.
        input data({'单位识别码': 1, '单位名称': '青岛X公司', ...}) which is a dictionary.
        return 'Done' if success;
        return Error Message if failed.
    '''
    # 参数合法性校验
    if not data:
        return '您未输入任何数据'
    # 参数数量校验
    if len(data) != len(uc.CompanyFields):
        return '参数数量(%d)错误，应为(%d)个' % (len(data), len(uc.CompanyFields))
    # 确保UDID是整数
    try:
        UDID = int(data.get('单位识别码') or 0)
    except Exception as e:
        return str(e)
    # 确保传入的参数类型正确
    dict_type = dict(zip(uc.CompanyFields, uc.CompanyFields_Type))
    for field, value in data.items():
        if field not in uc.CompanyFields:
            return '无法存储<%s>，请重新输入' % field
        _type = dict_type.get(field)
        if (_type == '整数型' and not (type(value) == type(1) or value is None))\
                or (_type == '浮点型' and not (type(value) == type(1.0) or type(value) == type(decimal.Decimal(1.0)) or type(value) == type(1) or value is None))\
                or (_type == '字符串型' and not (type(value) == type('abc') or value is None))\
                or (_type == '文本型' and not (type(value) == type('abc') or value is None)):
            return '<%s:%s>类型(%s)错误，应为<%s>，请检查' % (field, str(value), str(type(value)), _type)
        if _type == '日期型':
            try:
                data[field] = datetime.date(
                    *list(time.strptime(data.get(field), "%Y-%m-%d"))[:3])
            except Exception as e:
                return str(e)
    # 判断应该用insert还是update
    try:
        if UDID > 0:    # UDID存在，说明应该update
            # 确保该项存在
            flag = not table_Company.objects.filter(单位识别码=UDID)
            if flag:
                return '单位识别码为<%d>的记录尚不存在，无法修改，请检查' % UDID
            # 数据合法性校验（是否存在重码）
            flag = table_Company.objects.filter(
                单位名称__exact=data.get('单位名称')).exclude(单位识别码=UDID)
            if flag:
                return '<%s>已存在，请检查' % data.get('单位名称')
            flag = table_Company.objects.filter(
                单位识别码__exact=UDID).update(**data)
            if flag:
                return 'Done'
        else:           # UDID不存在，说明应该insert
            # 数据合法性校验（是否存在重码）
            flag = table_Company.objects.filter(单位名称__exact=data.get('单位名称'))
            if flag:
                return '<%s>已存在，请检查' % data.get('单位名称')
            # 数据合法性校验（是否未输入单位名称）
            flag = not data.get('单位名称')
            if flag:
                return '<单位名称>未填写，请检查'
            flag = table_Company.objects.create(**data)
            if flag:
                return 'Done'
    except Exception as e:
        return str(e)

# 立项管理


def read_For_Initiation_GridDialog(where_sql='', where_list=[], order_sql='ORDER BY 立项识别码', order_list=[]):
    # 预自建过程
    sql1 = '''
        CREATE TEMPORARY TABLE IF NOT EXISTS tmp_UDID_table (立项识别码 INT);
        '''
    sql2 = '''
        CREATE TEMPORARY TABLE IF NOT EXISTS tmp_pay_table (立项识别码 INT, 已分配概算 DECIMAL(12, 2), 已付款 DECIMAL(12, 2));
        '''
    sql2_5 = '''
        CREATE TEMPORARY TABLE IF NOT EXISTS tmp_parent_pay_table (立项识别码 INT, 已分配概算 DECIMAL(12, 2), 已付款 DECIMAL(12, 2));
        '''
    sql3 = '''
        TRUNCATE TABLE tmp_UDID_table;
        '''
    sql4 = '''
        TRUNCATE TABLE tmp_pay_table;
        '''
    sql4_5 = '''
        TRUNCATE TABLE tmp_parent_pay_table;
        '''
    # 将自身的立项识别码及全部子项的立项识别码导入表tmp_UDID_table
    sql5 = '''
        DROP PROCEDURE IF EXISTS get_all_children;
        '''
    sql6 = '''
        CREATE PROCEDURE `get_all_children` (areaId INT)
        BEGIN
            DECLARE sTemp VARCHAR(4000);
            DECLARE sTempChd VARCHAR(4000);
            SET sTemp = '$';
            SET sTempChd = cast(areaId as char);
            INSERT INTO tmp_UDID_table (立项识别码) VALUES(areaId);
            WHILE sTempChd is not NULL DO
                SET sTemp = CONCAT(sTemp,',',sTempChd);
                INSERT INTO tmp_UDID_table (立项识别码) SELECT 立项识别码 FROM tabel_立项信息 WHERE FIND_IN_SET(父项立项识别码,sTempChd)>0;
                SELECT group_concat(立项识别码) INTO sTempChd FROM tabel_立项信息 WHERE FIND_IN_SET(父项立项识别码,sTempChd)>0;
            END WHILE;
        END;
    '''
    # 遍历立项信息表，将立项识别码-项下已付款存入临时表tmp_pay_table
    sql7 = '''
        drop procedure if exists proc_tmp;
        '''
    sql8 = '''
        create procedure `proc_tmp`()
        BEGIN
            declare done int default 0;
            declare UDID bigint;
            declare idCur cursor for select 立项识别码 from tabel_立项信息 ORDER BY 立项识别码;
            declare continue handler for not FOUND set done = 1;
            open idCur;
            REPEAT
                fetch idCur into UDID;
                if not done THEN
                    TRUNCATE TABLE tmp_UDID_table;
                    CALL get_all_children(UDID);
                    INSERT INTO tmp_pay_table (立项识别码, 已分配概算, 已付款)
                        (SELECT UDID,
                        (SELECT SUM(项目概算) FROM tabel_立项信息 WHERE 父项立项识别码=UDID),
                        ifnull(SUM(本次付款额),0) FROM tabel_付款信息 WHERE 立项识别码 IN (SELECT 立项识别码 FROM tmp_UDID_table));
                    INSERT INTO tmp_parent_pay_table (立项识别码, 已分配概算, 已付款)
                        (SELECT UDID,
                        (SELECT SUM(项目概算) FROM tabel_立项信息 WHERE 父项立项识别码=UDID),
                        ifnull(SUM(本次付款额),0) FROM tabel_付款信息 WHERE 立项识别码 IN (SELECT 立项识别码 FROM tmp_UDID_table));
                end if;
            until done end repeat;
            close idCur;
        END;
        '''
    sql9 = '''
        CALL proc_tmp();
    '''
    # 正式
    # 编辑/etc/my.cnf文件，加入如下参数，重启mysql
    # sql_mode = "STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER"
    sql = '''SELECT {} FROM
             (SELECT           A.立项识别码, A.项目名称, A.分项名称, A.父项立项识别码, B.项目名称 AS 父项项目名称,
                               B.分项名称 AS 父项分项名称, 子项数量,
                               B.项目概算 AS 父项项目概算,
                               ifnull(B.项目概算, 0)-ifnull(TP.已分配概算, 0)+ifnull(A.项目概算, 0) AS 项目概算上限,
                               A.建设单位识别码, U1.单位名称 AS 建设单位名称, A.代建单位识别码, U2.单位名称 AS 代建单位名称,
                               A.立项文件名称, A.立项时间, A.项目概算, T.已分配概算, A.项目概算-T.已分配概算 AS 未分配概算,
                               T.已分配概算/A.项目概算 AS 概算分配比, T.已付款 AS 概算已付款额, A.项目概算-T.已付款 AS 概算可付余额,
                               T.已付款/A.项目概算 AS 概算付款比, A.立项备注
              FROM             tabel_立项信息 AS A
                   LEFT JOIN   tabel_立项信息 AS B  ON A.父项立项识别码=B.立项识别码
                   LEFT JOIN   (SELECT 父项立项识别码, COUNT(*) AS 子项数量 FROM tabel_立项信息 GROUP BY 父项立项识别码) AS C ON A.立项识别码=C.父项立项识别码
                   LEFT JOIN   tabel_单位信息 AS U1 ON A.建设单位识别码=U1.单位识别码
                   LEFT JOIN   tabel_单位信息 AS U2 ON A.代建单位识别码=U2.单位识别码
                   LEFT JOIN   tmp_pay_table AS T ON A.立项识别码=T.立项识别码
                   LEFT JOIN   tmp_parent_pay_table AS TP ON A.父项立项识别码=TP.立项识别码
             ) AS Origin
          '''.format(', '.join(uc.InitiationColLabels)) + where_sql + ' ' + order_sql
    sql_list = where_list + order_list
    with connection.cursor() as cursor:
        cursor.execute(sql1)
    with connection.cursor() as cursor:
        cursor.execute(sql2)
    with connection.cursor() as cursor:
        cursor.execute(sql2_5)
    with connection.cursor() as cursor:
        cursor.execute(sql3)
    with connection.cursor() as cursor:
        cursor.execute(sql4)
    with connection.cursor() as cursor:
        cursor.execute(sql4_5)
    with connection.cursor() as cursor:
        cursor.execute(sql5)
    with connection.cursor() as cursor:
        cursor.execute(sql6)
    with connection.cursor() as cursor:
        cursor.execute(sql7)
    with connection.cursor() as cursor:
        cursor.execute(sql8)
    with connection.cursor() as cursor:
        cursor.execute(sql9)
    with connection.cursor() as cursor:
        cursor.execute(sql, sql_list)
        return dictfetchall(cursor)


def save_For_Initiation_GridDialog(**data):
    '''
        This function can insert/update data for table_Initiation.
        input data({'立项识别码': 1, '项目名称': '北王安置房', ...}) which is a dictionary.
        return 'Done' if success;
        return Error Message if failed.
    '''
    # 参数合法性校验
    if not data:
        return '您未输入任何数据'
    # 参数数量校验
    if len(data) != len(uc.InitiationFields):
        return '参数数量(%d)错误，应为(%d)个' % (len(data), len(uc.InitiationFields))
    # 确保UDID是整数
    try:
        UDID = int(data.get('立项识别码') or 0)
    except Exception as e:
        return str(e)
    # 确保传入的参数类型正确
    dict_type = dict(zip(uc.InitiationFields, uc.InitiationFields_Type))
    for field, value in data.items():
        if field not in uc.InitiationFields:
            return '无法存储<%s>，请重新输入' % field
        _type = dict_type.get(field)
        if (_type == '整数型' and not (type(value) == type(1) or value is None))\
                or (_type == '浮点型' and not (type(value) == type(1.0) or type(value) == type(1) or type(value) == type(decimal.Decimal(1.0)) or value is None))\
                or (_type == '字符串型' and not (type(value) == type('abc') or value is None))\
                or (_type == '文本型' and not (type(value) == type('abc') or value is None)):
            return '<%s:%s>类型(%s)错误，应为<%s>，请检查' % (field, str(value), str(type(value)), _type)
        elif _type == '日期型':
            try:
                data[field] = datetime.date(
                    *list(time.strptime(data.get(field), "%Y-%m-%d"))[:3])
            except Exception as e:
                return str(e)
    # 判断应该用insert还是update
    try:
        # 项目名称不应为空
        if not data.get('项目名称'):
            return '请输入<%s>字段' % '项目名称'
        # 如果有父项，项目名称应与父项项目名称一致
        parentUDID = data.get('父项立项识别码') or 0
        if parentUDID:
            project = data.get('项目名称')
            orm_init = table_Initiation.objects.filter(
                立项识别码=parentUDID).values()
            if orm_init:
                parent_project = orm_init[0].get('项目名称') or ''
                flag = project != parent_project
                if flag:
                    return '<项目名称>(%s)与<父项项目名称>(%s)不一致，请修改' % (project, parent_project)
        # 父项应为空，或父项的父项...应为空，否则说明有循环引用象
        for i in range(20):
            if not parentUDID:
                break
            orm_init = table_Initiation.objects.filter(
                立项识别码=parentUDID).values()
            if orm_init:
                parentUDID = orm_init[0].get('父项立项识别码')
            else:
                break
        else:
            return '该项深度超过20层或存在循环引用现象，请优化项目结构'
        # update
        if UDID > 0:
            # 确保该项存在
            flag = not table_Initiation.objects.filter(立项识别码=UDID)
            if flag:
                return '立项识别码为<%d>的记录尚不存在，无法修改，请检查' % UDID
            # 项目名称、分项名称不应有重复
            flag = table_Initiation.objects.filter(项目名称__exact=data.get(
                '项目名称'), 分项名称__exact=data.get('分项名称')).exclude(立项识别码=UDID)
            if flag:
                return '<%s-%s>已存在，请检查' % (data.get('项目名称'), (data.get('分项名称') or ''))
            # 查询一次数据库
            old_data = read_For_Initiation_GridDialog(
                'WHERE 立项识别码=%s', [UDID])[0]
            # 项目概算应>=已付款
            estimate = float(data.get('项目概算') or 0)
            payed_estimate = float(old_data.get('概算已付款额') or 0)
            if estimate < payed_estimate:
                return '<项目概算>(%f)过低，请调整为不低于<概算已付款额>(%f)' % (estimate, payed_estimate)
            # 项目概算应>=已分配概算
            estimate = float(data.get('项目概算') or 0)
            distributed_estimate = float(old_data.get('已分配概算') or 0)
            if estimate < distributed_estimate:
                return '<项目概算>(%f)过低，请调整为不低于<已分配概算>(%f)' % (estimate, distributed_estimate)
            # 父项存在时，项目概算应<= 项目概算上限
            parentUDID = data.get('父项立项识别码') or 0
            estimate = float(data.get('项目概算') or 0)
            old_estimate = float(old_data.get('项目概算') or 0)
            parent_data = read_For_Initiation_GridDialog(
                'WHERE 立项识别码=%s', [UDID])
            if parent_data:
                parent_estimate = float(parent_data[0].get('项目概算') or 0)
                parent_distributed_estimate = float(
                    parent_data[0].get('已分配概算') or 0)
                limit_estimate = float(
                    parent_estimate - parent_distributed_estimate + old_estimate)
                if estimate > limit_estimate:
                    return '<项目概算>(%f)过高，请调整为不高于(%f)' % (estimate, limit_estimate)
            # 正戏
            flag = table_Initiation.objects.filter(
                立项识别码__exact=UDID).update(**data)
            if flag:
                return 'Done'
        # insert
        else:
            # 确保项目名称、项目分项不重复
            flag = table_Initiation.objects.filter(
                项目名称__exact=data.get('项目名称'), 分项名称__exact=data.get('分项名称'))
            if flag:
                return '<%s-%s>已存在，请检查' % (data.get('项目名称'), (data.get('分项名称') or ''))
            # 父项存在时，项目概算应<= 父项概算-父项已分配概算
            parentUDID = data.get('父项立项识别码') or 0
            estimate = float(data.get('项目概算') or 0)
            parent_data = read_For_Initiation_GridDialog(
                'WHERE 立项识别码=%s', [UDID])
            if parent_data:
                parent_estimate = float(parent_data[0].get('项目概算') or 0)
                parent_distributed_estimate = float(
                    parent_data[0].get('已分配概算') or 0)
                limit_estimate = float(
                    parent_estimate - parent_distributed_estimate)
                if estimate > limit_estimate:
                    return '<项目概算>(%f)过高，请调整为不高于(%f)' % (estimate, limit_estimate)
            # 正戏
            flag = table_Initiation.objects.create(**data)
            if flag:
                return 'Done'
    except Exception as e:
        return str(e)


def get_All_Grandchildren(UDID):
    '''
        取得某项下全部子项、孙项等的立项识别码
    '''
    sql1 = '''
    	  set global log_bin_trust_function_creators=1;
          DROP FUNCTION IF EXISTS queryChildrenAreaInfo;
          '''
    sql2 = '''
          CREATE FUNCTION `queryChildrenAreaInfo` (areaId INT)
          RETURNS VARCHAR(4000)
          BEGIN
              DECLARE sTemp VARCHAR(4000);
              DECLARE sTempChd VARCHAR(4000);
              SET sTemp = '$';
              SET sTempChd = cast(areaId as char);
              WHILE sTempChd is not NULL DO
                  SET sTemp = CONCAT(sTemp,',',sTempChd);
                  SELECT group_concat(立项识别码) INTO sTempChd FROM tabel_立项信息 where FIND_IN_SET(父项立项识别码,sTempChd)>0;
              END WHILE;
              return sTemp;
          END;
          '''
    sql = '''SELECT queryChildrenAreaInfo(%s);'''
    sql_list = [UDID]
    with connection.cursor() as cursor:
        cursor.execute(sql1)
        cursor.execute(sql2)
    with connection.cursor() as cursor:
        cursor.execute(sql, sql_list)
        fetchall = cursor.fetchall()[0][0].split(',')[2:]
        return dictfetchall(cursor)

# 招标管理


def read_For_Bidding_GridDialog(where_sql='', where_list=[], order_sql='', order_list=[]):
    sql = '''SELECT {} FROM
                 (SELECT           招标识别码, A.立项识别码 AS 立项识别码, 项目名称, 分项名称,
                                   建设单位识别码, U4.单位名称 AS 建设单位名称, 代建单位识别码, U5.单位名称 AS 代建单位名称,
                                   招标方式, 招标单位识别码,
                                   U1.单位名称 AS 招标单位名称, 招标代理识别码, U2.单位名称 AS 招标代理单位名称, 项目概算,
                                   预算控制价, 招标文件定稿时间, 公告邀请函发出时间, 开标时间, 中标通知书发出时间,
                                   中标单位识别码, U3.单位名称 AS 中标单位名称, 中标价, 招标备注
                  FROM             tabel_招标信息 AS A
                       LEFT JOIN   tabel_立项信息 AS I ON A.立项识别码=I.立项识别码
                       LEFT JOIN   tabel_单位信息 AS U1 ON A.招标单位识别码=U1.单位识别码
                       LEFT JOIN   tabel_单位信息 AS U2 ON A.招标代理识别码=U2.单位识别码
                       LEFT JOIN   tabel_单位信息 AS U3 ON A.中标单位识别码=U3.单位识别码
                       LEFT JOIN   tabel_单位信息 AS U4 ON I.建设单位识别码=U4.单位识别码
                       LEFT JOIN   tabel_单位信息 AS U5 ON I.代建单位识别码=U5.单位识别码
                 ) AS Origin
          '''.format(', '.join(uc.BiddingColLabels)) + where_sql + ' ' + order_sql
    sql_list = where_list + order_list
    with connection.cursor() as cursor:
        cursor.execute(sql, sql_list)
        return dictfetchall(cursor)


def save_For_Bidding_GridDialog(**data):
    '''
        This function can insert/update data for table_Bidding.
        input data({'招标识别码': 1, '招标方式': '公开招标', ...}) which is a dictionary.
        return 'Done' if success;
        return Error Message if failed.
    '''
    # 参数合法性校验
    if not data:
        return '您未输入任何数据'
    # 参数数量校验
    if len(data) != len(uc.BiddingFields):
        return '参数数量(%d)错误，应为(%d)个' % (len(data), len(uc.BiddingFields))
    # 确保UDID是整数
    try:
        UDID = int(data.get('招标识别码') or 0)
    except Exception as e:
        return str(e)
    # 确保传入的参数类型正确
    dict_type = dict(zip(uc.BiddingFields, uc.BiddingFields_Type))
    for field, value in data.items():
        if field not in uc.BiddingFields:
            return '无法存储<%s>，请重新输入' % field
        _type = dict_type.get(field)
        if (_type == '整数型' and not (type(value) == type(1) or value is None))\
                or (_type == '浮点型' and not (type(value) == type(1.0) or type(value) == type(1) or type(value) == type(decimal.Decimal(1.0)) or value is None))\
                or (_type == '字符串型' and not (type(value) == type('abc') or value is None))\
                or (_type == '文本型' and not (type(value) == type('abc') or value is None)):
            return '<%s:%s>类型(%s)错误，应为<%s>，请检查' % (field, str(value), str(type(value)), _type)
        elif _type == '日期型':
            try:
                data[field] = datetime.date(
                    *list(time.strptime(data.get(field), "%Y-%m-%d"))[:3])
            except Exception as e:
                return str(e)
    # 判断应该用insert还是update
    try:
        # 立项识别码必须存在、对应的立项必须存在
        InitUDID = data.get('立项识别码') or 0
        Init_data = read_For_Initiation_GridDialog(
            'WHERE 立项识别码=%s', [InitUDID])
        flag = not (InitUDID and Init_data)
        if flag:
            return '立项信息错误'
        # 对应的立项不应有子项
        children_Count = Init_data[0].get('子项数量') or 0
        if children_Count:
            return '对应的立项不应有子项，请重新选择立项信息'
        # 预算控制价不应超过项目概算
        control_price = float(data.get('预算控制价') or 0)
        estimate = float(Init_data[0].get('项目概算') or 0)
        flag = control_price > estimate or control_price < 0
        if flag:
            return '<预算控制价>(%f)输入错误，请将值设置为[0, <项目概算>(%f)]之间' % (control_price, estimate)
        # 中标价不应超过预算控制价
        bid_price = float(data.get('中标价') or 0)
        control_price = float(data.get('预算控制价') or 0)
        flag = bid_price > control_price or bid_price < 0
        if flag:
            return '<中标价>(%f)输入错误，请将值设置为[0, <预算控制价>(%f)]之间' % (bid_price, control_price)
        # update
        if UDID > 0:
            # 确保该项存在
            flag = not table_Bidding.objects.filter(招标识别码=UDID)
            if flag:
                return '招标识别码为<%d>的记录尚不存在，无法修改，请检查' % UDID
            # 正戏
            flag = table_Bidding.objects.filter(
                招标识别码__exact=UDID).update(**data)
            if flag:
                return 'Done'
        # insert
        else:
            # 正戏
            flag = table_Bidding.objects.create(**data)
            if flag:
                return 'Done'
    except Exception as e:
        return str(e)

# 合同管理


def read_For_Contract_GridDialog(where_sql='', where_list=[], order_sql='', order_list=[]):
    sql = '''SELECT {} FROM
                 (SELECT           A.合同识别码, A.立项识别码, 项目名称, 分项名称, 项目概算,
                                   I.建设单位识别码, U7.单位名称 AS 建设单位名称, I.代建单位识别码, U8.单位名称 AS 代建单位名称,
                                   A.招标识别码, 招标方式,
                                   B.招标单位识别码, U5.单位名称 AS 招标单位名称, B.中标单位识别码, U6.单位名称 AS 中标单位名称,
                                   合同编号, 合同名称, 合同主要内容, 合同类别,
                                   甲方识别码, U1.单位名称 AS 甲方单位名称, 乙方识别码, U2.单位名称 AS 乙方单位名称,
                                   丙方识别码, U3.单位名称 AS 丙方单位名称, 丁方识别码, U4.单位名称 AS 丁方单位名称,
                                   中标价, 合同值_签订时, 合同值_最新值, 合同值_最终值,
                                   已付款, 已付款/项目概算 AS 已付款占概算,
                                   已付款/合同值_最新值 AS 已付款占合同, 形象进度, 支付上限, 合同签订时间,
                                   开工时间, 竣工合格时间, 保修结束时间, 审计完成时间, 合同备注
                  FROM             tabel_合同信息 AS A
                       LEFT JOIN   tabel_立项信息 AS I ON A.立项识别码=I.立项识别码
                       LEFT JOIN   tabel_单位信息 AS U1 ON A.甲方识别码=U1.单位识别码
                       LEFT JOIN   tabel_单位信息 AS U2 ON A.乙方识别码=U2.单位识别码
                       LEFT JOIN   tabel_单位信息 AS U3 ON A.丙方识别码=U3.单位识别码
                       LEFT JOIN   tabel_单位信息 AS U4 ON A.丁方识别码=U4.单位识别码
                       LEFT JOIN   tabel_招标信息 AS B ON A.招标识别码=B.招标识别码
                       LEFT JOIN   tabel_单位信息 AS U5 ON B.招标单位识别码=U5.单位识别码
                       LEFT JOIN   tabel_单位信息 AS U6 ON B.中标单位识别码=U6.单位识别码
                       LEFT JOIN   tabel_单位信息 AS U7 ON I.建设单位识别码=U7.单位识别码
                       LEFT JOIN   tabel_单位信息 AS U8 ON I.代建单位识别码=U8.单位识别码
                       LEFT JOIN   (SELECT 合同识别码, SUM(本次付款额) AS 已付款 FROM tabel_付款信息 GROUP BY 合同识别码) AS P ON A.合同识别码=P.合同识别码
                  ) AS Origin
          '''.format(', '.join(uc.ContractColLabels)) + where_sql + ' ' + order_sql
    sql_list = where_list + order_list
    with connection.cursor() as cursor:
        cursor.execute(sql, sql_list)
        return dictfetchall(cursor)


def save_For_Contract_GridDialog(**data):
    '''
        This function can insert/update data for table_Contract.
        input data({'合同识别码': 1, '合同名称': '建设工程XX合同', ...}) which is a dictionary.
        return 'Done' if success;
        return Error Message if failed.
    '''
    # 参数合法性校验
    if not data:
        return '您未输入任何数据'
    # 参数数量校验
    if len(data) != len(uc.ContractFields):
        return '参数数量(%d)错误，应为(%d)个' % (len(data), len(uc.ContractFields))
    # 确保UDID是整数
    try:
        UDID = int(data.get('招标识别码') or 0)
    except Exception as e:
        return str(e)
    # 确保传入的参数类型正确
    dict_type = dict(zip(uc.ContractFields, uc.ContractFields_Type))
    for field, value in data.items():
        if field not in uc.ContractFields:
            return '无法存储<%s>，请重新输入' % field
        _type = dict_type.get(field)
        if (_type == '整数型' and not (type(value) == type(1) or value is None))\
                or (_type == '浮点型' and not (type(value) == type(1.0) or type(value) == type(1) or type(value) == type(decimal.Decimal(1.0)) or value is None))\
                or (_type == '字符串型' and not (type(value) == type('abc') or value is None))\
                or (_type == '文本型' and not (type(value) == type('abc') or value is None)):
            return '<%s:%s>类型(%s)错误，应为<%s>，请检查' % (field, str(value), str(type(value)), _type)
        elif _type == '日期型':
            try:
                data[field] = datetime.date(
                    *list(time.strptime(data.get(field), "%Y-%m-%d"))[:3])
            except Exception as e:
                return str(e)
    # 判断应该用insert还是update
    try:
        # 立项识别码必须存在、对应的立项必须存在
        InitUDID = data.get('立项识别码') or 0
        Init_data = read_For_Initiation_GridDialog(
            'WHERE 立项识别码=%s', [InitUDID])
        flag = not (InitUDID and Init_data)
        if flag:
            return '立项信息错误'
        # 对应的立项不应有子项
        children_Count = Init_data[0].get('子项数量') or 0
        if children_Count:
            return '对应的立项不应有子项，请重新选择立项信息'
        # 招标识别码如果存在，应有对应招标项，招标项如果存在，应与立项信息相对应
        BiddingUDID = data.get('招标识别码') or 0
        Bidding_data = read_For_Bidding_GridDialog(
            'WHERE 招标识别码=%s', [BiddingUDID])
        flag = not (BiddingUDID and Bidding_data)
        if flag:
            return '招标信息错误'
        # 合同签订值应>=0，招标项如果存在，<=中标价，否则应<=项目概算
        sign_price = float(data.get('合同值_签订时') or 0)
        estimate   = float(Init_data.get('项目概算') or 0)
        bid_price  = float(Bidding_data.get('中标价') or 0)
        if Bidding_data:
            flag = sign_price < 0 or sign_price > bid_price
            if flag:
                return '<合同值_签订时>(%f)输入错误，请将值设置为[0, <中标价>(%f)]之间' % (sign_price, bid_price)
        else:
            flag = sign_price < 0 or sign_price > estimate
            if flag:
                return '<合同值_签订时>(%f)输入错误，请将值设置为[0, <项目概算>(%f)]之间' % (sign_price, estimate)
        # 合同最终值应不应<0
        final_price = float(data.get('合同值_最终值') or 0)
        flag = final_price < 0
        if flag:
            return '<合同值_最终值>(%f)输入错误，请将值设置为非负数' % final_price
        # 预算控制价不应超过项目概算
        # ======================================写到这儿啦===================================================================
        # 支付上限应<=合同最新值，>=合同已付款(若无该项，则为0)
        # 当合同最终值不存在时，合同最新值应>=项目已付款(若无该项，则为0)，<=项目概算，否则应=项目最终值
        # update
        if UDID > 0:
            # 确保该项存在
            flag = not table_Contract.objects.filter(合同识别码=UDID)
            if flag:
                return '合同识别码为<%d>的记录尚不存在，无法修改，请检查' % UDID
            # 正戏
            flag = table_Contract.objects.filter(
                合同识别码__exact=UDID).update(**data)
            if flag:
                return 'Done'
        # insert
        else:
            # 正戏
            flag = table_Contract.objects.create(**data)
            if flag:
                return 'Done'
    except Exception as e:
        return str(e)
# 分包合同管理


def read_For_SubContract_GridDialog(where_sql='', where_list=[], order_sql='', order_list=[]):
    sql = '''SELECT {} FROM
             (SELECT           分包合同识别码, A.立项识别码, 项目名称, 分项名称, A.合同识别码, 合同编号 AS 总包合同编号,
                               合同名称 AS 总包合同名称, 合同主要内容 AS 总包合同主要内容, 合同类别 AS 总包合同类别,
                               合同值_最新值 AS 总包合同值, 分包合同编号, 分包合同名称, 分包合同主要内容, 分包合同类别,
                               A.甲方识别码, U1.单位名称 AS 甲方单位名称, A.乙方识别码, U2.单位名称 AS 乙方单位名称,
                               A.丙方识别码, U3.单位名称 AS 丙方单位名称, A.丁方识别码, U4.单位名称 AS 丁方单位名称,
                               B.甲方识别码 AS 总包甲方识别码, U5.单位名称 AS 总包甲方单位名称, B.乙方识别码 AS 总包乙方识别码, U6.单位名称 AS 总包乙方单位名称,
                               B.丙方识别码 AS 总包丙方识别码, U7.单位名称 AS 总包丙方单位名称, B.丁方识别码 AS 总包丁方识别码, U8.单位名称 AS 总包丁方单位名称,
                               分包合同签订时间, 分包合同值_签订时, 分包合同值_最新值, 分包合同值_最终值, 分包合同备注
              FROM             tabel_分包合同信息 AS A
                   LEFT JOIN   tabel_立项信息 AS I ON A.立项识别码=I.立项识别码
                   LEFT JOIN   tabel_合同信息 AS B ON A.合同识别码=B.合同识别码
                   LEFT JOIN   tabel_单位信息 AS U1 ON A.甲方识别码=U1.单位识别码
                   LEFT JOIN   tabel_单位信息 AS U2 ON A.乙方识别码=U2.单位识别码
                   LEFT JOIN   tabel_单位信息 AS U3 ON A.丙方识别码=U3.单位识别码
                   LEFT JOIN   tabel_单位信息 AS U4 ON A.丁方识别码=U4.单位识别码
                   LEFT JOIN   tabel_单位信息 AS U5 ON B.甲方识别码=U5.单位识别码
                   LEFT JOIN   tabel_单位信息 AS U6 ON B.乙方识别码=U6.单位识别码
                   LEFT JOIN   tabel_单位信息 AS U7 ON B.丙方识别码=U7.单位识别码
                   LEFT JOIN   tabel_单位信息 AS U8 ON B.丁方识别码=U8.单位识别码) AS Origin
          '''.format(', '.join(uc.SubContractColLabels)) + where_sql + ' ' + order_sql
    sql_list = where_list + order_list
    with connection.cursor() as cursor:
        cursor.execute(sql, sql_list)
        return dictfetchall(cursor)

# 变更管理


def read_For_Alteration_GridDialog(where_sql='', where_list=[], order_sql='', order_list=[]):
    sql = '''SELECT {} FROM
             (SELECT           变更识别码, A.立项识别码, 项目名称, 分项名称, A.合同识别码, 合同编号,
                               合同名称, 合同类别, 合同值_签订时, 甲方识别码, U1.单位名称 AS 甲方单位名称, 乙方识别码, U2.单位名称 AS 乙方单位名称,
                               丙方识别码, U3.单位名称 AS 丙方单位名称, 丁方识别码, U4.单位名称 AS 丁方单位名称,
                               变更类型, 变更编号, 变更主题, 变更登记日期, 变更生效日期,
                               变更原因, 预估变更额度, 预估变更额度/合同值_签订时 AS 预估变更率, 变更额度, 变更额度/合同值_签订时 AS 变更率, 变更备注
              FROM             tabel_变更信息 AS A
                   LEFT JOIN   tabel_立项信息 AS I ON A.立项识别码=I.立项识别码
                   LEFT JOIN   tabel_合同信息 AS C ON A.合同识别码=C.合同识别码
                   LEFT JOIN   tabel_单位信息 AS U1 ON C.甲方识别码=U1.单位识别码
                   LEFT JOIN   tabel_单位信息 AS U2 ON C.乙方识别码=U2.单位识别码
                   LEFT JOIN   tabel_单位信息 AS U3 ON C.丙方识别码=U3.单位识别码
                   LEFT JOIN   tabel_单位信息 AS U4 ON C.丁方识别码=U4.单位识别码) AS Origin
          '''.format(', '.join(uc.AlterationColLabels)) + where_sql + ' ' + order_sql
    sql_list = where_list + order_list
    with connection.cursor() as cursor:
        cursor.execute(sql, sql_list)
        return dictfetchall(cursor)

# 预算管理


def read_For_Budget_GridDialog(where_sql='', where_list=[], order_sql='ORDER BY 预算识别码', order_list=[]):
    # 预自建过程
    sql1 = '''
        CREATE TEMPORARY TABLE IF NOT EXISTS tmp_UDID_table (预算识别码 INT);
        '''
    sql2 = '''
        CREATE TEMPORARY TABLE IF NOT EXISTS tmp_pay_table (预算识别码 INT, 已分配预算 DECIMAL(12, 2), 已付款 DECIMAL(12, 2));
        '''
    sql2_5 = '''
        CREATE TEMPORARY TABLE IF NOT EXISTS tmp_parent_pay_table (预算识别码 INT, 已分配预算 DECIMAL(12, 2), 已付款 DECIMAL(12, 2));
        '''
    sql3 = '''
        TRUNCATE TABLE tmp_UDID_table;
        '''
    sql4 = '''
        TRUNCATE TABLE tmp_pay_table;
        '''
    sql4_5 = '''
        TRUNCATE TABLE tmp_parent_pay_table;
        '''
    # 将自身的立项识别码及全部子项的立项识别码导入表tmp_UDID_table
    sql5 = '''
        DROP PROCEDURE IF EXISTS get_all_children;
        '''
    sql6 = '''
        CREATE PROCEDURE `get_all_children` (areaId INT)
        BEGIN
            DECLARE sTemp VARCHAR(4000);
            DECLARE sTempChd VARCHAR(4000);
            SET sTemp = '$';
            SET sTempChd = cast(areaId as char);
            INSERT INTO tmp_UDID_table (预算识别码) VALUES(areaId);
            WHILE sTempChd is not NULL DO
                SET sTemp = CONCAT(sTemp,',',sTempChd);
                INSERT INTO tmp_UDID_table (预算识别码) SELECT 预算识别码 FROM tabel_预算信息 WHERE FIND_IN_SET(父项预算识别码,sTempChd)>0;
                SELECT group_concat(预算识别码) INTO sTempChd FROM tabel_预算信息 WHERE FIND_IN_SET(父项预算识别码,sTempChd)>0;
            END WHILE;
        END;
    '''
    # 遍历预算信息表，将预算识别码-项下已付款存入临时表tmp_pay_table
    sql7 = '''
        drop procedure if exists proc_tmp;
        '''
    sql8 = '''
        create procedure `proc_tmp`()
        BEGIN
            declare done int default 0;
            declare UDID bigint;
            declare idCur cursor for select 预算识别码 from tabel_预算信息 ORDER BY 预算识别码;
            declare continue handler for not FOUND set done = 1;
            open idCur;
            REPEAT
                fetch idCur into UDID;
                if not done THEN
                    TRUNCATE TABLE tmp_UDID_table;
                    CALL get_all_children(UDID);
                    INSERT INTO tmp_pay_table (预算识别码, 已分配预算, 已付款)
                        (SELECT UDID,
                        (SELECT SUM(预算总额) FROM tabel_预算信息 WHERE 父项预算识别码=UDID),
                        ifnull(SUM(本次付款额),0) FROM tabel_付款信息 WHERE 预算识别码 IN (SELECT 预算识别码 FROM tmp_UDID_table));
                    INSERT INTO tmp_parent_pay_table (预算识别码, 已分配预算, 已付款)
                        (SELECT UDID,
                        (SELECT SUM(预算总额) FROM tabel_预算信息 WHERE 父项预算识别码=UDID),
                        ifnull(SUM(本次付款额),0) FROM tabel_付款信息 WHERE 预算识别码 IN (SELECT 预算识别码 FROM tmp_UDID_table));
                end if;
            until done end repeat;
            close idCur;
        END;
        '''
    sql9 = '''
        CALL proc_tmp();
    '''
    # 正式
    sql = '''SELECT {} FROM
             (SELECT           A.预算识别码, A.预算名称, A.预算周期, A.预算总额,
                               A.父项预算识别码, B.预算名称 AS 父项预算名称, B.预算周期 AS 父项预算周期, 预算子项数量,
                               B.预算总额 AS 父项预算额,
                               ifnull(B.预算总额, 0)-ifnull(TP.已分配预算, 0)+ifnull(A.预算总额, 0) AS 预算上限,
                               T.已分配预算, A.预算总额-T.已分配预算 AS 未分配预算, T.已分配预算/A.预算总额 AS 预算分配比,
                               T.已付款 AS 预算已付额, A.预算总额-T.已付款 AS 预算余额, T.已付款/A.预算总额 AS 预算已付比,
                               A.预算备注
              FROM             tabel_预算信息 AS A
                   LEFT JOIN   tabel_预算信息 AS B  ON A.父项预算识别码=B.预算识别码
                   LEFT JOIN   (SELECT 父项预算识别码, COUNT(*) AS 预算子项数量 FROM tabel_预算信息 GROUP BY 父项预算识别码) AS C ON A.预算识别码=C.父项预算识别码
                   LEFT JOIN   tmp_pay_table AS T ON A.预算识别码=T.预算识别码
                   LEFT JOIN   tmp_parent_pay_table AS TP ON A.父项预算识别码=TP.预算识别码
                   ) AS Origin
          '''.format(', '.join(uc.BudgetColLabels)) + where_sql + ' ' + order_sql
    sql_list = where_list + order_list
    with connection.cursor() as cursor:
        cursor.execute(sql1)
    with connection.cursor() as cursor:
        cursor.execute(sql2)
    with connection.cursor() as cursor:
        cursor.execute(sql2_5)
    with connection.cursor() as cursor:
        cursor.execute(sql3)
    with connection.cursor() as cursor:
        cursor.execute(sql4)
    with connection.cursor() as cursor:
        cursor.execute(sql4_5)
    with connection.cursor() as cursor:
        cursor.execute(sql5)
    with connection.cursor() as cursor:
        cursor.execute(sql6)
    with connection.cursor() as cursor:
        cursor.execute(sql7)
    with connection.cursor() as cursor:
        cursor.execute(sql8)
    with connection.cursor() as cursor:
        cursor.execute(sql9)
    with connection.cursor() as cursor:
        cursor.execute(sql, sql_list)
        return dictfetchall(cursor)


def read_Budget_For_TreeList():
    # 正式
    sql = '''SELECT 预算识别码 AS Id, CONCAT(ifnull(预算名称, ''), ifnull(预算周期, '')) AS name, 父项预算识别码 AS PId
               FROM tabel_预算信息
           ORDER BY 预算识别码
          '''
    with connection.cursor() as cursor:
        cursor.execute(sql)
        return dictfetchall(cursor)


def format_Budget_Details_By_Tree():
    sql1 = '''SELECT 预算识别码, 预算名称, 预算周期, 预算总额 FROM tabel_预算信息'''
    sql2 = '''SELECT 预算识别码, 父项预算识别码 FROM tabel_预算信息'''
    with connection.cursor() as cursor:
        cursor.execute(sql1)
        data = list(map(list, cursor.fetchall()))
        cursor.execute(sql2)
        hierarchy = list(map(list, cursor.fetchall()))
    # 将列表形式的数据格式化成字典型的
    dict_data = {}
    for da in data:
        dict_data[da[0]] = da[1:]
    # 将层级数据结构转化为dataframe
    array_hierarchy = np.array(hierarchy)
    frame_hierarchy = pd.DataFrame(
        array_hierarchy, columns=['预算识别码', '父项预算识别码'])

    def get_All_Roots():
        frame = frame_hierarchy[frame_hierarchy['父项预算识别码'].isnull()]
        list_frame = frame['预算识别码'].values.tolist()
        return [[x, 0] for x in list_frame]

    def get_All_Children(UDID, deep=0):
        frame = frame_hierarchy[frame_hierarchy['父项预算识别码'] == UDID]
        list_frame = frame['预算识别码'].values.tolist()
        return [[x, deep + 1] for x in list_frame]
    # 开始迭代获取数据层级
    roots_info = get_All_Roots()
    # 访问这些根节点，取得每个根节点的所有子项，存入其中

    def zipLeaves(roots_info):
        for i in range(len(roots_info)):
            UDID = roots_info[i][0]
            deep = roots_info[i].pop()
            roots_info[i] += dict_data[UDID] + [deep]
            children = get_All_Children(UDID, deep)
            roots_info[i] = [roots_info[i]]
            if children:
                roots_info[i].append(children)
                zipLeaves(children)
    zipLeaves(roots_info)
    return roots_info

# 付款管理


def read_For_Payment_GridDialog(where_sql='', where_list=[], order_sql='', order_list=[]):
    sql = '''SELECT {} FROM
             (SELECT           A.付款识别码, 付款登记时间, 付款支付时间, A.立项识别码, I.项目名称, I.分项名称,
                               A.合同识别码, 合同名称, 合同类别, 合同编号, 付款批次, 付款事由,
                               A.付款单位识别码, U1.单位名称 AS 付款单位名称, U1.银行账号 AS 付款单位账号,
                               A.收款单位识别码, U2.单位名称 AS 收款单位名称, U2.银行账号 AS 收款单位账号,
                               I.建设单位识别码, U3.单位名称 AS 建设单位名称, I.代建单位识别码, U4.单位名称 AS 代建单位名称,
                               BI.招标单位识别码, U5.单位名称 AS 招标单位名称, BI.中标单位识别码, U6.单位名称 AS 中标单位名称,
                               C.甲方识别码, U7.单位名称 AS 甲方单位名称, C.乙方识别码, U8.单位名称 AS 乙方单位名称,
                               C.丙方识别码, U9.单位名称 AS 丙方单位名称, C.丁方识别码, U10.单位名称 AS 丁方单位名称,
                               A.预算识别码, 预算名称, 预算周期, 付款时预算总额, 付款时项目概算, 付款时合同付款上限,
                               付款时合同值, 合同值_最终值 AS 合同最终值,
                               付款时预算余额, 付款时概算余额, 付款时合同可付余额, 付款时合同未付额,
                               付款时预算已付额, 付款时合同已付额, 付款时概算已付额,
                               付款时预算已付额/付款时预算总额 AS 付款时预算已付比,
                               付款时合同已付额/付款时合同值 AS 付款时合同已付比,
                               付款时概算已付额/付款时项目概算 AS 付款时概算已付比,
                               付款时形象进度, 本次付款额,
                               本次付款额/付款时预算总额 AS 预算本次付款比,
                               本次付款额/付款时合同值 AS 合同本次付款比,
                               本次付款额/付款时项目概算 AS 概算本次付款比,
                               (本次付款额+付款时预算已付额)/付款时预算总额 AS 预算累付比,
                               (本次付款额+付款时合同已付额)/付款时合同值 AS 合同累付比,
                               (本次付款额+付款时概算已付额)/付款时项目概算 AS 概算累付比,
                               付款备注
              FROM             tabel_付款信息 AS A
                    LEFT JOIN  tabel_立项信息 AS I ON A.立项识别码=I.立项识别码
                    LEFT JOIN  tabel_招标信息 AS BI ON A.立项识别码=BI.立项识别码
                    LEFT JOIN  tabel_合同信息 AS C ON A.合同识别码=C.合同识别码
                    LEFT JOIN  (SELECT 立项识别码, 付款识别码, convert(rank , SIGNED) AS 付款批次
                                FROM (SELECT ff.立项识别码, ff.付款识别码, IF(@pa = ff.立项识别码, @rank:=@rank + 1, @rank:=1) AS rank, @pa:=ff.立项识别码
                                      FROM   (SELECT 立项识别码, 付款识别码
                                              FROM   tabel_付款信息
                                              GROUP BY 立项识别码 , 付款识别码
                                              ORDER BY 立项识别码 , 付款识别码) ff, (SELECT @rank:=0, @pa := NULL) tt) result) AS BP ON A.付款识别码=BP.付款识别码
                    LEFT JOIN  tabel_单位信息 AS U1 ON A.付款单位识别码=U1.单位识别码
                    LEFT JOIN  tabel_单位信息 AS U2 ON A.收款单位识别码=U2.单位识别码
                    LEFT JOIN  tabel_单位信息 AS U3 ON I.建设单位识别码=U3.单位识别码
                    LEFT JOIN  tabel_单位信息 AS U4 ON I.代建单位识别码=U4.单位识别码
                    LEFT JOIN  tabel_单位信息 AS U5 ON BI.招标单位识别码=U5.单位识别码
                    LEFT JOIN  tabel_单位信息 AS U6 ON BI.中标单位识别码=U6.单位识别码
                    LEFT JOIN  tabel_单位信息 AS U7 ON C.甲方识别码=U7.单位识别码
                    LEFT JOIN  tabel_单位信息 AS U8 ON C.乙方识别码=U8.单位识别码
                    LEFT JOIN  tabel_单位信息 AS U9 ON C.丙方识别码=U9.单位识别码
                    LEFT JOIN  tabel_单位信息 AS U10 ON C.丁方识别码=U10.单位识别码
                    LEFT JOIN  tabel_预算信息 AS B ON A.预算识别码=B.预算识别码) AS Origin
          '''.format(', '.join(uc.PaymentColLabels)) + where_sql + ' ' + order_sql
    sql_list = where_list + order_list
    with connection.cursor() as cursor:
        cursor.execute(sql, sql_list)
        return dictfetchall(cursor)

# 其余查询API


def get_Children_Count(UDID):
    '''
        make sure UDID is int.
        get the count of a clicked item's children.
        return int or None.
    '''
    try:
        UDID = int(UDID)
        return len(table_Initiation.objects.filter(父项立项识别码=UDID))
    except:
        return


def new_get_All_Grandchildren_UDID(UDID):
    '''
        make sure UDID is int.
        取得某项下全部后代的立项识别码
        return a list(filled by int) or a blank list.
    '''
    db_Id_PId = pd.DataFrame(
        list(table_Initiation.objects.values('立项识别码', '父项立项识别码')))

    def getChildren(UDID):
        return list(db_Id_PId[db_Id_PId.父项立项识别码 == UDID].立项识别码)

    def getGrandChildren(UDID):
        result = []
        children_UDID = getChildren(UDID)
        if children_UDID:       # 如果UDID下还有子项
            for x in children_UDID:
                result += getGrandChildren(x)
            return result + [UDID]
        else:           # 如果UDID为叶子
            return [UDID]

    result = getGrandChildren(UDID)
    result.remove(UDID)
    result.sort()
    return result


def get_All_Grandchildren_UDID(UDID):
    '''
        make sure UDID is int.
        取得某项下全部后代的立项识别码
        return a list(filled by int) or a blank list.
    '''
    try:
        UDID = int(UDID)
        sql = '''
              SELECT queryChildrenAreaInfo(%s);
              CREATE FUNCTION `queryChildrenAreaInfo` (areaId INT)
              RETURNS VARCHAR(4000)
              BEGIN
                  DECLARE sTemp VARCHAR(4000);
                  DECLARE sTempChd VARCHAR(4000);
                  SET sTemp = '$';
                  SET sTempChd = cast(areaId as char);
                  WHILE sTempChd is not NULL DO
                      SET sTemp = CONCAT(sTemp,',',sTempChd);
                      SELECT group_concat(立项识别码) INTO sTempChd FROM tabel_立项信息 where FIND_IN_SET(父项立项识别码,sTempChd)>0;
                  END WHILE;
                  return sTemp;
              END;
              '''
        sql_list = [UDID]
        with connection.cursor() as cursor:
            cursor.execute(sql, sql_list)
            fetchall = cursor.fetchall()[0][0].split(',')[2:]
            return list(map(lambda x: int(x), fetchall))
    except:
        return []


def get_All_Budget_Grandchildren_UDID(UDID):
    '''
        取得某预算下全部子项、孙项等的预算识别码
    '''
    db_Id_PId = pd.DataFrame(
        list(table_Budget.objects.values('预算识别码', '父项预算识别码')))

    def getChildren(UDID):
        return list(db_Id_PId[db_Id_PId.父项预算识别码 == UDID].预算识别码)

    def getGrandChildren(UDID):
        result = []
        children_UDID = getChildren(UDID)
        if children_UDID:       # 如果UDID下还有子项
            for x in children_UDID:
                result += getGrandChildren(x)
            return result + [UDID]
        else:           # 如果UDID为叶子
            return [UDID]

    result = getGrandChildren(UDID)
    result.remove(UDID)
    result.sort()
    return result


def get_All_Budget_Grandchildren_UDID(UDID):
    '''
        取得某预算下全部子项、孙项等的预算识别码
    '''
    try:
        UDID = int(UDID)
        sql1 = '''
              set global log_bin_trust_function_creators=1;
              DROP FUNCTION IF EXISTS queryBudgetChildrenAreaInfo;
              '''
        sql2 = '''
              CREATE FUNCTION `queryBudgetChildrenAreaInfo` (areaId INT)
              RETURNS VARCHAR(4000)
              BEGIN
                  DECLARE sTemp VARCHAR(4000);
                  DECLARE sTempChd VARCHAR(4000);
                  SET sTemp = '$';
                  SET sTempChd = cast(areaId as char);
                  WHILE sTempChd is not NULL DO
                      SET sTemp = CONCAT(sTemp,',',sTempChd);
                      SELECT group_concat(预算识别码) INTO sTempChd FROM tabel_预算信息 where FIND_IN_SET(父项预算识别码,sTempChd)>0;
                  END WHILE;
                  return sTemp;
              END;
              '''
        sql = '''SELECT queryBudgetChildrenAreaInfo(%s);'''
        sql_list = [UDID]
        with connection.cursor() as cursor:
            cursor.execute(sql1)
            cursor.execute(sql2)
            cursor.execute(sql, sql_list)
            fetchall = cursor.fetchall()[0][0].split(',')[2:]
            return list(map(lambda x: int(x), fetchall))
    except:
        return []


def get_Count_Payment(list_UDID):
    '''
        make sure UDID is list with int.
        get the count of payment times.
        return int or None.
    '''
    try:
        assert type(list_UDID) == type([])
        return len(table_Payment.objects.filter(立项识别码__in=list_UDID))
    except:
        return


def get_Sum_Money_Payment(list_UDID):
    '''
        make sure UDID is list with int.
        get the sum money of payment.
        return float or None.
    '''
    try:
        assert type(list_UDID) == type([])
        return float(sum([x.get('本次付款额') for x in list(table_Payment.objects.filter(立项识别码__in=list_UDID).values('本次付款额'))]))
    except:
        return


# 权限相关类

class getUserPermission():
    '''
        Check a user wether has a permission.
        Obj(username).func() returns True or False.
    '''

    def __init__(self, username=''):
        '''
            Initialize a object by a user's username
        '''
        self.__filterObj = table_Permission.objects.filter(
            用户名__exact=str(username))

    def user_Is_Exist(self):
        '''
            Judge a user whether exist.
        '''
        if self.__filterObj:
            self.__filterDict = self.__filterObj.values()[0]
            return True
        else:
            return False

    # 以下为打开网页或窗口的权限

    def can_Visit_Overview(self):
        '''
            If a user is exist, and his field(查看数据概览) is True, then return True.
            Otherwise return False.
        '''
        if not self.user_Is_Exist():
            return False
        return self.__filterDict.get('查看数据概览')

    def can_Visit_Table(self, classify=''):
        '''
            If a user is exist, and his field(查看XX信息) is True, then return True.
            Otherwise return False.
        '''
        if not self.user_Is_Exist():
            return False
        return self.__filterDict.get('查看%s信息' % classify)

    def can_Visit_Attachment(self, classify=''):
        '''
            If a user is exist, and his field(查看单位信息) >= 2, then return True.
            Otherwise return False.
        '''
        if not self.user_Is_Exist():
            return False
        return (self.__filterDict.get('查看%s信息' % classify) or 0) >= 2

    # 读取数据权限

    def can_Read_Overview(self):
        '''
            If a user is exist, and his field(查看数据概览) is True, then return True.
            Otherwise return False.
        '''
        if not self.user_Is_Exist():
            return False
        return self.__filterDict.get('查看数据概览')

    def can_Read_Table(self, classify=''):
        '''
            If a user is exist, and his field(查看XX信息) is True, then return True.
            Otherwise return False.
        '''
        if not self.user_Is_Exist():
            return False
        return self.__filterDict.get('查看%s信息' % classify)

    def can_Get_Attachment_List(self, classify=''):
        '''
            If a user is exist, and his field(查看XX信息) is >= 2, then return True.
            Otherwise return False.
        '''
        if not self.user_Is_Exist():
            return False
        return (self.__filterDict.get('查看%s信息' % classify) or 0) >= 2

    def can_Download_Attachment(self, classify=''):
        '''
            If a user is exist, and his field(查看XX信息) is >= 3, then return True.
            Otherwise return False.
        '''
        if not self.user_Is_Exist():
            return False
        return (self.__filterDict.get('查看%s信息' % classify) or 0) >= 3

    # 写入数据权限

    def can_Upload_Attachment(self, classify=''):
        '''
            If a user is exist, and his field(查看单位信息) >= 2, then return True.
            Otherwise return False.
        '''
        if not self.user_Is_Exist():
            return False
        return (self.__filterDict.get('查看%s信息' % classify) or 0) >= 2

    def can_Write_Table(self, classify='', project=''):
        '''
            If a user is exist, and his field(操作XX信息) is True,
            or his field(允许操作XX的项目) contains the project,
            then return True.
            Otherwise return False.
        '''
        if not self.user_Is_Exist():
            return False
        classfity_dict = {
            # [x, y]
            # x代表classfity对应的表名
            # y==0代表检验权限不需用到project，y==1则反之
            '':         [0,                    0, ],
            '单位':     ['操作单位信息',         1, ],
            '立项':     ['允许操作立项的项目',    2, ],
            '招标':     ['允许操作招标的项目',    2, ],
            '合同':     ['允许操作合同的项目',    2, ],
            '预算':     ['操作预算信息',         1, ],
            '付款':     ['允许操作付款的项目',    2, ],
            '变更':     ['允许操作变更的项目',    2, ],
            '分包合同': ['允许操作分包合同的项目', 2, ],
            '概算':     ['允许调整概算的项目',    2, ],
            '合同额':   ['允许调整合同额的项目',   2, ],
        }
        field_name, flag = classfity_dict[
            classify]      # 看看要查的表是哪一种，需不需要project
        if flag == 1:
            return bool(self.__filterDict.get(field_name))
        elif flag == 2:
            project_list = (self.__filterDict.get(field_name) or '').split('|')
            return bool(project and project in project_list)

    def get_Permission_Write_Table(self):
        '''
            If a user is exist, and his field(操作XX信息) is True,
            or his field(允许操作XX的项目) contains the project,
            then return True.
            Otherwise return False.
        '''
        if not self.user_Is_Exist():
            return False
        classfity_dict = {
            '单位':     '操作单位信息',
            '立项':     '允许操作立项的项目',
            '招标':     '允许操作招标的项目',
            '合同':     '允许操作合同的项目',
            '预算':     '操作预算信息',
            '付款':     '允许操作付款的项目',
            '变更':     '允许操作变更的项目',
            '分包合同': '允许操作分包合同的项目',
            '概算':     '允许调整概算的项目',
            '合同额':   '允许调整合同额的项目',
        }
        result = {}
        for k, v in classfity_dict.items():
            result[k] = self.__filterDict.get(v)
        return result

# 操作OSS文件类


class operateOSS():
    '''
        Operation of Ali-OSS2.
    '''
    __bucket_name = 'sy-erp'

    def __init__(self):
        '''
            Initialize a object with connecting server.
        '''
        self.signoss()

    def signoss(self):
        '''
            Connecting server.
        '''
        auth = oss2.Auth('LTAIiM9nh4F41qKR',
                         'FIWNICi6h6mJxaPFz5nU4Zu32yraIn')    # 密码为w开头6位
        self.bucket = oss2.Bucket(
            auth, 'http://oss-cn-shanghai.aliyuncs.com', self.__bucket_name)

    def listfile(self, classify, UDID):
        '''
            Get a list of all files with given classify(立项/招标/合同/付款/预算 etc.) and UDID.
            Return a list which is filled by a dictionary.
        '''
        webpath = '%s信息/' % classify + '%d/' % UDID
        result = []
        for b in oss2.ObjectIterator(self.bucket, prefix=webpath):
            filename = b.key.replace(webpath, '')
            if filename:
                f_name = b.key.replace(webpath, '')
                try:
                    f_type = f_name.split('.')[-1]
                except:
                    f_type = ''
                f_time = str(datetime.datetime.fromtimestamp(b.last_modified))
                f_size = b.size or 0
                result.append({'文件名': f_name, '文件类型': f_type,
                               '修改时间': f_time, '文件大小': f_size})
        return result

    def get_file_url(self, classify, UDID, filename):
        '''
            Get a URL of a file with given classify(立项/招标/合同/付款/预算 etc.), UDID and filename.
            Return a string which is a URL address.
        '''
        webpath = '%s信息/' % classify + '%d/' % UDID + filename
        result = self.bucket.sign_url('GET', webpath, 300)
        return result
