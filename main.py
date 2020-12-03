import vk_api
import subprocess
from random import choice
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.utils import get_random_id


class MainFunc:
    def __init__(self, token, group_id, db):
        self.vk_session = vk_api.VkApi(token=token)
        self.vk = self.vk_session.get_api()
        self.group_id = group_id
        self.long_poll = VkBotLongPoll(self.vk_session, self.group_id)
        self.db = db
        self.score = 0
        self.msg_recipient = ""

    def get_event_listener(self):
        return self.long_poll.listen()

    def set_message_recipient(self, event):
        self.msg_recipient = event.obj.peer_id

    def shitposter(self):
        self.msg_construct((get_file_array("array1.txt") +
                            get_file_array("array2.txt") +
                            get_file_array("array3.txt")).replace("\n", ""))

    def fortune(self):
        self.msg_construct(subprocess.check_output(['fortune', '-eso']))

    def not_group(self):
        self.msg_construct("Please add me to a group chat, I don't work in private messages!")

    def msg_construct(self, message):
        self.vk.messages.send(
            peer_id=self.msg_recipient,
            random_id=get_random_id(),
            message=message
        )


def get_file_array(file):
    with open(file, "r") as array:
        return choice(list(array)) + " "
