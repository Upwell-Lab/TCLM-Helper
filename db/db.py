import sqlite3

class db():
    def __init__(self):
        self.db_folder = "db"

    def ex_data(self, ex):
        conn = sqlite3.connect(f'{self.db_folder}/{ex}_s.db')
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ex_data'")
        table_exists = cursor.fetchone()

        while True:
            if not table_exists:
                # Если таблицы нет, создаем её
                cursor.execute("""
                    CREATE TABLE ex_data (
                        name TEXT ,
                        type TEXT
                    )
                """)
                break
            else:
                cursor.execute("DROP TABLE ex_data")
                
        conn.close()

    def insert(self, ex, name, type):
        #conn = sqlite3.connect(f'{self.db_folder}/{ex}_s.db')
        #cursor = conn.cursor()

        #cursor.execute("INSERT INTO ex_data (name, type) VALUES (?, ?)", (name, type))

        #conn.commit()
        #conn.close()
        pass