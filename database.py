import sqlite3


class DataBase:
    def __init__(self, database_file):
        print("Opening database...")
        if ".db" not in database_file:
            print("No database file in bot.py! Please add one.")
            exit()
        self.db = sqlite3.connect(database_file)
        self.cur = self.db.cursor()
        print("Database opened!")

    def update_value(self, table, column, chat_id, value):
        with self.db:
            if self.cur.execute(f"SELECT EXISTS(SELECT * FROM {table} WHERE chat=:chat)",
                                {"chat": chat_id}).fetchone() == (1,):  # If the chat already exists
                self.cur.execute(f"UPDATE {table} SET {column} = :value WHERE chat = :chat",
                                 {"value": value, "chat": chat_id})
            else:
                self.cur.execute(f"INSERT INTO {table} VALUES (:chat, :value)",
                                 {"chat": chat_id, "value": value})  # If the chat does not exist

    def get_value(self, table, chat_id):
        self.cur.execute(f"SELECT * FROM {table} WHERE chat=:chat", {"chat": chat_id})
        try:
            return self.cur.fetchone()[1]
        except TypeError:
            return 1

    def __del__(self):
        print("Closing database...")
        self.db.close()
