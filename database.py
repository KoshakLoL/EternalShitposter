import sqlite3


class DataBase:
    def __init__(self, database_file):
        if ".db" not in database_file:
            raise NoDatabaseFile
        self.db = sqlite3.connect(database_file)
        self.cur = self.db.cursor()

    def update_value(self, table, column, chat_id, value):
        with self.db:
            if self.cur.execute("SELECT EXISTS(SELECT * FROM {} WHERE chat=:chat)".format(table),
                                {"chat": chat_id}).fetchone() == (1,):
                self.cur.execute("""UPDATE {} SET {} = :value
                                     WHERE chat = :chat
                """.format(table, column), {"value": value, "chat": chat_id})
            else:
                self.cur.execute("INSERT INTO {} VALUES (:chat, :value)".format(table),
                                 {"chat": chat_id, "value": value})

    def get_value(self, table, chat_id):
        self.cur.execute("SELECT * FROM {} WHERE chat=:chat".format(table), {"chat": chat_id})
        try:
            return self.cur.fetchone()[1]
        except TypeError:
            return 1

    def close_db(self):
        self.db.close()


class NoDatabaseFile(Exception):
    def __init__(self):
        print("No database file in bot.py! Please add one.")
        exit()
