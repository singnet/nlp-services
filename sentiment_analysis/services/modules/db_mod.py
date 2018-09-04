import sqlite3


class DBManager:

    conn = False
    cursor = False

    def __init__(self, name=None):

        self.conn = sqlite3.connect('../../temp_' + name + '.db')
        self.cursor = self.conn.cursor()

    def open(self, name):

        try:
            # Generating databases
            self.conn = sqlite3.connect('../../temp_' + name + '.db')
            self.cursor = self.conn.cursor()

        except sqlite3.Error as e:
            print("Error connecting to database: " + str(e))

    def query(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()

    def close(self):
        self.conn.close()

    # c.execute("INSERT INTO sentiment (unix, tweet, sentiment) VALUES (?, ?, ?)",(time_ms, tweet, sentiment))
    # conn.commit()
