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
                if self.msg_recipient < 2000000000:
                    self.not_group()
                elif self.group_name in event.obj.text:
                    if "fortune" in event.obj.text:
                        self.fortune()
                        self.add_score()
                        self.check_score()
                    elif "auto" in event.obj.text:
                        if self.auto_shitpost == 0:
                            self.set_database_status(1)
                            self.set_message_payload("Now the bot will auto-shitpost!")
                        else:
                            self.set_database_status(0)
                            self.set_message_payload("Now the bot will NOT auto-shitpost... You're no fun :(")
                    else:
                        self.shitpost()
                        self.reset_score()
                self.get_database_status()
                if self.get_status() == 1:
                    self.get_database_score()
                    self.check_score()
                self.set_database_score()
                self.set_database_status(self.get_status())


if __name__ == "__main__":
    database = DataBase("database")
    bot = MainBot("token",
                  "group_id",
                  database)
    try:
        bot.main()
    except KeyboardInterrupt:
        exit()
