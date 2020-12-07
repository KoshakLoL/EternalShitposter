# -*- coding: utf-8 -*-
from database import DataBase
from vk_api.bot_longpoll import VkBotEventType

from main import MainFunc


class MainBot(MainFunc):
    def __init__(self, token, group_id, db):
        super().__init__(token, group_id, db)

    def main(self):
        for event in self.get_event_listener():
            if event.type == VkBotEventType.MESSAGE_NEW:
                self.set_message_recipient(event)

                self.set_score(self.get_database_score())  # This is the beginning of db-local transaction
                self.set_status(self.get_database_status())  # This is the end of db-local transaction

                # Local work
                if "fortune" in event.obj.text.lower() and (event.from_user or self.group_name in event.obj.text):
                    self.fortune()
                    self.set_score(self.get_score() - 1)

                elif "auto" in event.obj.text.lower() and self.group_name in event.obj.text and event.from_chat:
                    response = self.vk_api.messages.getConversationMembers(peer_id=self.msg_recipient,
                                                                           group_id=self.group_id)["items"]
                    if check_for_owner(response, event):
                        if self.get_status() == 0:
                            self.set_status(1)
                            self.set_message_payload("Now the bot will auto-shitpost!")
                            self.set_score(self.get_score() - 1)
                        else:
                            self.set_status(0)
                            self.set_message_payload("Now the bot will NOT auto-shitpost... You're no fun :(")
                    else:
                        self.set_message_payload("You're not an admin bro, get yourself some moderating privileges")

                elif ("shitpost" in event.obj.text.lower() and event.from_user) \
                        or (self.group_name in event.obj.text and event.from_chat):
                    self.shitpost()
                    self.set_score(1)

                if self.get_status() == 1:
                    if self.get_score() >= 10:
                        self.shitpost()
                        self.set_score(1)
                    else:
                        self.set_score(self.get_score() + 1)
                # Local work END

                self.set_database_score(self.get_score())  # This is the beginning of local-db transaction
                self.set_database_status(self.get_status())  # This is the end of local-db transaction


def check_for_owner(response, event):
    for entry in response:
        if entry["member_id"] == event.obj.from_id:
            if ("is_admin" in entry and entry["is_admin"]) or ("is_owner" in entry and entry["is_owner"]):
                return True
    return False


if __name__ == "__main__":
    database = DataBase("database")
    bot = MainBot("token",
                  "group_id",
                  database)
    try:
        bot.main()
    except KeyboardInterrupt:
        bot.db.close_db()
        exit()
