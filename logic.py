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
        self.cursor.execute("CREATE TABLE IF NOT EXISTS user(userid INTEGER PRIMARY KEY, username TEXT, age INTEGER, height INTEGER, weight INTEGER, gender INTEGER, aim_of_calories INTEGER DEFAULT 0, total_calories INTEGER DEFAULT 0)")

    def add_user(self, userid, username, age=None, height=None, weight=None, gender=None):
        self.cursor.execute("INSERT INTO user (userid, username, age, height, weight) VALUES (?, ?, ?, ?, ?, ?)", (userid, username, age, height, weight, gender))
        self.connection.commit()

    def set_calories(self, userid, calories):
        self.cursor.execute("UPDATE user SET aim_of_calories = ? WHERE userid = ?", (calories, userid))
        self.connection.commit()

    def add_calories(self, userid, calories):
        self.cursor.execute("UPDATE user SET total_calories = total_calories + ? WHERE userid = ?", (calories, userid))
        self.connection.commit()

    def get_calories(self, userid):
        self.cursor.execute("SELECT totol_calories FROM user WHERE userid = ?", (userid,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
def calori_calculating(height, weight, age, gender):
    if gender == 1:#woman
        bmr = 655 + (9.6 * weight) + (1.8 * height) - (4.7 * age)
        return bmr
    elif gender == 2:#man
        bmr = 66 + (13.7 * weight) + (5 * height) - (6.8 * age)
        return bmr
