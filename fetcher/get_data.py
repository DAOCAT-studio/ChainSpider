import pymysql


def se_data(t, symbol):
    try:
        host = '129.226.23.65'
        port = 3307
        passwd = '123456'
        user = 'root'
        db = "api_data"

        conn = pymysql.connect(host=host, user=user, password=passwd, database=db, port=port,
                               autocommit=True)

        with conn:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM glassnode WHERE t=%s AND symbol=%s "
                cursor.execute(sql, (t, symbol))
                result = cursor.fetchall()
                return result

    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(se_data('1604966400', 'BTC'))
