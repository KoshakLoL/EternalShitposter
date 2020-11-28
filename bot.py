# -*- coding: utf-8 -*-
import vk_api
from random import choice
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id


class MainBot:
    def __init__(self, token, group_id):
        self.vk_session = vk_api.VkApi(token=token)
        self.vk = self.vk_session.get_api()
        self.group_id = group_id
        self.long_poll = VkBotLongPoll(self.vk_session, self.group_id)
        self.score = 0

    def main(self):
        for event in self.long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if self.group_id in event.obj.text or self.score == 10:
                    msg_recipient = event.obj.peer_id
                    final = (get_file_array("array1.txt") +
                             get_file_array("array2.txt") +
                             get_file_array("array3.txt")).replace("\n", "")

                    self.vk.messages.send(
                        peer_id=msg_recipient,
                        random_id=get_random_id(),
                        message=final
                    )
                    self.score = 0
                else:
                    self.score += 1


def get_file_array(file):
    with open(file, "r") as array:
        return choice(list(array))


bot = MainBot("1572a1f3b0c5732276207571fa4a74fa53de2a826c6d719ce8d98cfb761eb4cba36e10e26fe144caa99c0", "200700644")
if __name__ == "__main__":
    bot.main()
