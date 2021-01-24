from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.exceptions import ApiError

import bot_functions
import bot_utils
import re

log = bot_utils.get_yml_logger("logging.yml", __name__)


class Main:
    def __init__(self, token, group_id, db):
        log.info("Starting bot initialization")
        log.info(f"Initializing VK API with {token[:4]}**** token")
        self.vk_session = VkApi(token=token)  # Initializing session
        self.vk_api = self.vk_session.get_api()  # Initializing API
        log.info("Ended VK API initialization")
        self.group_id = group_id
        self.group_name = f"club{self.group_id}"
        log.info(f"Initializing LongPoll for {self.group_name}")
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
        log.info(f"Ended LongPoll initialization")
        self.db = db
        self.score = 0
        self.auto_shitpost = 1
        self.auto_shitpost_limiter = 10
        self.msg_recipient = ""
        log.info("Ended bot initialization! Bot is up and running...")

    # --- Messages integration

    def set_message_payload(self, text):  # Send a message to a chat
        bot_utils.msg_construct(self.vk_api, self.msg_recipient, text)
        self.score -= 1

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

    # --- Database auto-shitpost limiter

    def get_database_limiter(self):
        return self.db.get_value("limiters", self.msg_recipient)

    def set_database_limiter(self, limiter):
        self.db.update_value("limiters", "limiter", self.msg_recipient, limiter)

    # --- Methods

    def check_owner(self, event):
        try:
            for entry in self.vk_api.messages.getConversationMembers(peer_id=self.msg_recipient,
                                                                     group_id=self.group_id)["items"]:
                if entry["member_id"] == event.obj.from_id and (
                        ("is_admin" in entry and entry["is_admin"])
                        or ("is_owner" in entry and entry["is_owner"])):
                    return True
        except ApiError:
            self.set_message_payload("ApiError! Either you're not an admin, or the bot is not an admin.")
            return False

    def shitpost(self):  # To shitpost a random message from three arrays
        self.set_message_payload(bot_functions.shitpost())
        self.score = 1

    def fortune(self):  # To pick a random BSD-styled fortune from a fortunes list
        self.set_message_payload(bot_functions.fortune())

    def help_com(self):  # To get help from a bot
        self.set_message_payload(bot_functions.help_com())

    def shitpost_status(self, event):  # To turn off auto-shitpost
        # Checking if the user is an owner
        if self.check_owner(event):
            if self.auto_shitpost == 0:  # Turning on auto-shitpost
                self.auto_shitpost = 1
                self.set_message_payload("Now the bot will auto-shitpost!")
            else:  # Turning off auto-shitpost
                self.auto_shitpost = 0
                self.set_message_payload("Now the bot will NOT auto-shitpost... You're no fun :(")
                self.score += 1

    def shitpost_limiter(self, event):
        if self.check_owner(event):
            try:
                self.auto_shitpost_limiter = int(re.compile(r"limit\s\d+").findall(event.obj.text)[0][6:])
                self.set_message_payload(f"Current auto-shitpost limit is: {self.auto_shitpost_limiter}")
            except IndexError:
                self.set_message_payload("Did not specify the limit! ([bot_ping] help)")

    def check_status(self):  # To check auto-shitpost status
        if self.auto_shitpost and self.score >= self.auto_shitpost_limiter:
            self.shitpost()
        else:
            self.score += 1

    def __del__(self):
        log.info("Exiting the bot...")
