from datetime import datetime
import mysql.connector


class MySQLManager:
    def __init__(self) -> None:
        self.conn = None
        self.connect()

    def connect(self):
        self.conn = mysql.connector.connect(
            host="127.0.0.1",
            port=30306,
            user="root",
            password="root",
            database="auth")

        # Get a cursor
        # self.mydb = create_engine("mysql://root:rootpassword@localhost/auth", echo=True)

    def find_user(self, username):
        cur = self.conn.cursor()

        sql = "SELECT * from login where username=%s"
        cur.execute(sql, (username,))
        result = cur.fetchone()

        return result

    def find_one(self, username, password):
        cur = self.conn.cursor()

        sql = "SELECT * from login where username=%s and password=%s"
        cur.execute(sql, (username, password,))
        result = cur.fetchone()
        print(result)
        return result


    def insert_one(self, user_id, username, password, created_date, last_modified):
        mycursor = self.conn.cursor()
        sql = "INSERT INTO login (user_id, username, password, role, created_date, last_modified) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (user_id, username, password, "u", created_date, last_modified)
        mycursor.execute(sql, val)

        self.conn.commit()

        print(mycursor.rowcount, "record inserted.")
        return mycursor.rowcount
