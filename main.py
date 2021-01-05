from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.exceptions import ApiError

import bot_functions
import bot_utils


class MainFunc:
    def __init__(self, token, group_id, db):
        print("Starting bot initialization...")
        print("Initializing VK API...")
        self.vk_session = VkApi(token=token)  # Initializing session
        self.vk_api = self.vk_session.get_api()  # Initializing API
        print("Ended VK API initialization!")
        self.group_id = group_id
        self.group_name = f"club{self.group_id}"
        print("Initializing LongPoll...")
        try:
            self.long_poll = VkBotLongPoll(self.vk_session, self.group_id)  # Initializing LongPoll API
        except ApiError as e:
            e_str = str(e)
            if "[5]" in e_str:
                print("Token not valid!")
            elif "[100]" in e_str:
                print("Group ID not valid!")
            else:
                print(f"Something went wrong...\n{e_str}")
            exit()
        print("Ended LongPoll initialization!")
        self.db = db
        self.score = 0
        self.auto_shitpost = 1
        self.msg_recipient = ""
        print("Ended bot initialization! Bot is up and running...")

    def get_event_listener(self):  # Return current events from a listener
        return self.long_poll.listen()

    # --- Messages integration

    def set_message_payload(self, text):  # Send a message to a chat
        bot_utils.msg_construct(self.vk_api, self.msg_recipient, text)
        self.set_score(self.get_score() - 1)

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
        self.set_message_payload(bot_functions.shitpost())
        self.set_score(1)

    def fortune(self):  # To pick a random BSD-styled fortune from a fortunes list
        self.set_message_payload(bot_functions.fortune())

    def help_com(self):  # To get help from a bot
        self.set_message_payload(bot_functions.help_com())

    def shitpost_status(self, event):  # To turn off auto-shitpost
        # Checking if the user is an owner
        try:
            if bot_utils.check_for_owner(self.vk_api.messages.getConversationMembers(peer_id=self.msg_recipient,
                                                                                     group_id=self.group_id)["items"],
                                         event):
                if self.get_status() == 0:  # Turning on auto-shitpost
                    self.set_status(1)
                    self.set_message_payload("Now the bot will auto-shitpost!")
                else:  # Turning off auto-shitpost
                    self.set_status(0)
                    self.set_message_payload("Now the bot will NOT auto-shitpost... You're no fun :(")
                    self.set_score(self.get_score() + 1)
            else:  # If the user is not an owner
                self.set_message_payload("You're not an admin bro, get yourself some moderating privileges")
        except ApiError:
            self.set_message_payload("Give the bot admin, pls. It cannot access the API :(")

    def check_status(self):  # To check auto-shitpost status
        if self.get_status() == 1:
            self.shitpost() if self.get_score() >= 10 else self.set_score(self.get_score() + 1)

    def __del__(self):
        print("Exiting bot...")
