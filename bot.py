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
                        self.check_score()
                    else:
                        self.shitpost()
                        self.reset_score()
                else:
                    self.score = self.db.get_score(self.msg_recipient)
                    self.check_score()
                self.db.update_chat(str(self.msg_recipient), self.score)


database = DataBase("database")
bot = MainBot("token",
              "group_id",
              database)
if __name__ == "__main__":
    try:
        bot.main()
    except KeyboardInterrupt:
        database.__del__()  # Forcing data-base to shutdown
        exit()
