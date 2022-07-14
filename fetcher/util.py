import json
import logging
import os
import time
import traceback
from logging import handlers

import pymysql
import requests

import settings

LOG_ROOT = settings.LOG_ROOT
host = settings.HOST
port = settings.PORT
user = settings.USER
passwd = settings.PASSWD
db = settings.DB


def get_logger(log_filename, level=logging.DEBUG, when='midnight', back_count=0):
    """
    :brief  日志记录
    :param log_filename: 日志名称
    :param level: 日志等级
    :param when: 间隔时间:
        S:秒
        M:分
        H:小时
        D:天
        W:每星期（interval==0时代表星期一）
        midnight: 每天凌晨
    :param back_count: 备份文件的个数，若超过该值，就会自动删除
    :return: logger
    """
    logger = logging.getLogger(log_filename)
    logger.setLevel(level)
    log_path = os.path.join(LOG_ROOT, "logs")
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    log_file_path = os.path.join(log_path, log_filename)
    # log输出格式
    formatter = logging.Formatter('%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    # 输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(level)
    # 输出到文件
    fh = logging.handlers.TimedRotatingFileHandler(
        filename=log_file_path,
        when=when,
        backupCount=back_count,
        encoding='utf-8')
    fh.setLevel(level)
    # 设置日志输出格式
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # 添加到logger对象里
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


# 获取代理ip
def get_ip():
    while True:
        try:
            response = requests.get(
                url='http://proxy.httpdaili.com/apinew.asp?text=true&noinfo=true&sl=1&ddbh=nmdd001&px=sj')
            response.encoding = 'utf-8'
            proxy_ip = response.text.strip()
            return "socks5://{}".format(proxy_ip)
        except:
            time.sleep(0.05)


def db_ori_set():
    try:
        conn = pymysql.connect(host=host, user=user, password=passwd, database=db, port=port,
                               autocommit=True)
        date = time.strftime("%Y%m%d", time.localtime())
        with conn:
            # 检查列是否存在
            with conn.cursor() as cursor:
                sql = "UPDATE state_trace SET state=0"
                cursor.execute(sql)

    except:
        print(traceback.format_exc())


def db_handle(api_url, symbol, result_list):
    # logger = get_logger("glassnode.log")
    try:
        # col_type = 'varchar(100)'
        col_type = 'double'
        col_name = api_url.split('/')[-2] + '_' + api_url.split('/')[-1]

        insert_data = []
        if isinstance(result_list, list):
            keys = list(result_list[0].keys())
            col_name = col_name + '_' + keys[1]
            if keys[1] != 'v':
                col_type = 'json'

            # 整理成要插入数据库的数据
            for item in result_list:

                temp = []
                t = item.get("t")
                for value in item.values():
                    temp.append(json.dumps(value) if isinstance(value, dict) else value)
                # data.append(symbol)
                data = temp[1]

                insert_data.append(("{}_{}".format(t, symbol), t, data, symbol, data))
        # 解决某些api返回是字典的情况
        elif isinstance(result_list, dict):
            t = result_list.pop("t")
            data = json.dumps(result_list)
            col_name = col_name + '_data'
            col_type = 'json'
            insert_data.append(("{}_{}".format(t, symbol), t, data, symbol, data))
        else:
            print(result_list)
            # logger.info("unknown response type", api_url)
            raise TypeError("unknown response type")

        # print(insert_data)

        conn = pymysql.connect(host=host, user=user, password=passwd, database=db, port=port,
                               autocommit=True)
        with conn:
            # 检查列是否存在
            with conn.cursor() as cursor:
                sql = "SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` " \
                      "WHERE `TABLE_SCHEMA`='api_data' AND `TABLE_NAME`='glassnode';"
                # print(sql)
                cursor.execute(sql)
                result = cursor.fetchall()
                # print('hi----------------')
                # print(result)
                column_set = [i[0] for i in result]
                # print(column_set)
                if col_name not in column_set:
                    # 不存在即创建
                    # print('not exists')
                    with conn.cursor() as cursor_1:
                        sql = "ALTER TABLE `glassnode` ADD `{col_name}` {col_type} ".format(col_name=col_name,
                                                                                            col_type=col_type)
                        try:
                            cursor_1.execute(sql)
                            print('successfully created a new column named `{}`!'.format(col_name))
                        except pymysql.err.OperationalError as err:
                            print(err)
                            # logger.error("{}:col_name-{},col_type-{},sql-{}".format(err, col_name, col_type, sql))
            # 插入api返回的数据
            with conn.cursor() as cursor:
                try:
                    for data in insert_data:
                        sql = "INSERT INTO glassnode ( t_symbol, t, " + col_name + ", symbol ) VALUES ( %s, %s, %s, %s ) ON DUPLICATE KEY UPDATE " + col_name + " = %s "
                        # print(sql)
                        cursor.execute(sql, (data[0], data[1], data[2], data[3], data[4]))

                    print('successfully inserted data!')
                except:
                    # logger.error("{}:col_name-{},col_type-{},sql-{}".format(e, col_name, col_type, insert_query))
                    # logger.info(e)
                    print(traceback.format_exc())



    except Exception as e:
        # print(traceback.format_exc())
        # logger.error(e)
        print(e)


def db_trace(api_url, symbol, api_key, status):
    # logger = get_logger("glassnode.log")
    try:
        conn = pymysql.connect(host=host, user=user, password=passwd, database=db, port=port,
                               autocommit=True)
        date = time.strftime("%Y%m%d", time.localtime())
        with conn:
            # 检查列是否存在
            # 更新追踪表
            with conn.cursor() as cursor:
                # 执行插入，如主键存在即更新
                api_symbol = '{}_{}'.format(api_url, symbol)
                update_data = (api_symbol, api_url, symbol, 1, api_key, status,
                               time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                # update_query = 'INSERT INTO `state_trace` ( `api_symbol`,`api`, `symbol`, `{col_name}` ) VALUES ( %s, %s, %s ) ' \
                #                'ON DUPLICATE KEY UPDATE `symbol` = %s, `{col_name}`= %s '.format(col_name=col_name)
                update_query = "REPLACE INTO `state_trace` ( `api_symbol`,`api`, `symbol`, `state`,`api_key`, `last_status`, `updatetime` ) " \
                               "VALUES ( %s, %s, %s, %s, %s, %s, %s) "
                # print(update_query)
                cursor.execute(update_query, update_data)
                print('successfully updated state_trace!')

    except Exception as e:
        # logger.error(e)
        print(e)


def db_get_429():
    # logger = get_logger("glassnode.log")
    try:
        conn = pymysql.connect(host=host, user=user, password=passwd, database=db, port=port,
                               autocommit=True)
        with conn:
            with conn.cursor() as cursor:
                sql = "SELECT api,symbol FROM state_trace where last_status=429 and state=1 "
                # print(update_query)
                cursor.execute(sql)
                re_cur = cursor.fetchall()
                return re_cur

    except Exception as e:
        print(e)


def record_api(res):
    try:
        insert_api_data = []
        for item in res:
            path = "https://api.glassnode.com{}".format(item.get("path"))
            tier = item.get("tier")
            assets = str(item.get("assets"))
            currencies = str(item.get("currencies"))
            resolutions = str(item.get("resolutions"))
            formats = str(item.get("formats"))
            insert_api_data.append((path, tier, assets, currencies, resolutions, formats,
                                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

        conn = pymysql.connect(host=host, user=user, password=passwd, database=db, port=port,
                               autocommit=True)
        with conn:
            with conn.cursor() as cursor:
                update_query = "REPLACE INTO `endpoints` ( `api_url`,`tier`, `assets`, `currencies`,`resolutions`, `formats`, `updatetime` ) " \
                               "VALUES ( %s, %s, %s, %s, %s, %s, %s) "
                # print(update_query)
                cursor.executemany(update_query, insert_api_data)
                print("successfully updated endpoints!")
    except Exception as e:
        print(e)
        # print(traceback.format_exc())


if __name__ == '__main__':
    api = "https://api.glassnode.com/v1/metrics/addresses/sending_count"
    result = [{"t": 161455611800, "s": {"h": 22001246972.515, "w": 22001246, "t": 2200}},
              {"t": 161451111111, "s": {"h": 22001246972.515, "w": 22001246, "t": 2200}}]
    # db_handle(api, 'BTC', result)
    r = db_get_429()
    print(r)
    print(type(r))
    print(len(r))
    d = [{"api": i[0], "symbol": i[1]} for i in r]
    print(d)
