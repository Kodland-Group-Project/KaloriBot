import sqlite3

class DBManager:
    def __init__(self, db_name='app.db'):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def get_value(self, food_name):
        self.cursor.execute("SELECT value FROM data WHERE Food_Items=?", (food_name,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def create_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS user(userid INTEGER PRIMARY KEY, username TEXT, age INTEGER, height INTEGER, weight INTEGER, aim_of_calories_in_3_month INTEGER DEFAULT 0, totol_calories_in_3_month INTEGER DEFAULT 0)")

    def add_user(self, userid, username, age=None, height=None, weight=None):
        self.cursor.execute("INSERT INTO user (userid, username, age, height, weight) VALUES (?, ?, ?, ?, ?)", (userid, username, age, height, weight))
        self.connection.commit()

    def set_calories(self, userid, calories):
        self.cursor.execute("UPDATE user SET aim_calories_in_3_month = ? WHERE userid = ?", (calories, userid))
        self.connection.commit()

    def add_calories(self, userid, calories):
        self.cursor.execute("UPDATE user SET totol_calories_in_3_month = totol_calories_in_3_month + ? WHERE userid = ?", (calories, userid))
        self.connection.commit()

    def get_calories(self, userid):
        self.cursor.execute("SELECT totol_calories_in_3_month FROM user WHERE userid = ?", (userid,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
def calori_calculating():
    pass