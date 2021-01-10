from os import environ

from vk_api.bot_longpoll import VkBotEventType

from database import Database
from main import Main


class MainBot(Main):
    def __init__(self, token, group_id, db):
        super().__init__(token, group_id, db)

    def main_listen(self):
        for event in self.get_event_listener():  # Listening to events
            if event.type == VkBotEventType.MESSAGE_NEW:  # If a new message pops up
                self.set_message_recipient(event)

                setattr(self, "score", self.get_database_score())  # This is the beginning of db-local transaction
                setattr(self, "auto_shitpost", self.get_database_status())  # This is the end of db-local transaction

                # Local work
                #    Check if "fortune" is in the text      Either private message event or ping in a group chat
                if "fortune" in event.obj.text.lower() and (event.from_user or self.group_name in event.obj.text):
                    self.fortune()
                #    Check if "auto" is in the text                 Only works in group chats and with ping
                elif "auto" in event.obj.text.lower() and self.group_name in event.obj.text and event.from_chat:
                    self.shitpost_status(event)
                #    Check if "help is in the text"         Either private message event or ping in a group chat
                elif "help" in event.obj.text.lower() and (event.from_user or self.group_name in event.obj.text):
                    self.help_com()
                #   Check if either "shitpost" is in the text and it's an event from user
                #       OR       check if the bot was pinged in a group chat
                elif ("shitpost" in event.obj.text.lower() and event.from_user) or (
                        self.group_name in event.obj.text and event.from_chat):
                    self.shitpost()

                self.check_status()
                # Local work END

                self.set_database_score(getattr(self, "score"))  # This is the beginning of local-db transaction
                self.set_database_status(getattr(self, "auto_shitpost"))  # This is the end of local-db transaction


if __name__ == "__main__":
    # Token, group_id, database
    bot = MainBot(environ["BOT_TOKEN"], environ["VK_GROUP_ID"], Database("conf_db.db"))
    try:
        bot.main_listen()
    except KeyboardInterrupt:
        bot.db.close_db()
        exit()
