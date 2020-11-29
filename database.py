import sqlite3


class DataBase:
    def __init__(self, database_file):
        self.db = sqlite3.connect(database_file)
        self.cur = self.db.cursor()

    def update_chat(self, group_id, score):
        if self.cur.execute("SELECT EXISTS(SELECT * FROM chats WHERE chat=:group_id)",
                            {"group_id": group_id}).fetchone() == (1,):
            self.cur.execute("""UPDATE chats SET score = :score
                                 WHERE chat = :group_id
            """, {"group_id": group_id, "score": score})
        else:
            self.cur.execute("INSERT INTO chats VALUES (:group_id, :score)", {"group_id": group_id, "score": score})
        self.db.commit()

    def get_score(self, group_id):
        self.cur.execute("SELECT * FROM chats WHERE chat=:chat", {"chat": group_id})
        try:
            return self.cur.fetchone()[1]
        except TypeError:
            print("Value doesn't exist! Returning 0...")
            return 0

    def get_scores(self):
        self.cur.execute("SELECT * FROM chats")
        return self.cur.fetchall()

    def __del__(self):
        self.db.close()
