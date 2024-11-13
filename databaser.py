import pymysql
import pymysql.cursors
from config import host, user, password, db_name


def connect():
    try:
        con = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        return con
    except Exception as ex:
        return False

def close(con):
    try:
        con.close()
        return True
    except Exception as ex:
        return False

def user_entry(username, password):
    con = connect()
    try:
        with con.cursor() as cursor:
            sql = f"""
            SELECT user_name, status_name
            FROM users
            JOIN status
            ON users.status_id = status.status_id
            WHERE user_name LIKE '{username}' AND user_password LIKE '{password}';
            """
            cursor.execute(sql)
            user = cursor.fetchall()[0]
            close(con)
            user = [user['user_name'], user['status_name']]

            return user

    except Exception as ex:
        print(ex)
        close(con)

        return False