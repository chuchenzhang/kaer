import pymysql


def randomHero(amount):
    if amount == 0:
        return None
    db = pymysql.connect(host='127.0.0.1', user='root', password='root', database='kaer', charset='utf8')

    cursor = db.cursor()

    sql = 'select * from heroes order by rand() limit %d' % amount
    # print(sql)

    try:
        cursor.execute(sql)

        data = cursor.fetchall()

        # print(data)
        return data
    except:
        return 'Error: unable to fetch data'
