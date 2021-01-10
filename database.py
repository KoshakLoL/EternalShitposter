import os
import sqlite3

from bot_utils import get_yml_logger

log = get_yml_logger("logging.yml", __name__)


class Database:
    def __init__(self, database_file):
        log.info(f"Opening {database_file}...")
        if not os.path.exists(database_file):
            raise WrongDatabaseFile(database_file)
        self.db = sqlite3.connect(database_file)
        self.cur = self.db.cursor()
        log.info("Database opened!")

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

    def close_db(self):
        log.info("Closing database...")
        self.db.close()


class WrongDatabaseFile(Exception):
    def __init__(self, db_file):
        log.critical(f"{db_file} not found in {os.getcwd()}!")
        exit()
