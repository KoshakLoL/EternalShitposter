import vk_api
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.utils import get_random_id

from msg_construct import msg_construct

from bot_functions.fortune import fortune
from bot_functions.shitposter import shitpost


class MainFunc:
    def __init__(self, token, group_id, db):
        self.vk_session = vk_api.VkApi(token=token)
        self.vk_api = self.vk_session.get_api()
        self.group_id = group_id
        self.long_poll = VkBotLongPoll(self.vk_session, self.group_id)
        with vk_api.VkRequestsPool(self.vk_session) as pool:
            response = pool.method("groups.getById")
        self.group_prefix = "[club" + self.group_id + "|" + response.result[0]["name"] + "]"
        self.db = db
        self.score = 0
        self.msg_recipient = ""

    def get_event_listener(self):
        return self.long_poll.listen()

    def set_message_payload(self, text):
        msg_construct(self.vk_api, self.msg_recipient, get_random_id(), text)

    def set_message_recipient(self, event):
        self.msg_recipient = event.obj.peer_id

    def shitpost(self):
        self.set_message_payload(shitpost())

    def fortune(self):
        self.set_message_payload(fortune())

    def not_group(self):
        self.set_message_payload("Please add me to a group chat, I don't work in private messages!")
