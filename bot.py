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
                if event.from_user:
                    self.not_group()
                elif self.group_name in event.obj.text:
                    if "fortune" in event.obj.text:
                        self.fortune()
                        self.add_score()
                        self.check_score()
                    elif "auto" in event.obj.text:
                        response = self.vk_api.messages.getConversationMembers(peer_id=self.msg_recipient,
                                                                               group_id=self.group_id)["items"]
                        if check_for_owner(response, event):
                            if self.auto_shitpost == 0:
                                self.set_database_status(1)
                                self.set_message_payload("Now the bot will auto-shitpost!")
                            else:
                                self.set_database_status(0)
                                self.set_message_payload("Now the bot will NOT auto-shitpost... You're no fun :(")
                        else:
                            self.set_message_payload("You're not an admin bro, get yourself some moderating privileges")
                    else:
                        self.shitpost()
                        self.reset_score()
                self.get_database_status()
                if self.get_status() == 1:
                    self.get_database_score()
                    self.check_score()
                self.set_database_score()
                self.set_database_status(self.get_status())


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
        exit()
