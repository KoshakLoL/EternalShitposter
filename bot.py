from vk_api.bot_longpoll import VkBotEventType

from bot_methods import BotMethods
from database import DataBase
from os import environ


class MainBot(BotMethods):
    def __init__(self, token, group_id, db):
        super().__init__(token, group_id, db)
        for event in self.get_event_listener():
            if event.type == VkBotEventType.MESSAGE_NEW:
                self.set_message_recipient(event)

                self.set_score(self.get_database_score())  # This is the beginning of db-local transaction
                self.set_status(self.get_database_status())  # This is the end of db-local transaction

                # Local work
                #    Check if "fortune" is in the text      Either private message event or ping in a group chat
                if "fortune" in event.obj.text.lower() and (event.from_user or self.group_name in event.obj.text):
                    self.bot_fortune()
                #    Check if "auto" is in the text                 Only works in group chats and with ping
                elif "auto" in event.obj.text.lower() and self.group_name in event.obj.text and event.from_chat:
                    self.bot_auto(event)
                #    Check if "help is in the text"         Either private message event or ping in a group chat
                elif "help" in event.obj.text.lower() and (event.from_user or self.group_name in event.obj.text):
                    self.bot_help_com()
                #   Check if either "shitpost" is in the text and it's an event from user
                #       OR       check if the bot was pinged in a group chat
                elif ("shitpost" in event.obj.text.lower() and event.from_user) or (
                        self.group_name in event.obj.text and event.from_chat):
                    self.bot_shitpost()

                self.bot_check_status()
                # Local work END

                self.set_database_score(self.get_score())  # This is the beginning of local-db transaction
                self.set_database_status(self.get_status())  # This is the end of local-db transaction


if __name__ == "__main__":
    try:
        # Token, group_id, database
        MainBot(environ["BOT_TOKEN"], "200700644", DataBase("conf_db.db"))
    except Exception as e:
        print(e)
    finally:
        exit()
