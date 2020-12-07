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
                #    Check if "fortune" is in text          Either private message event or ping in a group chat
                if "fortune" in event.obj.text.lower() and (event.from_user or self.group_name in event.obj.text):
                    self.fortune()
                    self.set_score(self.get_score() - 1)
                #    Check if "auto" is in text                 Only works in group chats and with ping
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
                #   Check if either "shitpost" is in text and it's an event from user
                #       OR       check if the bot was pinged in a group chat
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
        # If it is the same member as the one who called
        if entry["member_id"] == event.obj.from_id:
            # If the member is admin
            if ("is_admin" in entry and entry["is_admin"]) or ("is_owner" in entry and entry["is_owner"]):
                return True
    return False


if __name__ == "__main__":
    database = DataBase("database")  # Database sample
    bot = MainBot("token",  # Group token
                  "group_id",  # Group ID
                  database)  # Database reference
    try:
        bot.main()
    except KeyboardInterrupt:  # If the bot was stopped by keyboard (useful for testing)
        bot.db.close_db()
        exit()
