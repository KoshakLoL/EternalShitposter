from vk_api import VkApi
from vk_api.exceptions import ApiError
from vk_api.bot_longpoll import VkBotLongPoll

from msg_construct import msg_construct

from bot_functions.fortune import fortune
from bot_functions.shitposter import shitpost


class MainFunc:
    def __init__(self, token, group_id, db):
        self.vk_session = VkApi(token=token)  # Initializing session
        self.vk_api = self.vk_session.get_api()  # Initializing API
        self.group_id = group_id
        self.group_name = "club" + self.group_id
        try:
            self.long_poll = VkBotLongPoll(self.vk_session, self.group_id)  # Initializing LongPoll API
        except ApiError as e:
            e_str = str(e)
            if "[5]" in e_str:
                print("Token not valid!")
            elif "[100]" in e_str:
                print("Group ID not valid!")
            else:
                print("Something went wrong...\n", e_str)
            exit()
        self.db = db
        self.score = 0
        self.auto_shitpost = 1
        self.msg_recipient = ""

    def get_event_listener(self):  # Return current events from a listener
        return self.long_poll.listen()

    # --- Messages integration

    def set_message_payload(self, text):  # Send a message to a chat
        msg_construct(self.vk_api, self.msg_recipient, text)

    def set_message_recipient(self, event):  # Set peer_id (where to send the message)
        self.msg_recipient = event.obj.peer_id

    # --- LOCAL

    # --- Score

    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score

    # --- Auto-shitpost status

    def get_status(self):
        return self.auto_shitpost

    def set_status(self, status):
        self.auto_shitpost = status

    # --- DATABASE

    # --- Database scores

    def get_database_score(self):
        return self.db.get_value("scores", self.msg_recipient)

    def set_database_score(self, score):
        self.db.update_value("scores", "score", self.msg_recipient, score)

    # --- Database auto-shitpost status

    def get_database_status(self):
        return self.db.get_value("statuses", self.msg_recipient)

    def set_database_status(self, status):
        self.db.update_value("statuses", "status", self.msg_recipient, status)

    # --- Methods

    def shitpost(self):  # To shitpost a random message from three arrays
        self.set_message_payload(shitpost())

    def fortune(self):  # To pick a random BSD-styled fortune from a fortunes list
        self.set_message_payload(fortune())
