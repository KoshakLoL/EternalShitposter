from main import MainFunc

from bot_utils import check_for_owner


class BotMethods(MainFunc):
    def __init__(self, token, group_id, db):
        super().__init__(token, group_id, db)

    def bot_fortune(self):
        self.fortune()
        self.set_score(self.get_score() - 1)

    def bot_auto(self, event):
        response = self.vk_api.messages.getConversationMembers(peer_id=self.msg_recipient,
                                                               group_id=self.group_id)["items"]
        if check_for_owner(response, event):
            if self.get_status() == 0:
                self.set_status(1)
                self.set_message_payload("Now the bot will auto-shitpost!")
                self.set_score(self.get_score() - 1)
            else:
                self.set_status(0)
                self.set_message_payload("Now the bot will NOT auto-shitpost... You're no fun :(")
        else:
            self.set_message_payload("You're not an admin bro, get yourself some moderating privileges")

    def bot_shitpost(self):
        self.shitpost()
        self.set_score(1)

    def bot_check_status(self):
        if self.get_status() == 1:
            if self.get_score() >= 10:
                self.shitpost()
                self.set_score(1)
            else:
                self.set_score(self.get_score() + 1)
