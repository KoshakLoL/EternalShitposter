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
                elif event.obj.text == self.group_id + " fortune":
                    self.fortune()
                else:
                    self.score = self.db.get_score(self.msg_recipient)
                    if self.group_id in event.obj.text or self.score == 10:
                        self.shitposter()
                        self.score = 1
                    else:
                        self.score += 1
                    self.db.update_chat(str(self.msg_recipient), self.score)


database = DataBase("database")
bot = MainBot("token", "group", database)
if __name__ == "__main__":
    bot.main()
