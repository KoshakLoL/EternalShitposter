import logging.config

import yaml
from vk_api.utils import get_random_id


def msg_construct(vk, msg_recipient, message):
    vk.messages.send(
        peer_id=msg_recipient,
        random_id=get_random_id(),
        message=message
    )


def check_for_owner(response, event):
    for entry in response:
        # If it is the same member as the one who called
        # If the member is an owner or an admin
        if entry["member_id"] == event.obj.from_id and (
                ("is_admin" in entry and entry["is_admin"]) or
                ("is_owner" in entry and entry["is_owner"])
        ):
            return True
    return False


def get_yml_logger(config, name):
    with open(config, "r") as f:
        logging.config.dictConfig(yaml.safe_load(f))
    return logging.getLogger(name)
