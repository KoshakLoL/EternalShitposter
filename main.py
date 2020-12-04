import vk_api
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.utils import get_random_id

from msg_construct import msg_construct

from bot_functions.fortune import fortune
from bot_functions.shitposter import shitpost


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

    def get_message_payload(self, text):
        return self.vk, self.msg_recipient, get_random_id(), text

    def set_message_recipient(self, event):
        self.msg_recipient = event.obj.peer_id

    def shitposter(self):
        msg_construct(*self.get_message_payload(shitpost()))

    def fortune(self):
        msg_construct(*self.get_message_payload(fortune()))

    def not_group(self):
        msg_construct(*self.get_message_payload("Please add me to a group chat, I don't work in private messages!"))
