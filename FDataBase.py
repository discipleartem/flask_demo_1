import sqlite3
import math
import time


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):
            sql = 'SELECT * FROM mainmenu'
            try:
                self.__cur.execute(sql)
                res = self.__cur.fetchall()
                if res: return res
            except sqlite3.Error as e:
                print('Ошибка чтения из БД:', e)
            return []

    def addPost(self, title, text):
        try:
            tm = math.floor(time.time())
            self.__cur.execute('INSERT INTO posts VALUES(NULL, ?, ?, ?)', (title, text, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД:"+str(e))
            return False

        return True


    def getPost(self, id_post):
        try:
            self.__cur.execute(f"SELECT title, text FROM posts WHERE id = {id_post} LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка чтения статьи из БД:"+str(e))

        return (False, False)

    def getPostsAnonce(self):
        try:
            self.__cur.execute(f"SELECT id, title, text FROM posts ORDER BY time DESC")
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка чтения статьи из БД:"+str(e))

        return []