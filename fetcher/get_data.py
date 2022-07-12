import pymysql


# 独立于其他脚本以外的查询实例
def se_data(t, symbol):
    try:
        host = '43.158.211.160'
        port = 3306
        passwd = 'admin'
        user = 'admin'
        db = "api_data"

        conn = pymysql.connect(host=host, user=user, password=passwd, database=db, port=port,
                               autocommit=True)
        t_symbol = "{}_{}".format(t,symbol)
        with conn:
            with conn.cursor() as cursor:
                # sql = "SELECT * FROM glassnode WHERE t_symbol=%s "
                # cursor.execute(sql, t_symbol)
                sql = "SELECT * FROM glassnode WHERE symbol=%s "
                cursor.execute(sql, symbol)
                result = cursor.fetchall()
                return result

    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(se_data('1604966400', 'BTC'))
