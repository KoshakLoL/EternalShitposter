from bot_utils import check_for_owner
from main import MainFunc


class BotMethods(MainFunc):
    def __init__(self, token, group_id, db):
        super().__init__(token, group_id, db)

    def bot_fortune(self):  # Fortune function logic
        self.fortune()
        self.set_score(self.get_score() - 1)

    def bot_auto(self, event):
        # Checking if the user is an owner
        if check_for_owner(self.vk_api.messages.getConversationMembers(peer_id=self.msg_recipient,
                                                                       group_id=self.group_id)["items"], event):
            if self.get_status() == 0:  # Turning on auto-shitpost
                self.set_status(1)
                self.set_message_payload("Now the bot will auto-shitpost!")
                self.set_score(self.get_score() - 1)
            else:  # Turning off auto-shitpost
                self.set_status(0)
                self.set_message_payload("Now the bot will NOT auto-shitpost... You're no fun :(")
        else:  # If the user is not an owner
            self.set_message_payload("You're not an admin bro, get yourself some moderating privileges")

    def bot_shitpost(self):  # Shitpost function logic
        self.shitpost()
        self.set_score(1)

    def bot_check_status(self):  # Auto function logic
        if self.get_status() == 1:
            self.bot_shitpost() if self.get_score() >= 10 else self.set_score(self.get_score() + 1)

    def bot_help_com(self):  # Help function logic
        self.help_com()
        self.set_score(self.get_score() - 1)