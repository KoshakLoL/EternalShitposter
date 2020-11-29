# -*- coding: utf-8 -*-
import vk_api
from random import choice
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id

from database import DataBase


class MainBot:
    def __init__(self, token, group_id, db):
        self.group_id = group_id
        self.vk_session = vk_api.VkApi(token=token)
        self.vk = self.vk_session.get_api()
        self.long_poll = VkBotLongPoll(self.vk_session, self.group_id)
        self.db = db
        self.score = 0

    def main(self):
        for event in self.long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                msg_recipient = event.obj.peer_id
                if msg_recipient < 2000000000:
                    self.vk.messages.send(
                        peer_id=msg_recipient,
                        random_id=get_random_id(),
                        message="Please add me to a group chat, I don't work in private messages!"
                    )
                else:
                    self.score = self.db.get_score(msg_recipient)
                    if self.group_id in event.obj.text or self.score == 10:
                        final = (get_file_array("array1.txt") +
                                 get_file_array("array2.txt") +
                                 get_file_array("array3.txt")).replace("\n", "")

                        self.vk.messages.send(
                            peer_id=msg_recipient,
                            random_id=get_random_id(),
                            message=final
                        )
                        self.score = 1
                    else:
                        self.score += 1
                    self.db.update_chat(str(event.obj.peer_id), self.score)


def get_file_array(file):
    with open(file, "r") as array:
        return choice(list(array))


database = DataBase("database")
bot = MainBot("token", "group_id", database)
if __name__ == "__main__":
    bot.main()
