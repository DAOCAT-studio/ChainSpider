import pymysql
import os
import configparser

cur_path = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(cur_path, 'config.ini')
cf = configparser.ConfigParser()
cf.read(config_path, encoding='utf-8')

db_set = cf['server']

host = db_set['HOST']
port = int(db_set['PORT'])
user = db_set['USER']
passwd = db_set['PASSWD']
db = 'api_data'


# 独立于其他脚本以外的查询实例
def se_data(date):
    try:
        conn = pymysql.connect(host=host, user=user, password=passwd, database=db, port=port,
                               autocommit=True)
        with conn:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM glassnode WHERE date=" + date + " "
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
    except Exception as e:
        print(e)


def time_series(start, end):
    try:
        conn = pymysql.connect(host=host, user=user, password=passwd, database=db, port=port,
                               autocommit=True)
        with conn:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM glassnode WHERE date BETWEEN " + start + " AND " + end + "  "
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
    except Exception as e:
        print(e)


def reduce_data():
    try:
        conn = pymysql.connect(host=host, user=user, password=passwd, database=db, port=port,
                               autocommit=True)
        with conn:
            with conn.cursor() as cursor:
                sql = "SELECT date,symbol,(addresses_count_v*1.5+market_marketcap_usd_v*1.5+market_price_usd_close_v*1.5) AS result " \
                      "FROM glassnode GROUP BY date,symbol,result ORDER BY date "
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # 传入日期参数，数据将以元组的列表形式返回
    # 1
    print(se_data('20220722'))
    # 2
    # print(time_series('20210701', '20210801'))
    # 3
    # print(reduce_data())
